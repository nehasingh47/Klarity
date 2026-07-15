# Klarity

A document summarization tool that extracts key sentences from PDFs and scanned images using NLP.

## Overview

Klarity takes a PDF or image (PNG/JPEG) and returns a short extractive summary - the most information-dense sentences from the document, picked out using word-frequency scoring over nouns and verbs. Upload a document, get the core content back in seconds, no full read-through required.

## How it works

1. **Text extraction**
   - PDFs: parsed directly with PyPDF2
   - Images: run through Tesseract OCR (pytesseract) to extract text
2. **Summarization**
   - The extracted text is processed with spaCy (`en_core_web_sm`)
   - Non-stopword nouns and verbs are frequency-scored
   - Each sentence is scored by the sum of its words' frequency weights
   - The top-scoring sentences (default: 3) are returned as the summary

This is a lightweight, explainable **extractive** approach - it selects and returns real sentences from the source text, rather than generating new text.

## Tech Stack

**Backend:** Python, Flask, Flask-CORS
**NLP:** spaCy (`en_core_web_sm`)
**Document parsing:** PyPDF2 (PDF), pytesseract + Pillow (OCR for images)
**Frontend:** HTML, Tailwind CSS (CDN), vanilla JavaScript
**Export:** jsPDF (client-side PDF generation for saving summaries)

## Getting Started

### Prerequisites
- Python 3.7+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed locally (required for image-based summarization)

### Installation

```bash
git clone https://github.com/nehasingh47/Klarity.git
cd Klarity
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

> **Note:** `app.py` currently points to a hardcoded Tesseract path (`C:\Program Files\Tesseract-OCR\tesseract.exe`). If you're not on Windows, or installed Tesseract elsewhere, update the `pytesseract.pytesseract.tesseract_cmd` line in `app.py` to match your install path.

### Running

```bash
python app.py
```

Then open `http://localhost:5000` in your browser.

## Usage

1. Drop a PDF or image onto the upload zone (or click to browse)
2. Klarity extracts the text and generates a summary
3. Copy the summary or export it as a PDF

## Project Structure

```
Klarity/
├── app.py              # Flask app — text extraction + summarization logic
├── templates/
│   └── index.html      # Upload UI and result view
├── static/              # (if applicable) CSS/JS assets
├── requirements.txt     # Python dependencies
└── README.md
```

## Known limitations

- Summary length is fixed at 3 sentences by default (not yet user-configurable in the UI)
- OCR accuracy depends on image quality scanned or low-res documents may summarize poorly
- Tesseract path is currently hardcoded for local development

## Roadmap

- Make summary length adjustable from the UI
- Cross-platform Tesseract path handling
- Support for DOCX input

## Author

[nehasingh47](https://github.com/nehasingh47)
