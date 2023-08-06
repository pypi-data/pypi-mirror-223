import setuptools
from setuptools import setup, find_packages
import os

from urllib.request import urlopen

with urlopen("https://raw.githubusercontent.com/famutimine/ICD10CodeLookUp/main/README.md") as fh:
    long_description = fh.read().decode()

setuptools.setup(
    name='ICD10CodeLookUp',
    version='0.0.2',
    description='ICD10CodeLookUp is a Python library that can be used to look up ICD10 Diagnosis Codes.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/famutimine/ICD10CodeLookUp',
    author='Daniel Famutimi MD, MPH',
    author_email='danielfamutimi@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Intended Audience :: Healthcare Industry',
    ],
    keywords='ICD1O Code',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas',	
    ],
)
