from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name='yvesCMD',
    version='0.0.6',
    author='YveRadvir',
    url='https://github.com/Yveradvir/Yvescmd',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_data={'': ['README.md']},
    long_description=long_description,
    long_description_content_type='text/markdown',
)
