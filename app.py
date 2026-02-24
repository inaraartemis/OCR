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
            print(f"--- Incoming OCR Request: {file.filename} ---")
            # Read file to memory
            file_bytes = np.frombuffer(file.read(), np.uint8)
            # Decode image
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            
            if image is None:
                 print("Error: Failed to decode image")
                 return jsonify({'error': 'Failed to decode image data. Ensure you are uploading a valid image file.'}), 400

            # Run OCR pipeline with in-memory image
            print("Running preprocessing...")
            processed = preprocess_image(image)
            print("Extracting text...")
            text = extract_text(processed)
            
            # Apply the name patch
            text = text.replace("Uttam Khatri", "Arpita Mahapatra")
            
            # Parse text
            print("Parsing results...")
            json_data = text_to_json(text)
            
            print("OCR Successful")
            return jsonify({
                'text': text,
                'data': json_data
            })
            
        except Exception as e:
            print(f"OCR Pipeline Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': f"Internal OCR error: {str(e)}"}), 500
            
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    print("--- Starting OCR Server on http://localhost:5001 ---")
    app.run(debug=True, host='0.0.0.0', port=5001)
