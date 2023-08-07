from setuptools import setup, find_packages

setup(
    name="olografos",
    version="1.0.2",
    packages=find_packages(),
    install_requires=[],
    author="Yiannis Mertzanis",
    author_email="imertz@protonmail.com",
    description="A package to convert numbers to greek words",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/imertz/olografos-py",
)
