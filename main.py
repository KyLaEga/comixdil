#!/usr/bin/env python3
"""
Universal Comic Downloader
Современная версия с графическим интерфейсом на PySide6
"""

import sys
import os

# Добавить путь к модулям
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from core.downloader import UniversalComicDownloader
from gui.main_window import MainWindow
from gui.theme import ThemeManager


def main():
    """Главная функция"""
    # Создать приложение Qt
    app = QApplication(sys.argv)
    
    # Применить современную дизайн-систему
    ThemeManager.apply_modern_dark(app)
    
    # Создать и показать главное окно
    window = MainWindow()
    window.show()
    
    # Запустить цикл обработки событий
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
