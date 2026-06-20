"""
Модуль для скачивания комиксов с любых сайтов с поддержкой многопоточности
"""

import os
import sys
import re
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import subprocess
import json
import tempfile
import shutil
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from urllib.parse import urljoin, urlparse

import mmap
import zipfile
import img2pdf

class UniversalComicDownloader:
    """Универсальный загрузчик комиксов с любых сайтов"""
    _last_request_time = 0.0
    _rate_limit_lock = threading.Lock()
    
    def __init__(self, max_workers=3):
        self.max_workers = max_workers
        self.session = requests.Session()
        
        # Настройка Retry для стабильности сети
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
                
        self.lock = threading.Lock()
        self.cancelled = False
        self.cancel_event = threading.Event()
        self.pause_event = threading.Event()
        self.pause_event.set()  # Сразу разрешаем работу
        
        # Задержка между запросами картинок (в секундах) для защиты от 503
        self.rate_limit_delay = 0.75 
        
        # Минимальный размер изображения (в байтах) для фильтрации рекламы/иконок
        self.min_image_size = 50 * 1024  # 50 KB
        
    def close(self):
        """Корректно закрыть сессию и освободить ресурсы"""
        if hasattr(self, 'session') and self.session:
            self.session.close()
    
    def pause(self):
        """Поставить скачивание на паузу"""
        self.pause_event.clear()
        
    def resume(self):
        """Продолжить скачивание"""
        self.pause_event.set()
        
    def cancel(self):
        """Отменить загрузку"""
        self.cancelled = True
        self.cancel_event.set()
    
    def reset_cancel(self):
        """Сбросить флаг отмены"""
        self.cancelled = False
        self.cancel_event.clear()
    
    def sanitize_filename(self, filename):
        """Очистить имя файла"""
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'[_\s]+', '_', filename)
        filename = filename.strip('_')
        if len(filename) > 200:
            filename = filename[:200]
        return filename
    
    def get_base_url(self, url):
        """Получить базовый URL для относительных ссылок"""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    
    def detect_site_type(self, url):
        """Определить тип сайта по URL"""
        domain = urlparse(url).netloc.lower()
        
        if 'telegra.ph' in domain:
            return 'telegraph'
        elif 'sexkomix' in domain:
            return 'sexkomix'
        else:
            return 'generic'
    
    def parse_telegraph(self, soup, base_url):
        """Парсер для telegra.ph"""
        images = soup.find_all('img')
        image_urls = []
        
        for img in images:
            src = img.get('src')
            if src:
                # Исправить URL
                if src.startswith('http://') or src.startswith('https://'):
                    image_urls.append(src)
                elif src.startswith('//'):
                    image_urls.append('https:' + src)
                elif src.startswith('/'):
                    image_urls.append('https://telegra.ph' + src)
                else:
                    image_urls.append('https://telegra.ph/' + src)
        
        return image_urls
    
    def parse_sexkomix(self, soup, base_url):
        """Парсер для sexkomix2.com и подобных сайтов"""
        image_urls = []
        seen_urls = set()
        
        # Найти все ссылки с классом fancybox (это страницы комикса)
        fancybox_links = soup.find_all('a', class_='fancybox', href=True)
        
        for link in fancybox_links:
            href = link['href']
            # Проверить что это изображение
            if re.search(r'\.(jpg|jpeg|png|gif|webp)(\?.*)?$', href, re.IGNORECASE):
                full_url = urljoin(base_url, href)
                if full_url not in seen_urls:
                    image_urls.append(full_url)
                    seen_urls.add(full_url)
        
        # Если не нашли fancybox, попробовать другие варианты
        if not image_urls:
            # Попробовать найти изображения в определённых контейнерах
            for container_class in ['comic-page', 'page-image', 'comic-image', 'gallery-item']:
                containers = soup.find_all(class_=container_class)
                for container in containers:
                    img = container.find('img')
                    if img and img.get('src'):
                        src = img['src']
                        full_url = urljoin(base_url, src)
                        if full_url not in seen_urls:
                            image_urls.append(full_url)
                            seen_urls.add(full_url)
        
        return image_urls
    
    def parse_generic(self, soup, base_url):
        """Универсальный парсер для неизвестных сайтов"""
        image_urls = []
        seen_urls = set()
        
        # 1. Обычные <img> теги
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if src:
                full_url = urljoin(base_url, src)
                if full_url not in seen_urls:
                    image_urls.append(full_url)
                    seen_urls.add(full_url)
        
        # 2. Изображения в ссылках <a href="image.jpg">
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Проверить расширение
            if re.search(r'\.(jpg|jpeg|png|gif|webp|bmp)(\?.*)?$', href, re.IGNORECASE):
                full_url = urljoin(base_url, href)
                if full_url not in seen_urls:
                    image_urls.append(full_url)
                    seen_urls.add(full_url)
        
        # 3. Background images в CSS
        for elem in soup.find_all(style=True):
            style = elem['style']
            bg_match = re.search(r'background-image:\s*url\([\'"]?([^\'"]+)[\'"]?\)', style)
            if bg_match:
                bg_url = bg_match.group(1)
                full_url = urljoin(base_url, bg_url)
                if full_url not in seen_urls:
                    image_urls.append(full_url)
                    seen_urls.add(full_url)
        
        return image_urls
    
    def filter_images(self, image_urls, referer, site_type):
        """Фильтровать изображения по размеру (убрать рекламу/иконки)"""
        # Для специализированных парсеров не фильтруем
        if site_type in ['telegraph', 'sexkomix']:
            print(f"✅ Специализированный парсер: {len(image_urls)} изображений")
            return image_urls
        
        # Для generic парсера фильтруем по размеру
        headers = {'Referer': referer}
        
        def check_url(url):
            if self.cancelled:
                return None
            try:
                # HEAD запрос для проверки размера
                response = self.session.head(url, timeout=10, headers=headers, allow_redirects=True)
                
                # Если HEAD не работает, пробуем GET с Range
                if response.status_code >= 400:
                    response = self.session.get(url, timeout=10, headers={**headers, 'Range': 'bytes=0-1024'}, stream=True)
                    response.close() # Обязательно закрываем stream!
                
                # Проверить Content-Type
                content_type = response.headers.get('Content-Type', '')
                if not content_type.startswith('image/'):
                    return None
                
                # Проверить размер
                content_length = response.headers.get('Content-Length')
                if content_length:
                    if int(content_length) >= self.min_image_size:
                        return url
                    else:
                        return None
                else:
                    # Если размер неизвестен, добавить (проверим при загрузке)
                    return url
            except Exception:
                # В случае ошибки добавить (проверим при загрузке)
                return url

        # Распараллеливаем проверку размеров
        with ThreadPoolExecutor(max_workers=min(10, self.max_workers * 2)) as executor:
            results = list(executor.map(check_url, image_urls))
            
        filtered = [url for url in results if url is not None]
        print(f"✅ После фильтрации: {len(filtered)} изображений")
        return filtered
    
    def get_gallery_dl_info(self, url, progress_callback=None):
        """Попытка получить информацию с помощью gallery-dl"""
        if progress_callback:
            progress_callback(0, 100, "Получение информации...")
        try:
            # Используем gallery-dl из venv если он есть, иначе глобальный
            exe_dir = os.path.dirname(sys.executable)
            gallery_dl_cmd = os.path.join(exe_dir, "gallery-dl.exe" if os.name == 'nt' else "gallery-dl")
            if not os.path.exists(gallery_dl_cmd):
                gallery_dl_cmd = "gallery-dl"
                
            args = [gallery_dl_cmd, "-j"]
            args.append(url)
            
            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            start_time = time.time()
            timeout_seconds = 45  # Максимальное время ожидания ответа
            
            stdout = ""
            # Читаем данные через communicate с таймаутом, чтобы не переполнить pipe-буфер ОС (deadlock)
            while True:
                if self.cancel_event.is_set():
                    process.kill()
                    process.wait()
                    return None
                    
                try:
                    out, err = process.communicate(timeout=0.5)
                    stdout = out
                    break
                except subprocess.TimeoutExpired:
                    if time.time() - start_time > timeout_seconds:
                        print(f"⚠️ Ошибка: gallery-dl завис (тайм-аут {timeout_seconds}с)")
                        process.kill()
                        process.wait()
                        return None
                        
            if process.returncode != 0 or not stdout.strip():
                return None
            
            data = json.loads(stdout)
            if not data or not isinstance(data, list):
                return None
                
            title = None
            image_urls = []
            
            for item in data:
                if isinstance(item, list) and len(item) >= 2:
                    if item[0] == 2 and isinstance(item[1], dict):
                        title = item[1].get("title")
                    elif item[0] == 3 and isinstance(item[1], str):
                        image_urls.append(item[1])
                        
            if image_urls:
                return {
                    'title': title,
                    'image_urls': image_urls,
                    'page_count': len(image_urls),
                    'is_archive': False
                }
        except Exception as e:
            print(f"Ошибка gallery-dl: {e}")
        return None

    def get_page_info(self, url, progress_callback=None):
        """Получить информацию о странице (универсальный метод)"""


        # 1. Сначала пробуем gallery-dl
        print(f"🔍 Попытка использовать gallery-dl для {url}")
        info = self.get_gallery_dl_info(url, progress_callback)
        if info and info['image_urls']:
            print(f"✅ gallery-dl успешно нашел {len(info['image_urls'])} изображений")
            return info
            
        print("⚠️ gallery-dl не справился, используем встроенные парсеры")
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            base_url = self.get_base_url(url)
            
            # Поиск прямых ссылок на архивы
            archive_link = soup.find('a', href=re.compile(r'\.(zip|rar|cbz|pdf)$', re.IGNORECASE))
            if archive_link:
                return {
                    'title': None,
                    'image_urls': [],
                    'page_count': 0,
                    'is_archive': True,
                    'archive_url': urljoin(base_url, archive_link['href'])
                }
                
            site_type = self.detect_site_type(url)
            
            print(f"🔍 Определён тип сайта: {site_type}")
            
            # Заголовок (попробовать разные варианты)
            title = None
            
            # 1. <h1>
            title_tag = soup.find('h1')
            if title_tag:
                title = title_tag.get_text().strip()
            
            # 2. <title>
            if not title:
                title_tag = soup.find('title')
                if title_tag:
                    title = title_tag.get_text().strip()
            
            # 3. og:title
            if not title:
                og_title = soup.find('meta', property='og:title')
                if og_title:
                    title = og_title.get('content', '').strip()
            
            # Найти изображения в зависимости от типа сайта
            if site_type == 'telegraph':
                image_urls = self.parse_telegraph(soup, base_url)
            elif site_type == 'sexkomix':
                image_urls = self.parse_sexkomix(soup, base_url)
            else:
                image_urls = self.parse_generic(soup, base_url)
            
            print(f"🔍 Найдено {len(image_urls)} изображений")
            
            # Фильтровать по размеру (только для generic)
            filtered_urls = self.filter_images(image_urls, referer=url, site_type=site_type)
            
            return {
                'title': title,
                'image_urls': filtered_urls,
                'page_count': len(filtered_urls),
                'is_archive': False
            }
        except Exception as e:
            raise Exception(f"Ошибка получения страницы: {e}")
    
    def download_image(self, url, retries=5, referer=None, save_path=None, quality=95):
        """Скачать одно изображение с повторными попытками.
        Если save_path задан — сохраняет на диск и возвращает путь (экономит RAM).
        Иначе — возвращает PIL Image объект (для обратной совместимости).
        """
        last_error = None
        
        # Добавить Referer для обхода hotlink защиты
        headers = {}
        if referer:
            if 'hitomi.la' in referer:
                match = re.search(r'(\d+)\.html', referer) or re.search(r'(\d+)\.html', url)
                if match:
                    gallery_id = match.group(1)
                    headers['Referer'] = f"https://hitomi.la/reader/{gallery_id}.html"
                else:
                    headers['Referer'] = "https://hitomi.la/"
            else:
                headers['Referer'] = referer
            
        self.pause_event.wait()
        if self.cancelled:
            return None
            
        for attempt in range(retries):
            self.pause_event.wait()
            if self.cancelled:
                return None
                
            # Применяем глобальную задержку между запросами для защиты от 503
            if self.rate_limit_delay > 0:
                with UniversalComicDownloader._rate_limit_lock:
                    now = time.time()
                    elapsed = now - UniversalComicDownloader._last_request_time
                    wait_time = self.rate_limit_delay - elapsed
                    if wait_time > 0:
                        if self.cancel_event.wait(wait_time):
                            return None
                    UniversalComicDownloader._last_request_time = time.time()
                
            try:
                response = self.session.get(url, timeout=15, headers=headers)
                
                if response.status_code == 503:
                    print(f"⚠️ Ошибка 503 (Сервер перегружен), ждем перед повторной попыткой {attempt+1}/{retries}...")
                    last_error = requests.exceptions.HTTPError("503 Server Error: Service Unavailable", response=response)
                    cooldown = 3.0 * (attempt + 1)
                    with UniversalComicDownloader._rate_limit_lock:
                        UniversalComicDownloader._last_request_time = time.time() + cooldown
                    if self.cancel_event.wait(cooldown):
                        return None
                    continue
                    
                response.raise_for_status()
                
                # Проверить размер (только для generic сайтов)
                if len(response.content) < 1024:  # Меньше 1KB - точно не страница комикса
                    raise Exception(f"Изображение слишком маленькое ({len(response.content)} байт)")
                
                img_data = BytesIO(response.content)
                del response  # Освобождаем сырые байты ответа
                img = Image.open(img_data)
                
                # Конвертировать в RGB
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                if save_path:
                    # Сохраняем на диск и сразу освобождаем RAM
                    img.save(save_path, format='JPEG', quality=quality)
                    img.close()
                    del img, img_data
                    return save_path
                else:
                    return img
            except requests.exceptions.HTTPError as e:
                # 404 - страница не существует, не повторять
                if getattr(e, 'response', None) and e.response.status_code == 404:
                    raise Exception(f"Изображение не найдено (404): {url}")
                last_error = e
                if attempt < retries - 1:
                    if self.cancel_event.wait(1 * (attempt + 1)):
                        return None
            except Exception as e:
                last_error = e
                if attempt < retries - 1:
                    if self.cancel_event.wait(1 * (attempt + 1)):
                        return None
        
        raise Exception(f"Ошибка загрузки изображения после {retries} попыток: {last_error}")
    
    def download_images(self, image_urls, referer=None, progress_callback=None, temp_dir=None, quality=95):
        """Скачать все изображения с многопоточностью.
        Если temp_dir задан — сохраняет на диск и возвращает пути к файлам.
        Иначе — возвращает PIL Image объекты (обратная совместимость).
        """
        results = [None] * len(image_urls)
        
        def download_with_index(idx, url):
            self.pause_event.wait()
            if self.cancelled:
                return idx, None
            
            try:
                save_path = os.path.join(temp_dir, f"page_{idx:04d}.jpg") if temp_dir else None
                result = self.download_image(url, referer=referer, save_path=save_path, quality=quality)
                if progress_callback:
                    progress_callback(idx + 1, len(image_urls))
                return idx, result
            except Exception as e:
                print(f"⚠️ Ошибка загрузки изображения #{idx+1}: {e}")
                return idx, None
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(download_with_index, idx, url): idx 
                for idx, url in enumerate(image_urls)
            }
            
            for future in as_completed(futures):
                self.pause_event.wait()
                if self.cancelled:
                    executor.shutdown(wait=False, cancel_futures=True)
                    break
                
                idx, result = future.result()
                if result is not None:
                    results[idx] = result
        
        # Убрать None (сохраняя порядок)
        results = [r for r in results if r is not None]
        return results
    
    def save_as_pdf(self, image_paths, output_path):
        """Сохранить изображения в PDF из файлов на диске с помощью img2pdf"""
        if not image_paths:
            raise Exception("Нет изображений для сохранения")
        
        try:
            with open(output_path, "wb") as f:
                f.write(img2pdf.convert(image_paths))
            return os.path.getsize(output_path)
        except Exception as e:
            raise Exception(f"Ошибка создания PDF с помощью img2pdf: {e}")
    
    def save_as_cbz(self, image_paths, output_path):
        """Сохранить изображения в CBZ из файлов на диске (без декодирования, т.к. они уже сжаты при скачивании)"""
        if not image_paths:
            raise Exception("Нет изображений для сохранения")
        
        try:
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_STORED) as cbz:
                for idx, img_path in enumerate(image_paths, 1):
                    page_name = f"page_{idx:04d}.jpg"
                    cbz.write(img_path, page_name)
            
            return os.path.getsize(output_path)
        except Exception as e:
            raise Exception(f"Ошибка создания CBZ: {e}")
    
    def download_comic(self, url, output_dir, format='pdf', quality=95, 
                      progress_callback=None, counter=None):
        """
        Скачать комикс с любого сайта.
        Картинки сохраняются во временную папку на диске, а не в оперативку.
        
        Args:
            url: URL страницы с комиксом
            output_dir: Папка для сохранения
            format: Формат (pdf или cbz)
            quality: Качество JPEG (60-95)
            progress_callback: Функция для обновления прогресса
            counter: Номер для автоназвания
        
        Returns:
            dict с информацией о загрузке
        """
        temp_dir = None
        try:
            # Получить информацию
            if progress_callback:
                progress_callback(0, 100, "В очереди на парсинг...")
            
            info = self.get_page_info(url, progress_callback)
            title = info.get('title')
            is_archive = info.get('is_archive', False)
            
            # Сгенерировать базовое имя файла
            if title and title.strip():
                base_name = self.sanitize_filename(title)
            elif counter is not None:
                base_name = f"comic_{counter:04d}"
            else:
                base_name = f"comic_{int(time.time())}"
            
            if is_archive:
                # Скачиваем архив напрямую
                archive_url = info['archive_url']
                ext = archive_url.split('.')[-1].lower()
                output_path = os.path.join(output_dir, f"{base_name}.{ext}")
                
                if progress_callback:
                    progress_callback(5, 100, "Проверка архива...")
                    
                response = self.session.get(archive_url, stream=True, timeout=30)
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                
                if os.path.exists(output_path):
                    local_size = os.path.getsize(output_path)
                    if total_size and local_size >= total_size:
                        response.close()
                        if progress_callback:
                            progress_callback(100, 100, "Уже скачано!")
                        return {
                            'success': True,
                            'url': url,
                            'title': title or base_name,
                            'file_path': output_path,
                            'format': ext,
                            'file_size': local_size,
                            'pages': 1,
                            'expected_pages': 1,
                            'is_complete': True
                        }
                
                if progress_callback:
                    progress_callback(10, 100, "Скачивание архива...")
                
                downloaded_size = 0
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        self.pause_event.wait()
                        if self.cancelled:
                            os.remove(output_path)
                            raise Exception("Отменено пользователем")
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            if total_size and progress_callback:
                                percent = 10 + int((downloaded_size / total_size) * 90)
                                progress_callback(percent, 100, f"Скачивание архива ({percent}%)")
                response.close()
                                
                if progress_callback:
                    progress_callback(100, 100, "Готово!")
                    
                return {
                    'success': True,
                    'url': url,
                    'title': title or base_name,
                    'file_path': output_path,
                    'format': ext,
                    'file_size': downloaded_size,
                    'pages': 1,
                    'expected_pages': 1,
                    'is_complete': True
                }

            # Обычный режим картинок
            image_urls = info.get('image_urls', [])
            
            if not image_urls:
                raise Exception("Не найдено изображений или архива на странице")
                
            output_path = os.path.join(output_dir, f"{base_name}.{format.lower()}")
            if os.path.exists(output_path):
                is_complete = False
                if format.lower() == 'cbz':
                    try:
                        with zipfile.ZipFile(output_path, 'r') as zf:
                            if len(zf.namelist()) >= len(image_urls):
                                is_complete = True
                    except Exception:
                        pass
                else:
                    # Попытка получить количество страниц PDF через regex/mmap
                    pdf_pages = None
                    try:
                        with open(output_path, 'rb') as f:
                            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                                matches = re.findall(br'/Count\s+(\d+)', mm)
                                if matches:
                                    pdf_pages = max(int(m) for m in matches)
                    except Exception:
                        pass
                    
                    if pdf_pages is not None:
                        if pdf_pages >= len(image_urls):
                            is_complete = True
                    else:
                        # Эвристика для PDF: если размер больше (кол-во страниц * 50KB), считаем полным
                        if os.path.getsize(output_path) >= len(image_urls) * 50 * 1024:
                            is_complete = True
                        
                if is_complete:
                    if progress_callback:
                        progress_callback(100, 100, "Уже скачано!")
                    return {
                        'success': True,
                        'url': url,
                        'title': title or base_name,
                        'file_path': output_path,
                        'format': format,
                        'file_size': os.path.getsize(output_path),
                        'pages': len(image_urls),
                        'expected_pages': len(image_urls),
                        'is_complete': True
                    }
            
            # Создать временную папку для картинок (не в RAM!)
            temp_dir = tempfile.mkdtemp(prefix='comic_dl_')
            
            # Скачать изображения на диск
            if progress_callback:
                progress_callback(10, 100, f"Загрузка {len(image_urls)} изображений...")
            
            def image_progress(current, total):
                percent = 10 + int((current / total) * 70)
                progress_callback(percent, 100, f"Загрузка {current}/{total}")
            
            image_paths = self.download_images(
                image_urls,
                referer=url,
                progress_callback=image_progress if progress_callback else None,
                temp_dir=temp_dir,
                quality=quality
            )
            
            if not image_paths:
                raise Exception(f"Не удалось загрузить изображения (0/{len(image_urls)}). Возможно, страница защищена или недоступна.")
            
            # Предупреждение если загрузились не все
            if len(image_paths) < len(image_urls):
                print(f"⚠️ Загружено {len(image_paths)}/{len(image_urls)} изображений. Некоторые страницы могут отсутствовать.")
            
            if self.cancelled:
                raise Exception("Отменено пользователем")
            
            # Сохранить
            if progress_callback:
                progress_callback(80, 100, f"Создание {format.upper()}...")
            
            if format.lower() == 'pdf':
                file_size = self.save_as_pdf(image_paths, output_path)
            elif format.lower() == 'cbz':
                file_size = self.save_as_cbz(image_paths, output_path)
            else:
                raise Exception(f"Неподдерживаемый формат: {format}")
            
            if progress_callback:
                progress_callback(100, 100, "Готово!")
            
            return {
                'success': True,
                'url': url,
                'title': title or base_name,
                'file_path': output_path,
                'format': format,
                'file_size': file_size,
                'pages': len(image_paths),
                'expected_pages': len(image_urls),  # Ожидаемое количество
                'is_complete': len(image_paths) == len(image_urls)  # Полный ли комикс
            }
            
        except Exception as e:
            return {
                'success': False,
                'url': url,
                'error': str(e)
            }
        finally:
            # Гарантированная очистка временных файлов и памяти
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
    
