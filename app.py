from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os, PyPDF2, pytesseract, spacy, logging
from PIL import Image
from collections import Counter
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration - Professional Pathing
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config.update(
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    MAX_CONTENT_LENGTH=16 * 1024 * 1024
)

# Tesseract Configuration
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load NLP Model once
try:
    nlp = spacy.load('en_core_web_sm')
except Exception as e:
    print(f"Error: Run 'python -m spacy download en_core_web_sm'")

def extract_text(filepath):
    """Unified extraction logic"""
    ext = filepath.lower().split('.')[-1]
    text = ""
    if ext == 'pdf':
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = "\n".join([page.extract_text() for page in reader.pages])
    else:
        text = pytesseract.image_to_string(Image.open(filepath))
    return text

def summarize_text(text, max_sentences=3):
    if not text.strip(): return "No text found."
    doc = nlp(text)
    keywords = [t.text.lower() for t in doc if not t.is_stop and not t.is_punct and t.pos_ in ['NOUN', 'VERB']]
    freq = Counter(keywords)
    m = max(freq.values()) if freq else 1
    scores = {s: sum(freq.get(w.text.lower(), 0)/m for w in s) for s in doc.sents}
    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:max_sentences]
    return " ".join([s[0].text for s in top])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        file = request.files.get('file')
        if not file: return jsonify({'error': 'No file uploaded'}), 400
        
        path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(path)
        
        text = extract_text(path)
        summary = summarize_text(text)
        
        os.remove(path) # Cleanup
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)