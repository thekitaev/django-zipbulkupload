from django.db.models import FileField


class FromZipFileField(FileField):
    """
    FileField that refers additionally to `model` and its `field` to create related instances.
    Used by ZipBulkUploadModel.
    `to_model` for a related model in `app.Model` format.
    `to_field` for a field of related model to which we write the files.
    `ext` for valid file extensions, format is ('.jpg', '.png').
    """

    def __init__(self, to_model='', to_field='', exts=tuple(), verbose_name=None, name=None, upload_to='', storage=None,
                 **kwargs):
        self.to_model = to_model
        self.to_field = to_field
        self.exts = exts
        kwargs['blank'] = True
        kwargs['null'] = True
        super(FromZipFileField, self).__init__(verbose_name, name, **kwargs)
