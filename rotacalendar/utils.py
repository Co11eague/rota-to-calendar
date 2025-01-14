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

	# Deskew the image
	image = deskew_image(image)

	# Convert to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Threshold to binary image
	binary = cv2.adaptiveThreshold(
		gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 5
	)

	# Detect horizontal and vertical lines
	kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 1))  # Horizontal kernel
	kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 30))  # Vertical kernel
	horizontal = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_h)
	vertical = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_v)

	# Combine horizontal and vertical lines to detect the table grid
	grid_dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
	binary = cv2.dilate(binary, grid_dilate_kernel, iterations=1)

	grid = cv2.bitwise_or(horizontal, vertical)

	# Inpaint the grid lines
	inpainted_image = cv2.inpaint(image, grid, 3, cv2.INPAINT_TELEA)

	# Find contours in the grid
	contours, _ = cv2.findContours(grid, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# Create a list of bounding boxes for contours
	bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]

	# Define maximum and minimum expected cell sizes
	min_cell_size = (10, 10)  # Minimum width and height
	max_cell_size = (gray.shape[1] // 3, gray.shape[0] // 5)  # Maximum width and height

	# Filter bounding boxes by size
	filtered_boxes = [
		box
		for box in bounding_boxes
		if min_cell_size[0] < box[2] < max_cell_size[0] and min_cell_size[1] < box[3] < max_cell_size[1]
	]

	# Sort bounding boxes (by y, then x)
	sorted_boxes = sorted(filtered_boxes, key=lambda b: (b[1], b[0]))

	# Extract cells into a list
	cell_list = []
	margin = 5  # Add padding
	for x, y, w, h in sorted_boxes:
		cropped_cell = inpainted_image[
		               max(0, y + margin):min(image.shape[0], y + h - margin),
		               max(0, x + margin):min(image.shape[1], x + w - margin)
		               ]
		cell_list.append(cropped_cell)

	return cell_list
