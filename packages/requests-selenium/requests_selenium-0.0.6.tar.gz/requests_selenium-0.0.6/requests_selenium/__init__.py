

# Import the main class from the selenium_utils module
#from .selenium_utils import requests_selenium

from requests_selenium.utils import requests_selenium
# Import the main class and the get_driver() method from the selenium_utils module

instance = requests_selenium()
requests_selenium = instance

'''
usage:

import requests_selenium

driver = requests_selenium.driver()

print(driver)

'''

'''

python setup.py sdist bdist_wheel
twine upload dist/*

'''

