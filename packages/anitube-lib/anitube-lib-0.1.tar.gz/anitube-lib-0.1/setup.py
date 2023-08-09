from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name="anitube-lib",
    version="0.1",
    author='Lorg0n',
    url='https://github.com/Lorg0n/anitube-ua-lib',
    description='Library that parses data from the site anitube.in.ua',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['beautifulsoup4', 'requests-cache'],
    packages=['anitube-lib'],
)