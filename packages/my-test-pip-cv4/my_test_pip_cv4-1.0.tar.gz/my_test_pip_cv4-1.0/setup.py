# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="my_test_pip_cv4",  # ??????????
    version="1.0",
    author="wdy",
    author_email="wday.wong@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wdayang/test",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['opencv-python>=4.2.0.34'],
    py_requires=["myCode"],  # ?????python?????
    python_requires='>=3.6',
)