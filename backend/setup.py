# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("requirements.txt", "rb") as requirement_file:
    requirements = requirement_file.read().decode("utf-16").split()
    print(requirements)

setup(
    name="database",
    description="database",
    version="1.0.0",
    author="adess",
    author_email="atagong5@gmail.com",
    install_requires=requirements,
    packages=find_packages()
)