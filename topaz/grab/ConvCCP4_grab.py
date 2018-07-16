#this is the code to convert .phs and .mtz to .map

from __future__ import division
from string import Template
import os
from CCP4Dispatchers import dispatcher_builder

####################################################################

#now code edited to alow change of folder of files and of the output folders/files
#folder1= "/dls/science/users/ycc62267/mtzfdr/tests"

def mtz2map(folder,out,logfile,name):

  #opening logfile
  text=open(logfile,'a')
  #text.write('mtz2map\n')


  mtzin=str(os.path.join(folder,name+'.mtz'))
  #f e.g. = /dls/science/..../mapfdr/tests/runtest/3S6E_i.mtz

  #adding to logfile
  #text.write('for file '+name+'.mtz \n')

  assert os.path.exists(folder)
  assert os.path.exists(out)
  if not os.path.exists(mtzin):
    text.write('mtzin %s does not exist for mtz2map' %mtzin)
    raise RuntimeError('mtzin %s does not exist for mtz2map' %mtzin)
    

  #calling cfft in dispatcher
  #text.write('calling cfft using ccp4 dispatcher\n')
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
  print mapout
  print mtzin
  if not os.path.exists(mapout):
    text.write('mapout %s does not exist, the mtz2map did not work'%mapout)
    raise RuntimeError('mapout %s does not exist, the mtz2map did not work' %mapout)
  assert os.path.exists(mapout)
  text.write('mtz2map successful\n')
  text.close()

####################################################################
##code for calling mtzdmp
##this is to find the information for unit cell a b c, and for the space group
##using Melaine's code with small adjustments

class MtzData(object):
  def __init__(self, filename,logfile):
    from iotbx import mtz
    import os.path

    #text=open(logfile,'a')
    #text.write('MtzData\n')

    #check if an MTZ file has been provided, return error is not
    if filename is None:
      raise RuntimeError('Need to specify hklin filename')
    elif not os.path.exists(filename):
      raise RuntimeError('%s does not exist' %filename)


    #text.write('reading file and creating a class.\n')
    self.mtz_file= mtz.object(filename)
    self.sg_num = self.mtz_file.space_group_number()
    #text.write('calling _get_cell() to get cell dimensions \n')
    #text.close()
    self.cell = self._get_cell(logfile)

    text=open(logfile,'a')
    text.write('MtzData successful\n')
    text.close()
    #cols = self.nuz_file.column_labels()
    #col_types = self.mtz_file.column_types()
    #
    ##here i have removed the code incuding the addition of f type and q type columns because they are
    ##not needed for this code
    #    
    #this may be a good place to fine phslayout
    return 

  def _get_cell(self,logfile):
    #this function is used to extract the unit cell information from an MTZ
    #file. it also compares that the unit cells are isomorphous if more than one
    #is given, and shows an error if not.
    text=open(logfile,'a')
    #text.write('_get_cell\n')
    from libtbx.test_utils import approx_equal
    xls = self.mtz_file.crystals()
    ucs = [e.unit_cell() for e in xls]

    cell0 = ucs[0]
    #this tests all cells to be similar
    tst = all([cell0.is_similar_to(e) for e in ucs])

    if not tst:
      print "multiple unit cells found! Only the first will be used:"
      text.write('multiple unit cells found! Only the first will be used\n')
      for cell in ucs: 
        print cell.parameters()
        text.write( cell.parameters())
                        
        #this could be improved by finding a way for one to continue by picking
        #a particular cell
    text.write('_get_cell successful\n')
    text.close()
    return cell0
    
#######################################################################
#A similar structure to convert .phs to .mtz

def phs2mtz(phsfile,mtzfile,out,logfile,name):
  #for file in os.listdir(folder)
  #  f=str(file)
  #  print f
  #  f=str(phsfile)

    #opening logfile
    text= open(logfile,'a')
    #text.write('\n\nfor file '+phsfile+'\n')


   # name=os.path.splitext(f)[0]
   # name1=name+"_in"

    #writing in logfile
    #text.write('extracting data from mtz file '+mtzfile+' using MTzData(). \n')
    #text.close()
    y=MtzData(mtzfile,logfile)
    
    #checking correct paths exist
    assert os.path.exists(phsfile)
    assert os.path.exists(out)
    assert os.path.exists(mtzfile)

    #adding to logfile
    #text=open(logfile,'a')
    #text.write('calling f2mtz through a ccp4 dispatcher. \n')

    print out
    print name

    #calling dispatcher
    hklout = os.path.join(out,name)+".mtz"
    cmd = Template(' '.join(["hklin %s" %phsfile, "hklout %s"
    %hklout
     ]))
    cmd = cmd.substitute(os.environ)

    celllengths = str(y.cell).strip('(').strip(')').replace(',',' ')
    #celllengths = "66.4687 112.149 149.93 90.00 90.00 90.00"
    phslayout= "H K L F FOM PHI SIGF"
    spacegroup=str(y.sg_num) 
    CTYPOUT = "H H H F W P Q"

    keywords='\n'.join([
    "CELL  %s" %celllengths,
    "SYMM %s" %spacegroup,
    "labout %s" %phslayout,
    "CTYPOUT %s" %CTYPOUT,
    ])
    print keywords
 
    d=dispatcher_builder("f2mtz", cmd, keywords)
    d.call()
    print hklout
    if not os.path.exists(hklout):
      text.write('hklout %s does not exist, the phs2mtz program has not worked.'%hklout)
      raise RuntimeError('hklout %s does not exist, the phs2mtz program has not worked.'%hklout)
    text.write('phs2mtz successful\n')
    text.close()
#############################################################################
# This is a function to convert the map into a map of a given size using the
# spacegroup of the crystal

def mapbox(folder,out,mtzfile,name,xyzlim,logfile):

  text=open(logfile,'a')

  mapin = os.path.join(folder, name +'.map')
  mapout = os.path.join(out,name)+'.map'
  XYZLIM = xyzlim
  
  y=MtzData(mtzfile,logfile)
  sym=str(y.sg_num)

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
    raise RuntimeError('mapout %s does not exist, the mapbox program has not
    worked.' %mapout)

  text.write('mapbox successful\n')
  text.close()


###################################################################################

#out1="/dls/science/users/ycc62267/mtzfdr/out"
#folder1= "/dls/science/users/ycc62267/phsfdr/in"
#mtzfolder1="/dls/science/users/ycc62267/mtzfdr/head"
#out2="/dls/science/users/ycc62267/mapfdr/tests"


#phs2mtz(folder1,mtzfolder1,out1)
#mtz2map(out1,out2)



