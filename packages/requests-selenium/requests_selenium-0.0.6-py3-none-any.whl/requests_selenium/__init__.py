
# Import the main class from the selenium_utils module using an absolute import
from requests_selenium.utils import requests_selenium as requests_selenium

# Define the __all__ variable to control what gets imported with 'from requests_selenium import *'
__all__ = ['requests_selenium']

# Make the requests_selenium class available at the package level
#requests_selenium = requests_selenium

#python setup.py sdist bdist_wheel
#twine upload dist/*
