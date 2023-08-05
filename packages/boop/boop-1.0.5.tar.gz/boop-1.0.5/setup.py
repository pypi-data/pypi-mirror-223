# pygenlib/templates/setup_template.py

from setuptools import setup

version = "1.0.5"

setup(
    name='boop',
    version=version,
    description='A brief description of your library',
    author='Your Name',
    author_email='your.email@example.com',
    packages=['boop', 'boop.boop_utils'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
