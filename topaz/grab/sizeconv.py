 # this is a script to change the size of the maps so they all are of the same
 # volume
import os
from string import Template
from CCP4Dispatchers import dispatcher_builder


def mapbox(folder,out,name,xyzlim,logfile,mtzfile)

  mapin = '/dls/science/users/ycc62267/mapfdr/tests/3UWT.map'
  mapin = os.path.join(folder,name+'.map')
  mapout = '/dls/science/users/ycc62267/mapfdr/tests/3UWTtest.map'
  mapout = os.path.join(out,name)+".map"
  XYZLIM = '0 300 0 300 0 300'
  XYZLIM = xyzlim
  sym = 'P3121'
  y=MtzData(mtzfile, logfile)
  sym = str(y.sg_num)

  cmd = Template(' '.join(["mapin %s" %mapin, "mapout %s"
  %mapout]))

  cmd=cmd.substitute(os.environ)

  keywords = '\n'.join([
  "XYZLIM %s" %XYZLIM,
  "EXTEND XTAL",
  "SYMMETRY %s" %sym, 
  ])

  d=dispatcher_builder("mapmask",cmd,keywords)
  d.call()
  


