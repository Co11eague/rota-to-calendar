import cv2
import numpy as np

def deskew_image(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Detect lines in the image using Hough Line Transform
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)

    # If no lines are detected, return original image
    if lines is None:
        return image

    # Find the angle of the most dominant line
    angles = [np.rad2deg(line[0][1]) for line in lines]
    median_angle = np.median(angles)  # The most common angle (median)

    # Calculate the rotation matrix and apply the transformation
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, median_angle, 1.0)

    # Compute the bounding box of the rotated image to ensure all pixels are retained
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])

    # New width and height
    new_w = int(h * sin + w * cos)
    new_h = int(h * cos + w * sin)

    # Adjust the rotation matrix to account for the translation
    rotation_matrix[0, 2] += (new_w / 2) - center[0]
    rotation_matrix[1, 2] += (new_h / 2) - center[1]

    # Perform the rotation and ensure that the whole image is included
    deskewed_image = cv2.warpAffine(image, rotation_matrix, (new_w, new_h), flags=cv2.INTER_CUBIC)

    return deskewed_image

def split_table_into_matrix(image_path):
    # Load the image
    image = cv2.imread(image_path)

    image = deskew_image(image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold to binary image
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    # Detect horizontal and vertical lines
    kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 1))  # Horizontal kernel
    kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 30))  # Vertical kernel
    horizontal = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_h)
    vertical = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_v)

    # Combine horizontal and vertical lines to detect table grid
    grid = cv2.bitwise_or(horizontal, vertical)

    # Find contours of the grid
    contours, _ = cv2.findContours(grid, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours to maintain order
    bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]
    sorted_boxes = sorted(bounding_boxes, key=lambda b: (b[1], b[0]))  # Sort by y, then x

    # Create a matrix of cells
    table_matrix = []
    current_row = []
    last_y = -1

    for box in sorted_boxes:
        x, y, w, h = box

        # Ignore very small boxes (noise)
        if w < 10 or h < 10:
            continue

        # New row detected
        if last_y != -1 and abs(y - last_y) > 20:  # Tolerance for row separation
            table_matrix.append(current_row)
            current_row = []

        # Extract the cell as an image (submatrix)
        cell = image[y:y + h, x:x + w]
        current_row.append(cell)
        last_y = y

    # Add the last row
    if current_row:
        table_matrix.append(current_row)

    return table_matrix
