from setuptools import setup, find_packages
import pypandoc

# long_description = pypandoc.convert_file("README.md", "rst")

setup(
    name="nanoSQLite",
    version="0.1",
    packages=find_packages(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
