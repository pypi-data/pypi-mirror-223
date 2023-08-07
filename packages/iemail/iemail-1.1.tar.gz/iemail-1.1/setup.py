from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='iemail',
    version='1.1',
    description='Temporary Email Python SDK of https://api.iemail.eu.org/',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://pypi.org/project/iemail/",
    author="IEmail",
    author_email="i@iemail.eu.org",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
    keywords="Tempmail mail iemail email API",
    install_requires=["requests"],
    packages=["iemail"],
    project_urls={
        "HomePage": "https://iemail.eu.org/",
        "API Gateway": "https://api.iemail.eu.org/",
    },
)
