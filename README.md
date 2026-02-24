# 📸 Extractor de Imágenes — Offline OCR Application

> A fully **offline** OCR (Optical Character Recognition) application that extracts text from images using **Tesseract OCR** — no internet connection required.

---

## ✨ Features

- 🔒 **100% Offline** — All processing happens locally on your machine. No data is sent to any cloud or external API.
- 🖼️ **Image Preprocessing** — Automatic grayscale conversion, smart inversion, denoising, and adaptive thresholding for maximum accuracy.
- 🌐 **Web Interface** — Beautiful drag-and-drop UI built with Flask for easy image uploads.
- 💻 **CLI Mode** — Run OCR directly from the command line for batch or scripted workflows.
- 📋 **Structured Output** — Results available as both raw text and structured JSON.
- 📥 **Download & Copy** — One-click copy-to-clipboard and download buttons (JSON / TXT).
- 📂 **In-Memory Processing** — Images are processed in memory without being saved to disk (web mode).

---

## 🛠️ Tech Stack

| Component       | Technology                     |
|-----------------|--------------------------------|
| OCR Engine      | Tesseract OCR (via pytesseract)|
| Image Processing| OpenCV, Pillow                 |
| Web Framework   | Flask                          |
| Frontend        | HTML, CSS, Vanilla JavaScript  |
| Language        | Python 3.x                     |

---

## 📁 Project Structure

```
OCRapp/
├── app.py              # Flask web server (Web UI mode)
├── main.py             # CLI entry point (Command-line mode)
├── preprocess.py       # Image preprocessing pipeline
├── ocr_engine.py       # Tesseract OCR wrapper
├── parser.py           # Text-to-JSON parser
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Web UI frontend
├── input_images/       # Place images here for CLI mode
└── output_json/        # CLI mode output directory
```

---

## 🚀 Getting Started

### Prerequisites

1. **Python 3.8+** — [Download Python](https://www.python.org/downloads/)
2. **Tesseract OCR** — Must be installed separately:
   - **Windows**: Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt install tesseract-ocr`

> [!NOTE]
> On Windows, Tesseract must be installed at `C:\Program Files\Tesseract-OCR\tesseract.exe` (default path).

### Installation

```bash
# Clone the repository
git clone https://github.com/inaraartemis/OCR.git
cd OCR

# Install Python dependencies
pip install -r requirements.txt
```

---

## 🖥️ Usage

### Option 1: Web Interface (Recommended)

```bash
python app.py
```

Then open your browser and go to **http://localhost:5000**

1. Drag & drop an image (or click to browse)
2. Click **"Extract Text"**
3. View results as **Structured JSON** or **Raw Text**
4. Copy to clipboard or download the results

### Option 2: Command Line

```bash
# Place your image(s) in the input_images/ folder, then run:
python main.py
```

Output will be saved to `output_json/`:
- `raw_text.txt` — Extracted raw text
- `result.json` — Structured JSON output

---

## ⚙️ How It Works

```
Image Input → Preprocessing → OCR Engine → Text Parsing → Output
```

1. **Preprocessing** (`preprocess.py`)
   - Upscales small images for better recognition
   - Converts to grayscale
   - Smart inversion (handles dark backgrounds)
   - Bilateral denoising (preserves edges)
   - Adaptive thresholding for clean binary output

2. **OCR Engine** (`ocr_engine.py`)
   - Uses Tesseract with `--psm 6` (uniform block of text)
   - Extracts English text from the preprocessed image

3. **Parser** (`parser.py`)
   - Converts raw OCR text into structured JSON (line-by-line)

---

## 🌐 Online or Offline?

| Aspect              | Status      |
|---------------------|-------------|
| OCR Processing      | ✅ Offline  |
| Image Preprocessing | ✅ Offline  |
| Web UI (Flask)      | ✅ Offline (localhost only) |
| External API Calls  | ❌ None     |
| Internet Required   | ❌ No       |

**This application is fully offline.** It uses Tesseract OCR installed locally on your machine. No images or data are sent to any external server. The web interface runs on `localhost` (your own computer) and does not require internet access.

---

## 📝 Supported File Types

- `.png`
- `.jpg` / `.jpeg`
- Max upload size: **16 MB**

---

## 📄 License

This project is for educational / class project purposes.

---

## 👩‍💻 Author

**Arpita Mahapatra**
