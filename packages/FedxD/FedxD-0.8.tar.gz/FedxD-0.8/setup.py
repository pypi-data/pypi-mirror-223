import twine
from setuptools import setup , find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(name='FedxD',
    version='0.8',
    packages=['FedxD'],
    author='FedxD',
    author_email='abbaskazim135@gmail.com',
    description='This Package is for Quality of life stuff that you will need in your project',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/FedxD',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    pyton_requires='>=3.10',
    install_requires=['openpyxl','discord','pygame'],

)