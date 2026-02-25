import cv2
import numpy as np

def deskew_image(image):
    """Detects text tilt and rotates the image to align it horizontally."""
    # Convert to grayscale if not already
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Threshold to find text
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Find all peak pixels
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    # Handle angle rotation
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # Rotate the image
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated

def apply_clahe(image):
    """Applies Contrast Limited Adaptive Histogram Equalization."""
    # Convert to LAB color space to handle luminosity independently
    if len(image.shape) == 3:
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    else:
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        return clahe.apply(image)

def sharpen_image(image):
    """Enhances character boundaries using a sharpening kernel."""
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    return cv2.filter2D(image, -1, kernel)

def preprocess_image(image_input, deskew=False, clahe=False, sharpen=False):
    # Read image if path string
    if isinstance(image_input, str):
        image = cv2.imread(image_input)
    elif isinstance(image_input, np.ndarray):
        image = image_input  # Already an image array
    else:
        raise ValueError("Input must be a file path string or a numpy array")

    if image is None:
        raise ValueError("Image not found or invalid image data")

    # Optional: Deskewing
    if deskew:
        image = deskew_image(image)

    # Optional: CLAHE
    if clahe:
        image = apply_clahe(image)

    # Optional: Sharpening
    if sharpen:
        image = sharpen_image(image)

    # 1. Resize algorithm (Scale up)
    h, w = image.shape[:2]
    if w < 1000:
        scale = 2
        image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # 2. Convert to grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # 3. Smart Inversion
    mean_brightness = np.mean(gray)
    if mean_brightness < 127:
        gray = 255 - gray

    # 4. Denoise
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)

    # 5. Adaptive Thresholding
    processed = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 2
    )

    return processed, image # Return both processed and original/filtered for display
