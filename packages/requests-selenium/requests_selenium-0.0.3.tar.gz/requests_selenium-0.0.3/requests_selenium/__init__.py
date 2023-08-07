
# Import the main class from the selenium_utils module using an absolute import
from requests_selenium.selenium_utils import requests_selenium

# Define the __all__ variable to control what gets imported with 'from requests_selenium import *'
__all__ = ['requests_selenium']

#python setup.py sdist bdist_wheel
#twine upload dist/*
