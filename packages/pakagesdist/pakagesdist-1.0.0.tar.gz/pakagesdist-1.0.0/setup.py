

from setuptools import setup
def readme_file():

    with open("README.rst", encoding="utf-8") as f:
        dec = f.read()
        return dec

setup(name="pakagesdist", version="1.0.0", description="this is the first pakage that was created by myself",
      packages=["pakagesdist"], py_modules=["study"], author="clw", author_email="2023@qq.com",
      url="https://pypi.test.org/simple",
      long_description = readme_file(), license="MIT")
