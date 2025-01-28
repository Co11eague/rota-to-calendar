import math
import os
import uuid
from io import BytesIO

import cv2
import numpy as np
import torch
from PIL import Image, ImageOps
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.shortcuts import render, redirect
from easyocr import easyocr

from accountSettings.models import UserSettings
from conversion.forms import ConversionForm
from conversion.model import Model
from conversion.models import UploadedTable, TableCell
from conversion.utils import AttnLabelConverter
from rotacalendar import settings
from rotacalendar.utils import split_table_into_list

# Initialize your model outside of the view to avoid reloading on every request
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def load_model():
	"""Load the pretrained model once and return it."""
	model_storage_directory = os.path.join(settings.BASE_DIR, 'custom_model/TPS-ResNet-BiLSTM-Attn.pth')

	opt = type('', (), {})()  # Empty object for options, simulate argparse arguments
	opt.imgH = 32
	opt.imgW = 80
	opt.batch_max_length = 50
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


def preprocess_image(image, target_height=32, target_width=80, keep_ratio_with_pad=True):
	"""Preprocess the image: resize, pad, normalize, and convert to tensor"""

	image.save(os.path.join(settings.MEDIA_ROOT, f"normal{uuid.uuid4()}.png"))

	# Convert to grayscale if image is in RGB
	if image.mode != 'L':
		image = image.convert('L')

	if keep_ratio_with_pad:
		# Resize to keep aspect ratio
		w, h = image.size
		ratio = w / float(h)
		resized_w = min(math.ceil(target_height * ratio), target_width)
		resized_image = image.resize((resized_w, target_height), Image.BICUBIC)

		# Apply padding if necessary
		padding_left = (target_width - resized_w) // 2
		padding_right = target_width - resized_w - padding_left
		padded_image = ImageOps.expand(resized_image, (padding_left, 0, padding_right, 0), fill=0)
	else:
		resized_image = image.resize((target_width, target_height))
		padded_image = resized_image

	# Normalize the image: here we normalize to [0, 1] first and can change as needed
	image = np.array(padded_image).astype(np.float32) / 255.0

	# Convert to tensor and normalize similarly to the other method [-1, 1]
	image = torch.tensor(image).unsqueeze(0).unsqueeze(0)  # [1, 1, 32, 80]
	image.sub_(0.5).div_(0.5)  # Normalize to [-1, 1]

	# padded_image.save(os.path.join(settings.MEDIA_ROOT, f"preprocessed{uuid.uuid4()}.png"))

	return image


def run_ocr_on_image(image):
	"""Run OCR model inference on an image."""
	image_tensor = preprocess_image(image).to(device)
	text_for_pred = torch.LongTensor(1, 50 + 1).fill_(0).to(device)  # Empty text input for prediction
	preds = model(image_tensor, text_for_pred, is_train=False)  # Run inference
	preds_size = torch.IntTensor([preds.size(1)]).to(device)  # Get prediction size
	_, preds_index = preds.max(2)  # Get the max probability indexes

	# Decode prediction
	converter = AttnLabelConverter('0123456789abcdefghijklmnopqrstuvwxyz -:|()')  # Adjust if needed
	preds_str = converter.decode(preds_index, preds_size)

	pred_end = preds_str[0].find('[s]')
	pred_text = preds_str[0][:pred_end].strip()  # Text before [s] token

	return pred_text  # Return the predicted text

def convert_to_inmemory_uploadedfile(image, name="cell_image.png"):
	"""
	Converts a numpy array image to a Django InMemoryUploadedFile.
	"""
	# Convert the NumPy array to PNG format
	_, buffer = cv2.imencode('.png', image)
	image_data = BytesIO(buffer.tobytes())

	# Create an InMemoryUploadedFile (same structure as uploaded file from a form)
	uploaded_file = InMemoryUploadedFile(
		file=image_data,  # The file object that we want Django to treat as an uploaded file
		field_name=None,  # Not needed for our purpose
		name=name,  # Name the file should have
		content_type='image/png',  # Image content type (change to match your image type if needed)
		size=image_data.getbuffer().nbytes,  # File size in bytes
		charset=None
	)

	return uploaded_file



@login_required
def index(request):
	user_settings = UserSettings.objects.get(user=request.user)
	conversionForm = ConversionForm()

	return render(request, 'conversion/index.html', {'conversionForm': conversionForm, 'dark': user_settings.darkMode})


@login_required
def process_table_image(request):
	if request.method == 'POST':


		conversion_form = ConversionForm(request.POST, request.FILES)


		if conversion_form.is_valid():
			uploaded_table = conversion_form.save(commit=False)

			uploaded_table.user = request.user

			uploaded_table.save()

			uploaded_image_path = uploaded_table.image.path  # Local file path of the image

			# Process the table into a matrix (assuming you have a function for this)
			table_list = split_table_into_list(uploaded_image_path)

			reader = easyocr.Reader(['en'])

			# Save each cell image using FileSystemStorage
			saved_image_urls = []
			for i, image in enumerate(table_list):
				_, cell_buffer = cv2.imencode('.png', image)  # Convert to PNG format for storage

				# Prepare the PIL image for OCR preprocessing
				pil_image = Image.open(BytesIO(cell_buffer.tobytes()))
				_, image_buffer = cv2.imencode('.png', image)

				ocrMode = UserSettings.objects.get(user=request.user).ocrRecognition

				if ocrMode == "native":
					predicted_text = run_ocr_on_image(pil_image)
				else:
					result = reader.readtext(image)

					if result:
						best_prediction = max(result, key=lambda x: x[2])
						bbox, text, confidence = best_prediction
						predicted_text = text
					else:
						predicted_text = ""

				uploaded_file = convert_to_inmemory_uploadedfile(image, f"cell_{uuid.uuid4()}.png")

				print("Spejimas:" + predicted_text)
				# Save cell data directly to the database
				TableCell.objects.create(
					table=uploaded_table,
					column_number=(i % int(uploaded_table.column_count)) + 1,
					row_number=i // int(uploaded_table.column_count) + 1,
					ocr_text=predicted_text,
					image=uploaded_file
				)

			# Optionally delete the original uploaded image if no longer needed

			# Return the image URLs for rendering
			return redirect('/history/' + str(uploaded_table.id) + '/cells/')
		else:
			return JsonResponse({"error": "Invalid request"}, status=400)