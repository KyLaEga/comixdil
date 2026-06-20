import os
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor, QIcon, QPixmap
from PySide6.QtCore import QByteArray
from PySide6 import QtSvg  # noqa: F401

class ThemeManager:
    _ICONS_SUBDIR = os.path.join("assets", "icons")
    _THEMES_SUBDIR = os.path.join("assets", "themes")

    DARK = {
        "bg": "#1E1F22",
        "surface": "#2B2D31",
        "text": "#DBDEE1",
        "border": "#4E5058",
    }
    LIGHT = {
        "bg": "#F2F3F5",
        "surface": "#FFFFFF",
        "text": "#313338",
        "border": "#E3E5E8",
    }

    FONT_CAPTION = 11
    FONT_BASE = 13
    FONT_HEADER = 16
    FONT_H1 = 20

    BUTTON_HEIGHT_PRIMARY = 40
    BUTTON_HEIGHT_ICON = 40

    ICON_GLYPHS = {
        "play": "M8 5v14l11-7z",
        "pause": "M6 19h4V5H6v14zm8-14v14h4V5h-4z",
        "stop": "M6 6h12v12H6z",
        "scan": ("M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 "
                 "13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 "
                 "4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 "
                 "11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"),
        "volume": ("M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05"
                   "c1.48-.73 2.5-2.25 2.5-4.02z"),
        "volume_muted": ("M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45"
                         "c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64"
                         "l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86"
                         "-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3 3 4.27 "
                         "7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 "
                         "1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 "
                         "19.73l-9-9L4.27 3zM12 4 9.91 6.09 12 8.18V4z"),
        "download": "M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z",
        "folder": "M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z",
        "trash": "M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z",
        "settings": ("M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"),
        "brush": "M12 3a9 9 0 0 0 0 18c.83 0 1.5-.67 1.5-1.5 0-.39-.15-.74-.39-1.01-.23-.26-.38-.61-.38-.99 0-.83.67-1.5 1.5-1.5H16c2.76 0 5-2.24 5-5 0-4.42-4.03-8-9-8zm-5.5 9c-.83 0-1.5-.67-1.5-1.5S5.67 9 6.5 9 8 9.67 8 10.5 7.33 12 6.5 12zm3-4C8.67 8 8 7.33 8 6.5S8.67 5 9.5 5s1.5.67 1.5 1.5S10.33 8 9.5 8zm5 0c-.83 0-1.5-.67-1.5-1.5S13.67 5 14.5 5s1.5.67 1.5 1.5S15.33 8 14.5 8zm3 4c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z",
    }

    @classmethod
    def make_icon(cls, glyph_name: str, color: str) -> QIcon:
        path_d = cls.ICON_GLYPHS.get(glyph_name)
        if not path_d:
            return QIcon()
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
            f'width="48" height="48"><path fill="{color}" d="{path_d}"/></svg>'
        )
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(svg.encode("utf-8")), "SVG")
        return QIcon(pixmap)

    _active = DARK

    @classmethod
    def colors(cls) -> dict:
        return cls._active

    @staticmethod
    def _resource_root() -> Path:
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            return Path(meipass)
        if getattr(sys, "frozen", False):
            exe_dir = Path(sys.executable).resolve().parent
            if sys.platform == "darwin":
                mac_resources = exe_dir.parent / "Resources"
                if mac_resources.exists():
                    return mac_resources
            return exe_dir
        return Path(__file__).resolve().parent.parent

    @classmethod
    def asset_path(cls, relative: str) -> str:
        return str(cls._resource_root() / relative)

    @classmethod
    def icon_path(cls, filename: str) -> str:
        return str(cls._resource_root() / cls._ICONS_SUBDIR / filename)

    @classmethod
    def load_icon(cls, filename: str) -> QIcon:
        path = cls.icon_path(filename)
        if os.path.exists(path):
            icon = QIcon(path)
            if not icon.isNull():
                return icon
        return QIcon()

    @classmethod
    def _load_stylesheet(cls, theme_name: str, fallback_qss: str) -> str:
        qss_path = cls._resource_root() / cls._THEMES_SUBDIR / f"{theme_name}.qss"
        try:
            if qss_path.is_file():
                text = qss_path.read_text(encoding="utf-8")
                if text.strip():
                    return text
        except OSError:
            pass
        return fallback_qss

    @classmethod
    def _typography_qss(cls) -> str:
        return (
            f'QLabel[txt="h1"] {{ font-size: {cls.FONT_H1}px; font-weight: bold; }}'
            f'QLabel[txt="h2"] {{ font-size: {cls.FONT_HEADER}px; font-weight: bold; }}'
            f'QLabel[txt="body"] {{ font-size: {cls.FONT_BASE}px; }}'
            f'QLabel[txt="caption"] {{ font-size: {cls.FONT_CAPTION}px; }}'
        )

    @classmethod
    def apply_modern_dark(cls, app: QApplication):
        cls._active = cls.DARK
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(cls.DARK["bg"]))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(cls.DARK["text"]))
        palette.setColor(QPalette.ColorRole.Base, QColor(cls.DARK["surface"]))
        palette.setColor(QPalette.ColorRole.Text, QColor(cls.DARK["text"]))
        palette.setColor(QPalette.ColorRole.Button, QColor(64, 66, 73))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(cls.DARK["text"]))
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(148, 155, 164))
        app.setPalette(palette)

        qss = """
        QMainWindow, QWidget#sidebar { background-color: #1E1F22; }
        QWidget#card { background-color: #2B2D31; border-radius: 8px; }
        QWidget#toolbar_flat { background-color: #2B2D31; border-radius: 6px; }
        QWidget#controls_panel, QWidget#bottom_btns, QWidget#multi_slider_panel { background-color: #2B2D31; border-top: 1px solid #1E1F22; }
        QWidget#video_bg { background-color: #2B2D31; }
        QFrame#divider { max-height: 1px; min-height: 1px; background-color: #4E5058; border: none; }
        
        QPushButton { 
            background-color: #404249; color: #DBDEE1; 
            border: none; border-radius: 6px; 
            padding: 6px 14px; font-weight: 500;
            min-height: 24px;
        }
        QPushButton:hover { background-color: #4E5058; }
        QPushButton:pressed { background-color: #313338; }
        QPushButton:disabled { background-color: #313338; color: #5C5E66; }
        
        QPushButton#primary { background-color: #23A559; color: white; font-weight: bold; }
        QPushButton#primary:hover { background-color: #1D8A4A; }
        QPushButton#action { background-color: #5865F2; color: white; }
        QPushButton#action:hover { background-color: #4752C4; }
        QPushButton#danger { background-color: #DA373C; color: white; font-weight: bold; }
        QPushButton#danger:hover { background-color: #A12828; }
        
        QPushButton#secondary { 
            background-color: transparent; 
            border: 1px solid #4E5058; 
            border-radius: 6px;
            padding: 6px 14px; 
            color: #DBDEE1;
            min-height: 24px;
        }
        QPushButton#secondary:hover { background-color: #3F4147; border: 1px solid #5865F2; }
        
        QPushButton#collapser { background-color: transparent; color: #949BA4; padding: 4px 8px; }
        QPushButton#collapser:hover { background-color: #3F4147; color: #FFFFFF; }
        
        QPushButton#player_btn { background-color: transparent; color: #FFFFFF; font-weight: bold; padding: 0px; }
        QPushButton#player_btn:hover { color: #5865F2; }
        
        QLineEdit, QPlainTextEdit { 
            background-color: #1E1F22; color: #FFFFFF; 
            border: 1px solid #4E5058; border-radius: 6px; 
            padding: 4px 10px; selection-background-color: #5865F2;
        }
        QLineEdit:focus, QPlainTextEdit:focus { border: 1px solid #5865F2; }
        
        QLineEdit#spin_entry {
            border-radius: 0; border-left: none; border-right: none;
            padding: 4px;
        }
        QPushButton#spin_btn_left, QPushButton#spin_btn_right {
            background-color: #404249; border: 1px solid #4E5058; color: #DBDEE1;
            font-weight: bold; font-size: 14px; padding: 0; min-height: 24px;
        }
        QPushButton#spin_btn_left { border-top-right-radius: 0; border-bottom-right-radius: 0; border-right: none; }
        QPushButton#spin_btn_right { border-top-left-radius: 0; border-bottom-left-radius: 0; border-left: none; }
        QPushButton#spin_btn_left:hover, QPushButton#spin_btn_right:hover { background-color: #4E5058; }
        QPushButton#spin_btn_left:pressed, QPushButton#spin_btn_right:pressed { background-color: #313338; }
        
        QCheckBox { spacing: 8px; color: #DBDEE1; }
        QCheckBox::indicator, QRadioButton::indicator { width: 16px; height: 16px; border-radius: 4px; border: 2px solid #5865F2; background: transparent; }
        QRadioButton::indicator { border-radius: 8px; }
        QCheckBox::indicator:checked, QRadioButton::indicator:checked { background: #5865F2; border: 2px solid #5865F2; }
        
        QTreeWidget#tree { background-color: #2B2D31; border: none; outline: none; border-radius: 8px; padding: 5px; color: #DBDEE1; }
        QTreeWidget::item { padding: 4px; border-radius: 4px; color: #DBDEE1; }
        QTreeWidget::item:selected { background-color: #3F4147; color: white; }
        QHeaderView::section { background-color: #1E1F22; color: #949BA4; border: none; padding: 4px 8px; font-weight: bold; }
        
        QComboBox {
            background-color: transparent; color: #DBDEE1;
            border: 1px solid #4E5058; border-radius: 6px;
            padding: 4px 6px 4px 6px;
            combobox-popup: 0;
            outline: none;
        }
        QComboBox:hover { background-color: #3F4147; border: 1px solid #5865F2; }
        QComboBox:focus, QComboBox:on { border: 1px solid #5865F2; }
        QComboBox::drop-down {
            subcontrol-origin: padding; subcontrol-position: center right;
            width: 20px; border: none; background: transparent;
        }
        QComboBox::down-arrow { width: 12px; height: 12px; }
        QComboBox::down-arrow:on { top: 1px; }

        QComboBox QAbstractItemView {
            background-color: #2B2D31; color: #DBDEE1;
            border: 1px solid #4E5058; border-radius: 6px;
            padding: 4px; outline: none;
            selection-background-color: #5865F2; selection-color: #FFFFFF;
        }
        QComboBox QAbstractItemView::item {
            min-height: 26px; padding: 4px 10px;
            border: none; border-radius: 4px;
        }
        QComboBox QAbstractItemView::item:hover { background-color: #3F4147; color: #FFFFFF; }
        QComboBox QAbstractItemView::item:selected { background-color: #5865F2; color: #FFFFFF; }
        
        QLabel { color: #DBDEE1; }
        QLabel#status, QLabel#elide_label { color: #949BA4; }
        QLabel#stat_val { color: #23A559; font-weight: bold; }
        QLabel#player_time { color: #FFFFFF; font-weight: bold; }
        
        QSplitter::handle:horizontal { width: 1px; background-color: #2B2D31; }
        QSplitter::handle:vertical { height: 1px; background-color: #2B2D31; }
        QSplitter::handle:hover { background-color: #5865F2; }
        QSplitter::handle:pressed { background-color: #4752C4; }
        
        QScrollBar:vertical { background: transparent; width: 14px; margin: 0px; }
        QScrollBar::handle:vertical { background: #4E5058; min-height: 20px; border-radius: 7px; border: 3px solid #2B2D31; }
        QScrollBar::handle:vertical:hover { background: #949BA4; }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
        
        QScrollBar:horizontal { background: transparent; height: 14px; margin: 0px; }
        QScrollBar::handle:horizontal { background: #4E5058; min-width: 20px; border-radius: 7px; border: 3px solid #2B2D31; }
        QScrollBar::handle:horizontal:hover { background: #949BA4; }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: none; }
        QProgressBar { border: none; background-color: #1E1F22; border-radius: 2px; text-align: center; color: transparent; }
        QProgressBar::chunk { background-color: #5865F2; border-radius: 2px; }
        
        QSlider { background: transparent; height: 24px; }
        QSlider::groove:horizontal { border: none; height: 4px; background: #1E1F22; border-radius: 2px; }
        QSlider::sub-page:horizontal { background: #5865F2; border-radius: 2px; }
        QSlider::handle:horizontal { background: #FFFFFF; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; border: 1px solid #1E1F22; }
        QSlider::handle:horizontal:hover { background: #4D8BFF; }
        """
        app.setStyleSheet(cls._load_stylesheet("dark", qss) + cls._typography_qss())

    @classmethod
    def apply_modern_light(cls, app: QApplication):
        cls._active = cls.LIGHT
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(cls.LIGHT["bg"]))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(cls.LIGHT["text"]))
        palette.setColor(QPalette.ColorRole.Base, QColor(cls.LIGHT["surface"]))
        palette.setColor(QPalette.ColorRole.Text, QColor(cls.LIGHT["text"]))
        palette.setColor(QPalette.ColorRole.Button, QColor(cls.LIGHT["border"]))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(cls.LIGHT["text"]))
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(148, 155, 164))
        app.setPalette(palette)

        qss = """
        QMainWindow, QWidget#sidebar { background-color: #F2F3F5; }
        QWidget#card { background-color: #FFFFFF; border-radius: 8px; border: 1px solid #E3E5E8; }
        QWidget#toolbar_flat { background-color: #FFFFFF; border-radius: 6px; border: 1px solid #E3E5E8; }
        QWidget#controls_panel, QWidget#bottom_btns, QWidget#multi_slider_panel { background-color: #FFFFFF; border-top: 1px solid #E3E5E8; }
        QWidget#video_bg { background-color: #FFFFFF; }
        QFrame#divider { max-height: 1px; min-height: 1px; background-color: #E3E5E8; border: none; }
        
        QPushButton { 
            background-color: #E3E5E8; color: #313338; 
            border: none; border-radius: 6px; 
            padding: 6px 14px; font-weight: 500; 
            min-height: 24px;
        }
        QPushButton:hover { background-color: #D4D7DC; }
        QPushButton:pressed { background-color: #B5BAC1; }
        QPushButton:disabled { background-color: #E3E5E8; color: #949BA4; }
        
        QPushButton#primary { background-color: #23A559; color: white; font-weight: bold; }
        QPushButton#primary:hover { background-color: #1D8A4A; }
        QPushButton#action { background-color: #5865F2; color: white; }
        QPushButton#action:hover { background-color: #4752C4; }
        QPushButton#danger { background-color: #DA373C; color: white; font-weight: bold; }
        QPushButton#danger:hover { background-color: #A12828; }
        
        QPushButton#secondary { 
            background-color: transparent; 
            border: 1px solid #D4D7DC; 
            border-radius: 6px; 
            padding: 6px 14px; 
            color: #313338; 
            min-height: 24px;
        }
        QPushButton#secondary:hover { background-color: #E3E5E8; border: 1px solid #5865F2; }
        
        QPushButton#collapser { background-color: transparent; color: #5C5E66; padding: 4px 8px; }
        QPushButton#collapser:hover { background-color: #E3E5E8; color: #313338; }
        
        QPushButton#player_btn { background-color: transparent; color: #313338; font-weight: bold; padding: 0px; }
        QPushButton#player_btn:hover { color: #5865F2; }
        
        QLineEdit, QPlainTextEdit { 
            background-color: #FFFFFF; color: #313338; 
            border: 1px solid #D4D7DC; border-radius: 6px; 
            padding: 4px 10px; selection-background-color: #5865F2; selection-color: white;
        }
        QLineEdit:focus, QPlainTextEdit:focus { border: 1px solid #5865F2; }
        
        QLineEdit#spin_entry {
            border-radius: 0; border-left: none; border-right: none;
            padding: 4px;
        }
        QPushButton#spin_btn_left, QPushButton#spin_btn_right {
            background-color: #F2F3F5; border: 1px solid #D4D7DC; color: #313338;
            font-weight: bold; font-size: 14px; padding: 0; min-height: 24px;
        }
        QPushButton#spin_btn_left { border-top-right-radius: 0; border-bottom-right-radius: 0; border-right: none; }
        QPushButton#spin_btn_right { border-top-left-radius: 0; border-bottom-left-radius: 0; border-left: none; }
        QPushButton#spin_btn_left:hover, QPushButton#spin_btn_right:hover { background-color: #E3E5E8; }
        QPushButton#spin_btn_left:pressed, QPushButton#spin_btn_right:pressed { background-color: #D4D7DC; }
        
        QCheckBox { spacing: 8px; color: #313338; }
        QCheckBox::indicator, QRadioButton::indicator { width: 16px; height: 16px; border-radius: 4px; border: 2px solid #5865F2; background: transparent; }
        QRadioButton::indicator { border-radius: 8px; }
        QCheckBox::indicator:checked, QRadioButton::indicator:checked { background: #5865F2; border: 2px solid #5865F2; }
        
        QTreeWidget#tree { background-color: #FFFFFF; border: 1px solid #E3E5E8; outline: none; border-radius: 8px; padding: 5px; color: #313338; }
        QTreeWidget::item { padding: 4px; border-radius: 4px; color: #313338; }
        QTreeWidget::item:selected { background-color: #E3E5E8; color: #000000; }
        QHeaderView::section { background-color: #F2F3F5; color: #5C5E66; border: none; padding: 4px 8px; font-weight: bold; border-bottom: 1px solid #E3E5E8; }
        
        QComboBox {
            background-color: transparent; color: #313338;
            border: 1px solid #D4D7DC; border-radius: 6px;
            padding: 4px 6px 4px 6px;
            combobox-popup: 0;
            outline: none;
        }
        QComboBox:hover { background-color: #F2F3F5; border: 1px solid #5865F2; }
        QComboBox:focus, QComboBox:on { border: 1px solid #5865F2; }
        QComboBox::drop-down {
            subcontrol-origin: padding; subcontrol-position: center right;
            width: 20px; border: none; background: transparent;
        }
        QComboBox::down-arrow { width: 12px; height: 12px; }
        QComboBox::down-arrow:on { top: 1px; }

        QComboBox QAbstractItemView {
            background-color: #FFFFFF; color: #313338;
            border: 1px solid #D4D7DC; border-radius: 6px;
            padding: 4px; outline: none;
            selection-background-color: #5865F2; selection-color: #FFFFFF;
        }
        QComboBox QAbstractItemView::item {
            min-height: 26px; padding: 4px 10px;
            border: none; border-radius: 4px;
        }
        QComboBox QAbstractItemView::item:hover { background-color: #F2F3F5; color: #313338; }
        QComboBox QAbstractItemView::item:selected { background-color: #5865F2; color: #FFFFFF; }
        
        QLabel { color: #313338; }
        QLabel#status, QLabel#elide_label { color: #5C5E66; }
        QLabel#stat_val { color: #23A559; font-weight: bold; }
        QLabel#player_time { color: #313338; font-weight: bold; }
        
        QSplitter::handle:horizontal { width: 1px; background-color: #E3E5E8; }
        QSplitter::handle:vertical { height: 1px; background-color: #E3E5E8; }
        QSplitter::handle:hover { background-color: #5865F2; }
        QSplitter::handle:pressed { background-color: #4752C4; }
        
        QScrollBar:vertical { background: transparent; width: 14px; margin: 0px; }
        QScrollBar::handle:vertical { background: #D4D7DC; min-height: 20px; border-radius: 7px; border: 3px solid #FFFFFF; }
        QScrollBar::handle:vertical:hover { background: #949BA4; }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
        
        QScrollBar:horizontal { background: transparent; height: 14px; margin: 0px; }
        QScrollBar::handle:horizontal { background: #D4D7DC; min-width: 20px; border-radius: 7px; border: 3px solid #FFFFFF; }
        QScrollBar::handle:horizontal:hover { background: #949BA4; }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: none; }
        QProgressBar { border: none; background-color: #E3E5E8; border-radius: 2px; text-align: center; color: transparent; }
        QProgressBar::chunk { background-color: #5865F2; border-radius: 2px; }
        
        QSlider { background: transparent; height: 24px; }
        QSlider::groove:horizontal { border: none; height: 4px; background: #E3E5E8; border-radius: 2px; }
        QSlider::sub-page:horizontal { background: #5865F2; border-radius: 2px; }
        QSlider::handle:horizontal { background: #FFFFFF; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; border: 1px solid #D4D7DC; }
        QSlider::handle:horizontal:hover { background: #F2F3F5; }
        """
        app.setStyleSheet(cls._load_stylesheet("light", qss) + cls._typography_qss())

    @classmethod
    def apply_system_theme(cls, app: QApplication):
        # Определяем светлая или тёмная системная тема и применяем
        # соответствующий ПОЛНЫЙ набор стилей (а не только типографику),
        # иначе кнопки/карточки теряют оформление по objectName.
        app.setStyle("Fusion")
        window = app.style().standardPalette().color(QPalette.ColorRole.Window)
        if window.lightnessF() < 0.5:
            cls.apply_modern_dark(app)
        else:
            cls.apply_modern_light(app)
