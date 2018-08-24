# Topaz: Very much work in progress

Topaz is a package that converts .phs data files for electron density into
.maps. This is done my calling functions from within CCP4 using CCP4Dispatchers.

The outputs of this are a set of .mtz files, a set of .maps of varying sizes and
a set of maps that are all the same specified dimensions. 


## Getting Started

These instructions will get a copy of the project working on your local machine. 

### Prerequisites

To install this software you will need: 

It is important to have already installed ccp4, CCP4Dispatchers and iotbox
before running this program. 

'''
give examples of how to install these things...
'''

### Installing

To get a development env running ...

### How to use

The program is run by calling running from the command line. The program must be
called using CCP4python. The arguments
required are as follows:

* --out1: Location to save maps before tessalation
* --out2: Location to save maps after tessalation
* --folder1: Directory to find files with phasing and symmetry. (e.g. Ep\_phasing
  and 20171025)
* --xyzlim1: Dimensions for tessalated map

Example of how to call:
'''
example here
'''

### Running tests

To run the tests ...

'''
example of tests
'''

expected outcome
'''
expected outcome here
'''

## Authors

* **Jenna Elliott** 

## Acknowledgements

* **Melanie Vollmar**
* **James Parkhurst**
* **Gwyndaf**
* expand this bit...


