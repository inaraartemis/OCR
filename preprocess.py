import cv2
import numpy as np

def preprocess_image(image_input):
    # Read image if path string
    if isinstance(image_input, str):
        image = cv2.imread(image_input)
    elif isinstance(image_input, np.ndarray):
        image = image_input  # Already an image array
    else:
        raise ValueError("Input must be a file path string or a numpy array")

    if image is None:
        raise ValueError("Image not found or invalid image data")

    # 1. Resize algorithm (Scale up)
    # Tesseract works best with images ~300 DPI. Scaling up small images helps.
    h, w = image.shape[:2]
    if w < 1000:
        scale = 2
        image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # 2. Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 3. Smart Inversion (Ensure dark text on light background)
    # Calculate mean brightness. If low (< 127), assume dark background and invert.
    mean_brightness = np.mean(gray)
    if mean_brightness < 127:
        gray = 255 - gray  # Invert to get light background

    # 4. Denoise (Bilateral is better than Gaussian for edges)
    # preserve edges while blurring flat areas
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)

    # 5. Adaptive Thresholding
    # Better for varying lighting conditions than global Otsu
    processed = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 2
    )

    # Optional: Dilation to thicken text if it's too thin
    # kernel = np.ones((1, 1), np.uint8)
    # processed = cv2.dilate(processed, kernel, iterations=1)

    return processed
