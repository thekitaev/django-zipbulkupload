"""Minimal Django settings for the zipbulkupload test suite."""
import tempfile

SECRET_KEY = 'test-only-secret-key'

DEBUG = True

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'zipbulkupload',
    'tests.testapp',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

MEDIA_ROOT = tempfile.mkdtemp(prefix='zbu_test_media_')
MEDIA_URL = '/media/'

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
