import cv2
import numpy as np

def deskew_image(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Detect lines in the image using Hough Line Transform
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)

    # If no lines are detected, return the original image
    if lines is None:
        return image

    # Find the angle of the most dominant line
    angles = [np.rad2deg(line[0][1]) for line in lines]
    median_angle = np.median(angles)  # The most common angle (median)

    # If the median angle is close to horizontal or vertical (within a tolerance), skip rotation
    tolerance = 1.0  # Adjust this value for sensitivity
    if -tolerance < median_angle < tolerance or 90 - tolerance < median_angle < 90 + tolerance:
        return image

    # Optionally log or return the median angle for analysis instead of rotating
    print(f"Detected skew angle: {median_angle} degrees (skipping rotation)")

    return image

def split_table_into_list(image_path):
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

    # Create a 1D list of cells
    cell_list = []

    for box in sorted_boxes:
        x, y, w, h = box

        # Ignore very small boxes (noise)
        if w < 10 or h < 10:
            continue

        # Extract the cell as an image (submatrix)
        cell = image[y:y + h, x:x + w]
        cell_list.append(cell)

    return cell_list
