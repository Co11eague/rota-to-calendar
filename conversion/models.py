from django.contrib.auth.models import User
from django.db import models


class UploadedTable(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to user
	image = models.ImageField(upload_to='uploaded_tables/')  # Original table image
	uploaded_at = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=50)
	column_count = models.IntegerField()


class TableCell(models.Model):
	table = models.ForeignKey(UploadedTable, related_name='cells', on_delete=models.CASCADE)
	image = models.ImageField(upload_to='split_cells/')  # Original table image
	column_number = models.IntegerField()  # Column number in the table
	row_number = models.IntegerField()
	ocr_text = models.TextField()
