import os

import cv2
import numpy as np
import torch
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render

from conversion.model import Model
from conversion.utils import AttnLabelConverter
from rotacalendar import settings
from rotacalendar.utils import split_table_into_list
from PIL import Image, ImageOps

# Initialize your model outside of the view to avoid reloading on every request
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')



def load_model():
    """Load the pretrained model once and return it."""
    model_storage_directory = os.path.join(settings.BASE_DIR, 'custom_model/TPS-ResNet-BiLSTM-Attn.pth')

    opt = type('', (), {})()  # Empty object for options, simulate argparse arguments
    opt.imgH = 32
    opt.imgW = 80
    opt.batch_max_length = 5000
    opt.character = '0123456789abcdefghijklmnopqrstuvwxyz -:|()'  # Adjust your character set
    opt.saved_model = model_storage_directory
    opt.Prediction = 'Attn'
    opt.Transformation = 'TPS'
    opt.FeatureExtraction = 'ResNet'
    opt.SequenceModeling = 'BiLSTM'
    opt.num_fiducial = 20
    opt.input_channel = 1
    opt.output_channel = 512
    opt.hidden_size = 256
    opt.num_class = 44


    # Load model
    model = Model(opt).to(device)
    model.load_state_dict(torch.load(opt.saved_model, map_location=device))
    model.eval()  # Set model to evaluation mode
    return model


# Load model once
model = load_model()


def preprocess_image(image, save_path=None):
    """ Convert image to tensor, resize it for model compatibility, and ensure single channel """
    # Convert image to grayscale (1 channel)
    image = image.convert('L')  # 'L' mode means grayscale

    # Calculate padding if the image is smaller than the required size
    target_height = 32
    target_width = 80

    width, height = image.size

    # Calculate padding for width and height
    padding_left = max(0, (target_width - width) // 2)
    padding_right = max(0, target_width - width - padding_left)
    padding_top = max(0, (target_height - height) // 2)
    padding_bottom = max(0, target_height - height - padding_top)

    # Apply padding
    image = ImageOps.expand(image, (padding_left, padding_top, padding_right, padding_bottom),
                            fill=0)  # padding with black (0)

    # Resize to the model's required input size if necessary (if the image wasn't already the target size)
    image = image.resize((target_width, target_height))

    # If save path is provided, save the preprocessed image
    if save_path:
        image.save(save_path)

    # Convert the padded and resized image to a numpy array and normalize
    image = np.array(image).astype(np.float32) / 255.0  # Normalize the pixel values to [0, 1]

    # Convert to tensor and add the batch and channel dimensions
    image = torch.tensor(image).unsqueeze(0).unsqueeze(0)  # [1, 1, 32, 80]

    print("Preprocessed image saved at:", save_path)

    return image


def run_ocr_on_image(image):
    """Run OCR model inference on an image."""
    image_tensor = preprocess_image(image).to(device)
    text_for_pred = torch.LongTensor(1, 5000 + 1).fill_(0).to(device)  # Empty text input for prediction
    preds = model(image_tensor, text_for_pred)  # Run inference
    preds_size = torch.IntTensor([preds.size(1)] * 1).to(device)  # Get prediction size
    _, preds_index = preds.max(2)  # Get the max probability indexes

    # Decode prediction
    converter = AttnLabelConverter('0123456789abcdefghijklmnopqrstuvwxyz -:|()')  # Adjust if needed
    preds_str = converter.decode(preds_index, preds_size)

    return preds_str[0]  # Return the predicted text


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
        table_list = split_table_into_list(saved_image_path)

        # Save each cell image using FileSystemStorage
        saved_image_urls = []
        for i, image in enumerate(table_list):
            cell_filename = f"cell_{i}.png"
            cell_path = os.path.join('temp_images', cell_filename)  # Saving inside 'temp_images' folder

            # Convert the cell image to bytes and save it using fs
                # To save the image to FileSystemStorage, we need to write it to a temporary file first
            temp_img_path = os.path.join(settings.MEDIA_ROOT, cell_path)
            cv2.imwrite(temp_img_path, image)

                # Save the image using FileSystemStorage
            cell_file = fs.save(cell_path, open(temp_img_path, 'rb'))

                # Get the URL for this image using fs.url() and store it in the row list
            saved_image_urls.append(fs.url(cell_file))

            preprocessed_path = os.path.join(settings.MEDIA_ROOT, f"preprocessed_{i}.png")
            pil_image = Image.open(temp_img_path).convert('RGB')  # Convert to RGB for processing
            preprocess_image(pil_image, save_path=preprocessed_path)

            predicted_text = run_ocr_on_image(pil_image)

            print("Spejimas:" + predicted_text)

            os.remove(temp_img_path)


        # Optionally delete the original uploaded image if no longer needed
        fs.delete(filename)

        # Return the image URLs for rendering
        return render(request, 'conversion/show_split_images.html', {'image_urls': saved_image_urls})

    return JsonResponse({"error": "Invalid request"}, status=400)
# Create your views here.
