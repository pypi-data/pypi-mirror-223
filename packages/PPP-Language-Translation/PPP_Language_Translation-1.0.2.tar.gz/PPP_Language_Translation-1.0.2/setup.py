from setuptools import setup
import setuptools


setup(
    name="PPP_Language_Translation",
    version="1.0.2",
    description="Here is a latest module to translate any language's sentence to any other language. It is a translation program purely build in python.",
    author="Somnath Dash",
    packages=setuptools.find_packages(),
    keywords=["translater","translator","language","language translet","language transletor","python","translate","google translater","google api","Language convert","convert language"],
    package_dir={"":"src"},
    requires=[
        "requests",
        ],
    install_requires=[
        "requests",
        ],
        
)