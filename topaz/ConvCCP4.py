#this is the code to convert .mtz to .mrc


from string import Template
import os
from CCP4Dispatchers import dispatcher_builder

#easiest way to allow us to use CCP4 in python
cmd = Template(' '.join([
  "-stdin"]))
cmd = cmd.substitute(os.environ)

keywords="""
mtzin /dls/science/users/ycc62267/3a5isf_refmac1.mtz
colin-fc /*/*/[FWT,PHIC]
mapout /home/ycc62267/Desktop/3a5isf_fft1.map
stats
stats-radius 4.0
"""


d=dispatcher_builder("cfft", cmd, keywords)
print cmd

d.call()
print "Hello"








