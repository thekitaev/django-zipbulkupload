# django-zipbulkupload
Abstract model for easily creating related instances by uploading ZIP-archive to a model field.

Python 3.8+ (tested on Python 3.9/3.14 with Django 4.2 LTS/6.x). Python 2 is no longer supported (version 0.1a was the last py2 release).

## How to use
First install package with
```
pip install git+https://github.com/thekitaev/django-zipbulkupload
```
Or just download it and copy to project root.

Add `zipbulkupload` to `INSTALLED_APPS`.

In `models.py` inherit parent model from `ZipBulkUploadModel`. Add `FromZipFileField` with `to_model` (`app.Model`) 
and `to_field` attributes. If you need to limit file formats, you can add `exts` with a list or tuple of `.ext`'s.

Default zip field name is `bulk_upload` but you can rename it at `BUMeta.bulkupload_field`.

Add a second model with a `ForeignKey` to first one.
Add a target field for files. Should work for any subclasses or `FileField` and `ImageField`.

Example:
```python
from django.db import models
from zipbulkupload.models import ZipBulkUploadModel
from zipbulkupload.fields import FromZipFileField


class Parent(ZipBulkUploadModel):
    name = models.CharField('name', max_length=50)
    bulk_upload = FromZipFileField(to_model='main.Child', to_field='image', exts=('.jpg', '.png'))
    # other things


class Child(models.Model):
    parent = models.ForeignKey('Parent')
    image = models.FileField()
    # and so on
```

Then `makemigrations` and `migrate` with `manage.py`.

Now pack your files into a ZIP-archive. Create an instance and upload an archive to `FromZipFileField`. Voilà!


## Tests
```
PYTHONPATH=. DJANGO_SETTINGS_MODULE=tests.settings python -m django test tests
```

### TODO
- Change `FromZipFileField`'s `to_model` format to `ForeignKey`'s one
- ~~Tests~~
- Exceptions raising for wrong parameters
- Several fields for one model
- Filter in-archive system files (done partially)
- Move functionality from model to field (maybe)
