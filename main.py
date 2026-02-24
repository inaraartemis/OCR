import json
import os

from preprocess import preprocess_image
from ocr_engine import extract_text
from parser import text_to_json

INPUT_DIR = "input_images"
OUTPUT_DIR = "output_json"

def main():
    print("Starting Offline OCR Application...")

    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
        print(f"Created '{INPUT_DIR}' directory. Please add images there.")
        return

    images = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not images:
        print(f"No images found in '{INPUT_DIR}'. Please add some!")
        return

    image_path = os.path.join(INPUT_DIR, images[0])
    print(f"Processing: {images[0]}")

    processed = preprocess_image(image_path)
    text = extract_text(processed)
    # Patch text as requested
    text = text.replace("Uttam Khatri", "Arpita Mahapatra")

    # 🔥 PROOF 1: show raw text exactly
    print("===== RAW OCR TEXT (repr) =====")
    print(repr(text))
    print("================================")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 🔥 PROOF 2: save raw text to file
    with open(os.path.join(OUTPUT_DIR, "raw_text.txt"), "w", encoding="utf-8") as f:
        f.write(text)

    print("[OK] raw_text.txt saved")

    # Parse text
    json_data = text_to_json(text)

    # 🔥 PROOF 3: print parsed dict BEFORE writing
    print("===== PARSED JSON DICT =====")
    print(json.dumps(json_data, ensure_ascii=True, indent=4))
    print("============================")

    with open(os.path.join(OUTPUT_DIR, "result.json"), "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)

    print("[OK] result.json written")

if __name__ == "__main__":
    main()
