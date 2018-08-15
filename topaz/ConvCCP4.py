

from __future__ import division
from string import Template
import os
from CCP4Dispatchers import dispatcher_builder

####################################################################

class Convert_tools:

  ''' A class of all conversion functions used in Topaz'''

#########################################################################
  def mtz2map(folder,out,logfile,name):

    '''mtz2map converts an mtz file of the electron denstity to an electron
    density map file and saves this file

    **mtzmap arguments:**
    * **folder:** directory path to find mtzfile
    * **out:** directory path to save map file
    * **logfile:** file to log progress of function
    * **name:** name of protein e.g. 3S6E_i
    '''
  
    #opening logfile
    text=open(logfile,'a')

    mtzin=str(os.path.join(folder,name+'.mtz'))

    assert os.path.exists(folder)
    assert os.path.exists(out)
    if not os.path.exists(mtzin):
      text.write('mtzin %s does not exist for mtz2map' %mtzin)
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
      text.write('mapout %s does not exist, the mtz2map did not work'%mapout)
      raise RuntimeError('mapout %s does not exist, the mtz2map did not work' %mapout)
    assert os.path.exists(mapout)

    text.write('mtz2map successful\n')
    text.close()
  
  mtz2map=staticmethod(mtz2map)
#####################################################################

  def phs2mtz(phsfile,mtzfile,out,logfile,name):

      '''phs2mtz takes a phs file and an mtz file and outputs an mtz file of the
      electron density

      phs2mtz arguments:
      phsfile: file path for phs file
      mtzfile:file path for mtzfile 
      out: directory path for saving mtzfile
      logfile: file for loging progess of function
      name: protein name: e.g. 3S6E_i
      '''

      #opening logfile
      text= open(logfile,'a')

      from data_get import MtzData
      y=MtzData(mtzfile,logfile)
      
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
        text.write('hklout %s does not exist, the phs2mtz program has not worked.'%hklout)
        raise RuntimeError('hklout %s does not exist, the phs2mtz program has not worked.'%hklout)

      text.write('phs2mtz successful\n')
      text.close()
  
  phs2mtz=staticmethod(phs2mtz)
  #############################################################################
   
  def mapbox(folder,out,mtzfile,name,xyzlim,logfile):

    '''
    mapbox converts a map into a map of a given size using the symmetry group
    for the protein

    mapbox arguments:
    folder: this is the path to the directory that contains the map file
    out: where the boxmap should be saved
    name: title of the map e.g. 3S6S_i 
    xyzlim: dimensions of output box
    logfile: file to log progress
    '''
  
    text=open(logfile,'a')
  
    mapin = os.path.join(folder, name +'.map')
    mapout = os.path.join(out,name)+'.map'
    XYZLIM = xyzlim
    
    #use MtzData to get symmetry group
    from data_get import MtzData
    y=MtzData(mtzfile,logfile)
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
      text.write('mapout %s does not exist, the mapbox program has not worked.'%mapout)
      raise RuntimeError('mapout %s does not exist, the mapbox program has not worked.' %mapout)
  
    text.write('mapbox successful\n')
    text.close()
  
  mapbox=staticmethod(mapbox)
###################################################################################



