from django.db import models

# Create your models here.
class UploadedFile(models.Model):
    FILE_TYPES = [
        ('source', 'Source'),
        ('target', 'Target'),
    ]
    source_file_path = models.CharField(max_length=200)
    target_file_path = models.CharField(max_length=200)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    status = models.CharField(max_length=10, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)