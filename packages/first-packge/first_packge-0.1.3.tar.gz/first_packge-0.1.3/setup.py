# my_package/setup.py

from setuptools import setup, find_packages

with open('ReaDMe.txt', 'r') as f:
    long_description = f.read()

setup(
    name='first_packge',
    version='0.1.3',
    author='Sid_',
    author_email='lodiy87986@sportrid.com',
    description='A simple Python package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
)

