from setuptools import setup
from pypandoc import convert_file


try:
    long_description = convert_file('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='MorseCodePy',
    packages=['MorseCodePy'],
    version='1.0.2',
    author='CrazyFlyKite',
    author_email='karpenkoartem2846@gmail.com',
    url='https://github.com/CrazyFlyKite/MorseCode',
    description='Easily translate text into Morse code',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
