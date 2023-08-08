import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rearth",
    version="0.0.1",
    author="Nemupy",
    author_email="nemu.otoyume@gmail.com",
    description="Python package for the RearthServer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nemupy/rearth",
    packages=setuptools.find_packages()
)
