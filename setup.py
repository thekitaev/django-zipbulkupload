#!/usr/bin/env python

from setuptools import setup

setup(
    name='Django ZipBulkUpload',
    version='0.2',
    description='Django multiupload-through-archive solution',
    author='Andrey Kitaev',
    author_email='thekitaev@yandex.ru',
    url='https://github.com/thekitaev/django-zipbulkupload',
    packages=['zipbulkupload'],
    python_requires='>=3.8',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
