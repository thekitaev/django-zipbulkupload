import os, shutil

from django.conf import settings
from random import randint
from zipfile import ZipFile


class ZipManager(object):
    """
    Context manager to extract files of given `exts` from ZIP.
    Yields full paths.
    Deletes files on exit.
    """

    def __init__(self, filename, exts=tuple()):
        self.filename = filename
        self.exts = exts

    def __enter__(self):
        def path_name():
            return os.path.join(settings.MEDIA_ROOT, 'tmp_%03.d' % randint(0, 100))

        path_to_extract = path_name()

        while os.path.exists(path_to_extract):
            path_to_extract = path_name()

        os.mkdir(path_to_extract)
        self.temp_folder = path_to_extract

        with ZipFile(self.filename) as zip_file:
            for f in zip_file.filelist:
                name, ext = os.path.splitext(f.filename)
                if len(self.exts) == 0 or ext.lower() in self.exts:
                    zip_file.extract(f.filename, path_to_extract)

        for filename in os.listdir(self.temp_folder):
            full_path = os.path.join(settings.MEDIA_ROOT, self.temp_folder, filename)
            if os.path.isfile(full_path):  # scans only files in archive root
                yield full_path

    def __exit__(self, exc_type, exc_val, exc_tb):
        # recursively delete temp folder
        shutil.rmtree(self.temp_folder)
