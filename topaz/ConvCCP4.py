'''
Classes for file converstion

|

'''

from __future__ import division
from string import Template
import os
from CCP4Dispatchers import dispatcher_builder
import logging

####################################################################

class ConvertTools:

  ''' 
  A class of all conversion functions used in Topaz
  
  |
  
  '''

#########################################################################
  def mtz2map(folder,out,name):

    '''mtz2map converts an mtz file of the electron denstity to an electron
    density map file and saves this file

    **mtzmap arguments:**
    * **folder:** directory path to find mtzfile
    * **out:** directory path to save map file 
    * **name:** name of protein e.g. 3S6E_i
    
    |
    
    '''
  
    mtzin=str(os.path.join(folder,name+'.mtz'))

    assert os.path.exists(folder)
    assert os.path.exists(out)
    if not os.path.exists(mtzin):
      logging.info('mtzin %s does not exist for mtz2map' %mtzin)
      raise RuntimeError('mtzin %s does not exist for mtz2map' %mtzin)
    

    #calling cfft in dispatcher
    cmd = Template(' '.join([
      "-stdin"]))
    cmd = cmd.substitute(os.environ)
    mapout = os.path.join(out,name)+".map"
    keywords='\n'.join([
    "mtzin %s" %mtzin, 
    "colin-fc /*/*/[F,PHI]",
    "mapout %s" %mapout,
    "stats",
    "stats-radius 4.0"
    ])
    d=dispatcher_builder("cfft", cmd, keywords)
    d.call()

    
    if not os.path.exists(mapout):
      print keywords
      logging.warning('mapout %s does not exist, the mtz2map did not work' %mapout)
      raise RuntimeError('mapout %s does not exist, the mtz2map did not work' %mapout)
    assert os.path.exists(mapout)

    logging.info('mtz2map successful\n')
  
  mtz2map=staticmethod(mtz2map)
#####################################################################

  def phs2mtz(phsfile,mtzfile,out,name):

      '''phs2mtz takes a phs file and an mtz file and outputs an mtz file of the
      electron density

      phs2mtz arguments:
      phsfile: file path for phs file
      mtzfile: file path for mtzfile 
      out: directory path for saving mtzfile
      name: protein name: e.g. 3S6E_i
      
      |
      
      '''

      
      from data_get import MtzData
      y=MtzData(mtzfile)
      
      #checking correct paths exist
      assert os.path.exists(phsfile)
      assert os.path.exists(out)
      assert os.path.exists(mtzfile)
  
        
      #calling dispatcher
      hklout = os.path.join(out,name)+".mtz"
      cmd = Template(' '.join(["hklin %s" %phsfile, "hklout %s"
      %hklout
       ]))
      cmd = cmd.substitute(os.environ)
  
      celllengths = str(y.cell).strip('(').strip(')').replace(',',' ')
      phslayout= "H K L F FOM PHI SIGF"
      spacegroup=str(y.sg_num) 
      CTYPOUT = "H H H F W P Q"
  
      keywords='\n'.join([
      "CELL  %s" %celllengths,
      "SYMM %s" %spacegroup,
      "labout %s" %phslayout,
      "CTYPOUT %s" %CTYPOUT,
      ])

      d=dispatcher_builder("f2mtz", cmd, keywords)
      d.call()
       
      if not os.path.exists(hklout):
        logging.warning('hklout %s does not exist, the phs2mtz program has not worked.'%hklout)
        raise RuntimeError('hklout %s does not exist, the phs2mtz program has not worked.'%hklout)

      logging.info('phs2mtz successful\n')
  
  phs2mtz=staticmethod(phs2mtz)
  #############################################################################
   
  def mapbox(folder,out,mtzfile,name,xyzlim):

    '''
    mapbox converts a map into a map of a given size using the symmetry group
    for the protein

    mapbox arguments:
    folder: this is the path to the directory that contains the map file
    out: where the boxmap should be saved
    mtzfile: file location for ,mtz file with best symmetry in
    name: title of the map e.g. 3S6S_i 
    xyzlim: dimensions of output box
    
    |
    
    '''
  
      
    mapin = os.path.join(folder, name +'.map')
    mapout = os.path.join(out,name)+'.map'
    XYZLIM = xyzlim
    
    #use MtzData to get symmetry group
    from data_get import MtzData
    y=MtzData(mtzfile)
    sym=str(y.sg_num)
    
    #Using dispatcher
    cmd=Template(' '.join(["mapin %s" %mapin,  "mapout %s" %mapout]))
    cmd = cmd.substitute(os.environ)
  
    keywords= '\n'.join([
    "XYZLIM %s" %XYZLIM,
    "EXTEND XTAL",
    "SYMMETRY %s" %sym,
    ])
  
    d=dispatcher_builder("mapmask",cmd,keywords)
    d.call()
    
      
    if not os.path.exists(mapout):
      logging.warning('mapout %s does not exist, the mapbox progam has not worked.'%mapout)
      raise RuntimeError('mapout %s does not exist, the mapbox program has not worked.' %mapout)
  
    logging.info('mapbox successful\n')
  
  mapbox=staticmethod(mapbox)
###################################################################################



