"""End-to-end tests for zipbulkupload on Python 3 + modern Django."""
import io
import os
import shutil
import tempfile
import zipfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from zipbulkupload.fields import FromZipFileField

from .testapp.models import Gallery, GalleryImage


def make_zip(entries):
    """Build an in-memory zip: {arcname: content_bytes}."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as zf:
        for name, data in entries.items():
            zf.writestr(name, data)
    buf.seek(0)
    return buf


@override_settings(MEDIA_ROOT=tempfile.mkdtemp(prefix='zbu_media_'))
class ZipBulkUploadFlowTest(TestCase):
    def setUp(self):
        self.addCleanup(shutil.rmtree, settings_media_root(), ignore_errors=True)

    def upload(self, entries, name='upload.zip'):
        buf = make_zip(entries)
        gallery = Gallery(title='Тестовая галерея')
        gallery.bulk_upload = SimpleUploadedFile(name, buf.read())
        gallery.save()
        return gallery

    def test_creates_child_instance_per_matching_file_in_archive_root(self):
        gallery = self.upload({
            'a.jpg': b'jpeg-bytes-1',
            'b.PNG': b'png-bytes-1',   # extension check is case-insensitive
            'c.txt': b'should-be-skipped',
            'nested/d.jpg': b'only-root-files-counted',
        })

        self.assertEqual(GalleryImage.objects.count(), 2)

        files = {os.path.basename(f): f for f in GalleryImage.objects.values_list('image', flat=True)}
        self.assertEqual(set(files), {'a.jpg', 'b.PNG'})

        for image in GalleryImage.objects.all():
            self.assertEqual(image.gallery, gallery)
            # file really exists on disk under MEDIA_ROOT
            self.assertTrue(
                os.path.isfile(os.path.join(settings_media_root(), image.image.name)),
                'saved file missing on disk: %s' % image.image.name,
            )
            with open(os.path.join(settings_media_root(), image.image.name), 'rb') as fh:
                self.assertNotEqual(fh.read(), b'should-be-skipped')

    def test_archive_is_deleted_and_field_cleared_after_processing(self):
        gallery = self.upload({'x.jpg': b'jpeg-bytes'})

        gallery.refresh_from_db()
        self.assertFalse(gallery.bulk_upload, 'zip field must be cleared after processing')
        self.assertEqual(GalleryImage.objects.count(), 1)

    def test_save_without_archive_is_a_noop(self):
        gallery = Gallery.objects.create(title='пустая')

        gallery.save()
        self.assertFalse(gallery.bulk_upload)
        self.assertEqual(GalleryImage.objects.count(), 0)


class FromZipFileFieldTest(TestCase):
    def test_upload_to_is_passed_through_to_the_field(self):
        field = FromZipFileField(upload_to='bulk/')
        field.set_attributes_from_name('bulk_upload')

        self.assertEqual(field.upload_to, 'bulk/')

    def test_py2_migration_bytes_upload_to_is_normalized_to_str(self):
        """Old umsa migrations pass py2-style bytes values, e.g. upload_to=b''."""
        field = FromZipFileField(upload_to=b'', blank=True, null=True)
        field.set_attributes_from_name('bulk_upload')

        self.assertEqual(field.upload_to, '')
        self.assertNotIsInstance(field.upload_to, bytes)


def settings_media_root():
    from django.conf import settings
    return settings.MEDIA_ROOT
