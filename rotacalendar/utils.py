import cv2
import numpy as np


def deskew_image(image):
	# Convert to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Apply edge detection
	edges = cv2.Canny(gray, 50, 150)

	# Find contours in the edge-detected image
	contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# Find the largest rectangular contour (outer table border)
	largest_contour = max(contours, key=cv2.contourArea, default=None)

	if largest_contour is None:
		print("No table detected.")
		return image  # Return original if no table is found

	# Approximate contour to a polygon
	epsilon = 0.02 * cv2.arcLength(largest_contour, True)
	approx = cv2.approxPolyDP(largest_contour, epsilon, True)

	if len(approx) != 4:
		print("Couldn't find a proper quadrilateral.")
		return image

	# Order the corner points (top-left, top-right, bottom-right, bottom-left)
	approx = sorted(approx[:, 0], key=lambda p: (p[1], p[0]))  # Sort by y first, then x
	top_left, top_right = sorted(approx[:2], key=lambda p: p[0])
	bottom_left, bottom_right = sorted(approx[2:], key=lambda p: p[0])

	# Define the destination points for a straightened rectangle
	width = max(
		np.linalg.norm(top_right - top_left),
		np.linalg.norm(bottom_right - bottom_left)
	)
	height = max(
		np.linalg.norm(bottom_left - top_left),
		np.linalg.norm(bottom_right - top_right)
	)

	dst_pts = np.array([
		[0, 0],
		[width - 1, 0],
		[width - 1, height - 1],
		[0, height - 1]
	], dtype="float32")

	# Compute the perspective transform matrix
	src_pts = np.array([top_left, top_right, bottom_right, bottom_left], dtype="float32")
	M = cv2.getPerspectiveTransform(src_pts, dst_pts)

	# Warp the image to get a straightened table
	straightened = cv2.warpPerspective(image, M, (int(width), int(height)))

	return straightened


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
	cell_matrix = []
	row = []
	threshold = 10  # Adjust for row separation tolerance
	prev_y = None
	sorted_boxes = sorted(filtered_boxes, key=lambda b: (b[1], b[0]))

	# Extract cells into a list
	margin = 5  # Add padding
	for x, y, w, h in sorted_boxes:
		cropped_cell = inpainted_image[
		               max(0, y + margin):min(image.shape[0], y + h - margin),
		               max(0, x + margin):min(image.shape[1], x + w - margin)
		               ]

		if prev_y is not None and abs(y - prev_y) > threshold:
			# Start a new row
			cell_matrix.append(row)
			row = []

		row.append(cropped_cell)
		prev_y = y

	if row:
		cell_matrix.append(row)

	return cell_matrix
