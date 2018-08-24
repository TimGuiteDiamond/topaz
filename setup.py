
from setuptools import setup

setup(
    name = "topaz",
    version = "0.0.1",
    author = "Jenna Elliott",
    author_email = "jenna.elliott@diamond.ac.uk",
    description = "A package to convert an .phs file to a map using CCP4",
    license = "BSD",
    keywords = ".phs to .map conversion",
    packages=[
      'topaz',
      'tests',
    ],
    scripts=[
      'bin/RunTopaz'
    ],
    install_requires=[
      'pytest',
      'argparse'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
    ],
)

