import os

import cv2
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render

from rotacalendar import settings
from rotacalendar.utils import split_table_into_matrix

@login_required
def index(request):
	return render(request, 'conversion/index.html')


@login_required
def process_table_image(request):
    if request.method == 'POST' and 'table_image' in request.FILES:

        uploaded_image = request.FILES['table_image']

        # Save the uploaded image temporarily using FileSystemStorage
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)  # Adjust the location if needed
        filename = fs.save(uploaded_image.name, uploaded_image)

        # Generate the full path to the saved file on the local filesystem
        saved_image_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Read the saved image using OpenCV
        image = cv2.imread(saved_image_path)

        # Ensure the image is loaded properly
        if image is None:
            fs.delete(filename)  # Delete the uploaded file if failed to load
            return JsonResponse({"error": "Failed to load image. Please try again with a valid file."}, status=400)

        # Process the table into a matrix (assuming you have a function for this)
        table_matrix = split_table_into_matrix(saved_image_path)

        # Save each cell image using FileSystemStorage
        saved_image_urls = []
        for i, row in enumerate(table_matrix):
            row_urls = []
            for j, cell in enumerate(row):
                cell_filename = f"cell_{i}_{j}.png"
                cell_path = os.path.join('temp_images', cell_filename)  # Saving inside 'temp_images' folder

                # Convert the cell image to bytes and save it using fs
                # To save the image to FileSystemStorage, we need to write it to a temporary file first
                temp_img_path = os.path.join(settings.MEDIA_ROOT, cell_path)
                cv2.imwrite(temp_img_path, cell)

                # Save the image using FileSystemStorage
                cell_file = fs.save(cell_path, open(temp_img_path, 'rb'))

                # Get the URL for this image using fs.url() and store it in the row list
                row_urls.append(fs.url(cell_file))

                # Clean up the temporary image file
                os.remove(temp_img_path)

            # Append the entire row URLs to the main list (will maintain row order)
            saved_image_urls.append(row_urls)

        # Optionally delete the original uploaded image if no longer needed
        fs.delete(filename)

        # Return the image URLs for rendering
        return render(request, 'conversion/show_split_images.html', {'image_urls': saved_image_urls})

    return JsonResponse({"error": "Invalid request"}, status=400)
# Create your views here.
