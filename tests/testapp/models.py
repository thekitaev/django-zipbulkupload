"""Test models mirroring real usage in the umsa project."""
from django.db import models

from zipbulkupload.fields import FromZipFileField
from zipbulkupload.models import ZipBulkUploadModel


class Gallery(ZipBulkUploadModel):
    title = models.CharField('Название', max_length=100)
    bulk_upload = FromZipFileField(
        to_model='testapp.GalleryImage',
        to_field='image',
        exts=('.jpg', '.png'),
        upload_to='bulk/',
        verbose_name='Архив',
    )

    class BUMeta:
        bulkupload_field = 'bulk_upload'

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    image = models.FileField(upload_to='gallery/')

    def __str__(self):
        return self.image.name
