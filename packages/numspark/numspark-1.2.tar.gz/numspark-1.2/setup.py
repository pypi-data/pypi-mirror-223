from setuptools import setup, find_packages

name = "numspark"
version = "1.2"
description = "A math library for python"
author = "Sahil Rajwar"
url = "https://github.com/Sahil-Rajwar-2004/NumSpark"

with open("README.md","r",encoding = "utf-8") as file:
    long_description = file.read()

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=author,
    url=url,
    packages=find_packages(),
    install_requires=["numpy","sympy"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="math library numpy-alternative sci-calc calc",
    project_urls={
        "Source": url,
        "Bug Reports": f"{url}/issues",
    },
)
