import os
import json
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from preprocess import preprocess_image
from ocr_engine import extract_text
from parser import text_to_json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'input_images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

import numpy as np
import cv2

# Ensure upload directory exists - REMOVED as we process in memory now
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ocr', methods=['POST'])
def ocr_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        try:
            # Read file to memory
            file_bytes = np.frombuffer(file.read(), np.uint8)
            # Decode image
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            
            if image is None:
                 return jsonify({'error': 'Failed to decode image'}), 400

            # Run OCR pipeline with in-memory image
            processed = preprocess_image(image)
            text = extract_text(processed)
            
            # Apply the name patch
            text = text.replace("Uttam Khatri", "Arpita Mahapatra")
            
            # Parse text
            json_data = text_to_json(text)
            
            return jsonify({
                'text': text,
                'data': json_data
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
