======================
requests_selenium
======================
Features
---------

- when requests.get says 'You don't have permission to access this resource'
- opens headless chrome behind the scenes to get the page source without messing with chromedrivers
- can also define the driver easily if you still need to click on stuff using selenium api

Usage: When requests Doesn't Work
-----

To use this package, you can follow these steps:

1. Install the package: ``pip install requests-selenium``.
2. Import and use the package in your code.
3. Example code snippet:
.. code-block:: python
    import requests
    
    url = 'https://www.psychologytoday.com/'

    html_src = requests.get(url)

    print(hrml_srs)

.. parsed-literal::

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>403 Forbidden</title>
</head><body>
<h1>Forbidden</h1>
<p>You don't have permission to access this resource.</p>
</body></html>


Oh NO! Looks like a job for requests-selenium!

.. code-block:: python

   from requests_selenium.utils import requests_selenium

   url = 'https://www.psychologytoday.com/'

   html_source = requests_selenium.get(url)

   print(html_source)


You can also get the driver to do more interaction with the page, headlessly


.. code-block:: python

    from requests_selenium.utils import requests_selenium

    url = 'https://www.psychologytoday.com/'

    driver = requests_selenium.get_driver()

    driver.get(url)

    element = driver.find_element_by_id('myButton')
    element.click()

    html_source = driver.page_source

    driver.quit()


License
-------

This package is licensed under the MIT License.

.. note::

   Please provide feedback and report issues at the GitHub repository: `GitHub Link <https://github.com/your-username/your-package>`_.
