# 📚 comixdil

A lightweight desktop app for downloading comics & manga from almost any website and packing them into **PDF** or **CBZ**.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

> ⚠️ **Note**: The interface is in **Russian**, but the layout and icons are intuitive and easy to use regardless of language.

---

## ✨ Features

- 🌐 **Universal downloader** — powered by [`gallery-dl`](https://github.com/mikf/gallery-dl) with built-in fallback parsers for `telegra.ph`, SexKomix and any page that contains comic images
- 📦 **PDF & CBZ export** — assemble pages into a PDF (`img2pdf`) or a CBZ archive, with adjustable JPEG quality
- 🧠 **RAM-friendly** — pages are streamed to a temp folder on disk instead of being kept in memory, so large galleries don't eat your RAM
- 🧵 **Multithreaded + rate limiting** — parallel downloads with a configurable delay and automatic back-off on `503` errors
- ⏯️ **Queue control** — add many links at once, pause/resume, cancel, and clear finished tasks
- 🎨 **Themes** — dark, light and system, built on a modern PySide6 UI

---

## 🚀 Quick Start

```bash
git clone https://github.com/KyLaEga/comixdil.git
cd comixdil

pip install -r requirements.txt
python main.py
```

Requires **Python 3.11+**. Dependencies (`requests`, `beautifulsoup4`, `Pillow`, `PySide6`, `gallery-dl`, `img2pdf`) are installed from `requirements.txt`.

---

## 📋 Usage

1. Paste one or more links into the input box (**one per line**).
2. Pick the format (**PDF** or **CBZ**) and the output folder in the sidebar.
3. Click **«Скачать»** (Download) — the app finds the images and assembles the file.

**Tip:** tune *Комиксов* (parallel comics), *Потоков* (threads per comic) and *Задержка* (request delay) in the sidebar. Higher load = faster, but raises the risk of `503` blocks. Select queue items and press `Delete` to remove them.

---

## 🌐 Supported sites

- ✅ Telegraph (`telegra.ph`)
- ✅ SexKomix and similar galleries
- ✅ Everything `gallery-dl` supports (Hitomi, nHentai, and many more)
- ✅ Generic fallback — any page with comic images

---

## 📁 Project structure

```
comixdil/
├── main.py              # Entry point (Qt app bootstrap)
├── core/
│   └── downloader.py    # Universal downloader: parsers, fetching, PDF/CBZ export
├── gui/
│   ├── main_window.py   # Main window, settings sidebar, download queue
│   └── theme.py         # Theme manager (dark / light / system) + icons
└── requirements.txt
```

---

## 📖 Documentation

- [README (Russian)](README_RU.md) — документация на русском

---

## 📄 License

MIT License — feel free to use, modify, and distribute.

---

**Made with ❤️ for comic lovers**
