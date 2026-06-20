# 📚 Universal Comic Downloader

**Универсальный загрузчик комиксов** с поддержкой множества сайтов для **macOS**, **Windows** и **Linux**.

![Версия](https://img.shields.io/badge/версия-2.7.0-blue)
![Платформа](https://img.shields.io/badge/платформа-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey)
![Python](https://img.shields.io/badge/python-3.11+-green)

---

## ✨ Возможности

- 🌐 **Универсальный парсер** - загрузка комиксов с любых сайтов
- 🔄 **Конвертер форматов** - PDF ↔ CBZ
- 📚 **Библиотека** - организация коллекции с поиском и фильтрами
- 👁️ **Просмотрщик** - предпросмотр комиксов прямо в приложении
- ⌨️ **Горячие клавиши** - полная поддержка клавиатуры
- 🎨 **Современный интерфейс** - чистый, монохромный дизайн

---

## 🚀 Быстрый старт

### 🍎 macOS

```bash
# Распаковать
tar -xzf universal_comic_downloader_v2.7.0.tar.gz
cd telegraph_comic_downloader_gui

# Вариант 1: Запустить напрямую
./launch_macos.command

# Вариант 2: Создать .app
./create_simple_app.sh
cp -r "dist/Universal Comic Downloader.app" /Applications/
```

**При первом запуске**: Правая кнопка → "Открыть" → Подтвердить

### 🪟 Windows

```batch
cd telegraph_comic_downloader_gui
launch_windows.bat

:: Или собрать .exe
build_windows_exe.bat
```

### 🐧 Linux

```bash
cd telegraph_comic_downloader_gui
./launch_linux.sh

# Или собрать AppImage
./build_linux_appimage.sh
```

---

## 📋 Использование

### 1. Добавить комикс
1. Вставить URL (`Cmd+V` / `Ctrl+V`)
2. Нажать **"Добавить"** или `Enter`

### 2. Начать загрузку
Нажать **"▶ Начать загрузку"**

### 3. Просмотреть библиотеку
Вкладка **"📚 Библиотека"** → Двойной клик на комикс

### 4. Конвертировать формат
- **Из библиотеки**: Правая кнопка → "Конвертировать"
- **Любой файл**: Меню "Инструменты" → "Конвертация форматов"

---

## ⌨️ Горячие клавиши

| Действие | macOS | Windows/Linux |
|----------|-------|---------------|
| Вставить | `⌘ Cmd + V` | `Ctrl + V` |
| Копировать | `⌘ Cmd + C` | `Ctrl + C` |
| Выделить всё | `⌘ Cmd + A` | `Ctrl + A` |
| Удалить | `Delete` | `Delete` |

---

## 🌐 Поддерживаемые сайты

- ✅ **Telegraph** (telegra.ph)
- ✅ **SexKomix2** (sexkomix2.com)
- ✅ **Любые другие сайты** с комиксами (универсальный парсер)

---

## 🔧 Требования

- **Python**: 3.11+
- **Tkinter**: Обычно включён в Python
- **Интернет**: Для загрузки комиксов

### Для конвертации PDF:

| Платформа | Команда |
|-----------|---------|
| **macOS** | `brew install poppler` |
| **Linux** | `sudo apt install poppler-utils` |
| **Windows** | Скачать [Poppler](https://github.com/oschwartz10612/poppler-windows/releases) |

---

## 📁 Структура проекта

```
telegraph_comic_downloader_gui/
├── main.py                 # Точка входа
├── core/
│   ├── downloader.py       # Универсальный парсер
│   ├── converter.py        # Конвертер PDF ↔ CBZ
│   └── database.py         # SQLite библиотека
├── gui/
│   ├── main_window.py      # Главное окно
│   ├── converter_dialog.py # Диалог конвертера
│   └── comic_viewer.py     # Просмотрщик
└── utils/
    └── helpers.py          # Вспомогательные функции
```

---

## 🔧 Сборка приложений

| Платформа | Команда | Результат |
|-----------|---------|-----------|
| **macOS** | `./create_simple_app.sh` | `.app` (требует Python) |
| **macOS** | `./build_macos_app.sh` | Standalone `.app` |
| **Windows** | `build_windows_exe.bat` | `.exe` файл |
| **Linux** | `./build_linux_appimage.sh` | `.AppImage` |

---

## 📖 Документация

- [Горячие клавиши](KEYBOARD_SHORTCUTS.md)
- [Сборка для macOS](BUILD_MACOS_APP.md)
- [Сборка для Windows](WINDOWS_BUILD_GUIDE.md)
- [Сборка для Linux](LINUX_BUILD_GUIDE.md)

---

## 📝 История версий

### v2.7.0 (26 ноября 2025)
- ✅ Добавлен конвертер PDF ↔ CBZ
- ✅ Исправлен запуск .app на macOS

### v2.6.1 (26 ноября 2025)
- ✅ Убрана блокировка не-Telegraph URL
- ✅ Добавлена кнопка "Очистить библиотеку"

### v2.6.0 (26 ноября 2025)
- ✅ Универсальный парсер для любых сайтов
- ✅ Поддержка SexKomix2
- ✅ Горячие клавиши

---

## 📄 Лицензия

MIT License - свободное использование, модификация и распространение.

---

**Приятного использования! 🎨📚**
