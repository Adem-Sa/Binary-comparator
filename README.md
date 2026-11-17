# Binary Comparator

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41CD52?logo=qt&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)

A high-performance, multithreaded PyQt6 desktop utility engineered for analyzing and comparing raw binary files, firmware images, and ECU calibration dumps (`.bin`, `.ori`, `.mod`, `.hex`, `.eep`, `.mpc`, `.fls`) side-by-side.

---

## Key Features

- **Non-Blocking Asynchronous Engine (`QThread`)**: Performs byte-by-byte binary analysis using `memoryview` in a dedicated worker thread with real-time progress feedback—zero UI freezes even on large dumps.
- **Unlimited Progressive Block Streaming**: Streams 100% of modified byte blocks into `QPlainTextEdit` via timed batch rendering (`QTimer`), preserving smooth scrolling regardless of diff density.
- **Native Syntax-Highlighted Hex Inspector (`QSyntaxHighlighter`)**: Highlights modified bytes in coral red (Original) and cyan/green (Modified) with synchronized vertical and horizontal scrolling.
- **Complete Audit Report Export**: Exports full file metadata, similarity metrics, and every aligned hexadecimal diff block to a clean `.txt` report.
- **5-Language Localization**: Instant runtime switching between **English (`EN`)**, **French (`FR`)**, **Arabic (`AR`)**, **Russian (`RU`)**, and **Chinese (`ZH`)** while preserving strict Left-to-Right alignment in the hex views.

---

## Project Structure

```text
Binary-comparator/
├── main.py          # Application entry point
├── ui_main.py       # PyQt6 main window, QThread worker, batch renderer & QSyntaxHighlighter
├── engine.py        # High-speed memoryview binary comparison core
├── style.qss        # Dark mode QSS stylesheet
├── app_icon.png     # Application window & executable icon
└── README.md        # Project documentation
