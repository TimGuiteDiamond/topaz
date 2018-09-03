# Topaz

Topaz is a package that converts .phs data files for electron density into
.maps. This is written as a prerequesite data proccessing step to the package
Eclip, the github repositary for Eclip can be found 
[here](https://github.com/jmp1985/eclip). 

This package calls functions from within CCP4 using CCP4Dispatchers. The 
outputs of this are a set of .mtz files, a set of .map files of various sizes
and a set of .map files that are all the same specified dimensions. 


## Getting Started

These instructions will get a copy of the project working on your local machine. 

### Prerequisites

#### Software
To install this software you will need: 

* pytest
* argparse

These should all be installed (or already were installed) when the environment
is setup (see Installing). However, you will need to have already installed ccp4
before runing this program. 

#### Data
To run the program the directories must have a certain setup, an example of this
set up is included in the exampledir directory under the tests directory. In
here is an example of the layout of directories that the program requires. 

The datafiles required per protein are:
  * A .phs or .pha file - contains experimental data
  * A simple\_xia2\_to\_shelxcode.log file - contains Best space group info
  * A AUTOMATIC\_DEFAULT\_free.mtz file - contains cell dimension and symmetry
    group 



### Installing

To get a development env running first download the package. Then load ccp4,
then go to the directory containing setup.py and type the following into the
command line. 

```
> export Path=$PATH:/<your-ccp4-installation>
> ccp4-python setup.py develop --user
```

### How to use

The program is run by calling RunTopaz from the command line. The program must be
called using CCP4python.

The arguments required are as follows:

* --out1: Location to save maps before tessalation
* --out2: Location to save maps after tessalation
* --folder1: Directory to find files with phasing and symmetry. (e.g. Ep\_phasing
  and 20171025)
* --xyzlim1: Dimensions for tessalated map
* --raw: Whether the data is only the heavy atom positions or not. 

Example of how to call, if the default is needed there is not need to specify
the argument:
```
> RunTopaz --out1=/DIRECTORY/ --out2=/DIRECTORY/ --folder=/DIRECTORY/

```

## Authors

* **Jenna Elliott** 

## Acknowledgements

* Supervisor: **Melanie Vollmar**: 
* Co-supervisor: **James Parkhurst**
* Principle Investigator: **Gwyndaf Evans**


