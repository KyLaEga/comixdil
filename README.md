# 📚 Universal Comic Downloader

A powerful GUI application for downloading comics from various websites and converting between PDF and CBZ formats.

![Version](https://img.shields.io/badge/version-2.7.0-blue)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

> ⚠️ **Note**: The application interface is in **Russian**. However, the icons and layout are intuitive, making it easy to use regardless of language.

---

## ✨ Features

- 🌐 **Universal Parser** - Download comics from any website (Telegraph, SexKomix2, and more)
- 🔄 **Format Converter** - Convert between PDF and CBZ formats
- 📚 **Library Management** - Organize your comic collection with search and filters
- 👁️ **Built-in Viewer** - Preview comics directly in the app
- ⌨️ **Keyboard Shortcuts** - Full keyboard support (Ctrl/Cmd+C, V, A, Delete)
- 🎨 **Modern UI** - Clean, monochrome design

---

## 🚀 Quick Start

### macOS

```bash
# Extract
tar -xzf universal_comic_downloader_v2.7.0.tar.gz
cd telegraph_comic_downloader_gui

# Option 1: Run directly
./launch_macos.command

# Option 2: Create .app bundle
./create_simple_app.sh
cp -r "dist/Universal Comic Downloader.app" /Applications/
```

### Windows

```batch
cd telegraph_comic_downloader_gui
launch_windows.bat

:: Or build .exe
build_windows_exe.bat
```

### Linux

```bash
cd telegraph_comic_downloader_gui
./launch_linux.sh

# Or build AppImage
./build_linux_appimage.sh
```

---

## 📋 Requirements

- **Python 3.11+**
- **Tkinter** (usually included with Python)
- **Dependencies** (installed automatically):
  - requests
  - beautifulsoup4
  - Pillow
  - pdf2image (for PDF→CBZ conversion)

### Additional for PDF conversion:

| Platform | Command |
|----------|---------|
| **macOS** | `brew install poppler` |
| **Linux** | `sudo apt install poppler-utils` |
| **Windows** | Download [Poppler](https://github.com/oschwartz10612/poppler-windows/releases) |

---

## 🎮 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl/Cmd + V` | Paste URL |
| `Ctrl/Cmd + C` | Copy |
| `Ctrl/Cmd + A` | Select All |
| `Delete` | Remove selected |
| `Enter` | Add to queue |

---

## 🌐 Supported Websites

- ✅ Telegraph (telegra.ph)
- ✅ SexKomix2 (sexkomix2.com)
- ✅ Any website with comic images (universal parser)

---

## 📁 Project Structure

```
telegraph_comic_downloader_gui/
├── main.py                 # Entry point
├── core/
│   ├── downloader.py       # Universal image parser
│   ├── converter.py        # PDF ↔ CBZ converter
│   └── database.py         # SQLite library
├── gui/
│   ├── main_window.py      # Main application window
│   ├── converter_dialog.py # Converter dialog
│   └── comic_viewer.py     # Built-in viewer
└── utils/
    └── helpers.py          # Utility functions
```

---

## 🔧 Building Standalone Apps

| Platform | Command | Output |
|----------|---------|--------|
| **macOS** | `./create_simple_app.sh` | `.app` bundle |
| **macOS** | `./build_macos_app.sh` | Standalone `.app` |
| **Windows** | `build_windows_exe.bat` | `.exe` file |
| **Linux** | `./build_linux_appimage.sh` | `.AppImage` |

---

## 📖 Documentation

- [README (Russian)](README_RU.md) - Подробная документация на русском
- [Keyboard Shortcuts](KEYBOARD_SHORTCUTS.md)
- [macOS Build Guide](BUILD_MACOS_APP.md)
- [Windows Build Guide](WINDOWS_BUILD_GUIDE.md)
- [Linux Build Guide](LINUX_BUILD_GUIDE.md)

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Add translations

---

## 📄 License

MIT License - feel free to use, modify, and distribute.

---

**Made with ❤️ for comic lovers**
