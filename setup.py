
from setuptools import setup

setup(
    name = "topaz",
    version = "0.0.1",
    author = "Jenna Elliott",
    author_email = "jenna.elliott@diamond.ac.uk",
    description = "A package to convert an .mtz file to a map using CCP4",
    license = "BSD",
    keywords = "awesome python package",
    packages=[
      'topaz',
      'tests',
    ],
    scripts=[
    ],
    install_requires=[
     # 'pytest',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
    ],
)

