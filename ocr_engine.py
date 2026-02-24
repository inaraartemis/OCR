import pytesseract
from PIL import Image
import os

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if not os.path.exists(TESSERACT_PATH):
    raise RuntimeError(
        "Tesseract OCR is not installed.\n"
        "Please install it from https://github.com/UB-Mannheim/tesseract/wiki"
    )

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def extract_text(processed_image):
    return pytesseract.image_to_string(
        Image.fromarray(processed_image),
        lang="eng",
        config="--psm 6"
    )
