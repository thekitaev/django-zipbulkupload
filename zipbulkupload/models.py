import os

from django.db import models
from django.apps import apps
from django.core.files import File
from .contextmanagers import ZipManager


class ZipBulkUploadModel(models.Model):
    """
    When saving with a ZIP-archive in a specified field, extracts it to a temporary folder
    and creates instances related to self with files from an archive.
    """

    def save(self, *args, **kwargs):
        # first save instance to have a PK
        super(ZipBulkUploadModel, self).save(*args, **kwargs)

        bulk_field_name = self.BUMeta.bulkupload_field  # name of zip-field
        bulkupload_field = self._meta.get_field(bulk_field_name)  # a field itself
        valid_exts = bulkupload_field.exts

        target_model = apps.get_model(bulkupload_field.to_model)  # related model
        target_fk_name = None
        # finding foreign key in related model
        for field in target_model._meta.fields:
            if field.get_internal_type() == "ForeignKey" and field.related_model == self._meta.model:
                target_fk_name = field.name
        target_field = bulkupload_field.to_field

        if getattr(self, bulk_field_name):  # if file is uploaded
            with ZipManager(getattr(self, bulk_field_name), valid_exts) as zf:
                for target_file in zf:
                    with open(target_file, mode='rb') as local_file:
                        file_folder, file_name = os.path.split(target_file)
                        create_kwargs = {target_fk_name: self}
                        child = target_model.objects.create(**create_kwargs)
                        getattr(child, target_field).save(file_name, File(local_file))
            getattr(self, bulk_field_name).delete()  # delete an archive and clear field

    class Meta:
        abstract = True

    class BUMeta:
        bulkupload_field = 'bulk_upload'
