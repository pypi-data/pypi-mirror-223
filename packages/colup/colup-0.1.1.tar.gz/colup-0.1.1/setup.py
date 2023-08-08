# colup/setup.py
from setuptools import setup, find_packages

setup(
    name='colup',
    version='0.1.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['colup=cowork.management.commands.upload_files:main'],
    },
    install_requires=[
        'requests',
        # List your dependencies here
    ],
    description='Colup',
    long_description='A python package to upload files remotely to your coloby projects',
    author='Noah Okoh',
    author_email='noahtochukwu10@gmail.com',
    url='https://github.com/yNoah-droid/colobyv1.0',
)
