from setuptools import setup
import setuptools


setup(
    name="PPP_Lang_Translation",
    version="1.0.3",
    description="Here is a latest module to translate any language's sentence to any other language. It is a translation program purely build in python.",
    author="Somnath Dash",
    packages=setuptools.find_packages(),
    keywords=["translater","translator","language","language translet","language transletor","python","translate","google translater","google api","Language convert","convert language"],
    license="./LICENSE.txt",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    requires=[
        "requests",
        ],
    install_requires=[
        "requests",
        ],
        
)