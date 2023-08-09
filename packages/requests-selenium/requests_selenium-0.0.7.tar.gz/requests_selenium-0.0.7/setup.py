from setuptools import setup, find_packages

setup(
    name='requests_selenium',
    version='0.0.7',
    description='A Python package for fetching page source using Selenium',
    author='Ben Bavonese',
    packages=find_packages(), 
    install_requires=[
        'requests',
        'beautifulsoup4',
        'chromedriver_autoinstaller',
        'selenium',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
