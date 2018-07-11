#this is the code to convert .phs and .mtz to .map

from __future__ import division
from string import Template
import os
from CCP4Dispatchers import dispatcher_builder

####################################################################

#now code edited to alow change of folder of files and of the output folders/files
#this code is currently working
#folder1= "/dls/science/users/ycc62267/mtzfdr/tests"

def mtz2map(folder,out,logfile):
  text=open(logfile,'a')
  text.write('mtz2map\n')
  for file in os.listdir(folder):
    f=str(file)
    print f	

    text.write('for file '+f+'\n')

    assert os.path.exists(folder)
    assert os.path.exists(out)

    text.write('calling cfft using ccp4 dispatcher\n')
    cmd = Template(' '.join([
      "-stdin"]))
    cmd = cmd.substitute(os.environ)
    mapout = os.path.join(out,os.path.splitext(f)[0])+".map"
    keywords='\n'.join([
    "mtzin %s" % os.path.join(folder,f), 
    "colin-fc /*/*/[F,PHI]",
    "mapout %s" %mapout,
    "stats",
    "stats-radius 4.0"
    ])
    d=dispatcher_builder("cfft", cmd, keywords)
    d.call()
    text.close()
    assert os.path.exists(mapout)

####################################################################
##code for calling mtzdmp
##this is to find the information for unit cell a b c, and for the space group
##using Melaine's code with small adjustments

class MtzData(object):
  def __init__(self, filename,logfile):
    from iotbx import mtz
    import os.path

    text=open(logfile,'a')
    text.write('MtzData\n')

    #check if an MTZ file has been provided, return error is not
    if filename is None:
      raise RuntimeError('Need to specify hklin filename')
    elif not os.path.exists(filename):
      raise RuntimeError('%s does not exist' %filename)
    text.write('reading file and creating a class.\n')
    self.mtz_file= mtz.object(filename)
    self.sg_num = self.mtz_file.space_group_number()
    text.write('calling _get_cell() to get cell dimensions \n')
    text.close()
    self.cell = self._get_cell(logfile)
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
    text.write('_get_cell\n')
    from libtbx.test_utils import approx_equal
    xls = self.mtz_file.crystals()
    ucs = [e.unit_cell() for e in xls]

    cell0 = ucs[0]
    #this tests all cells to be similar
    tst = all([cell0.is_similar_to(e) for e in ucs])

    if not tst:
      print "multiple unit cells found! Only the first will be used:"
      text.write('multiple unit cells found! Only the first will be used\n')
      for cell in ucs: print cell.parameters()

        #this could be improved by finding a way for one to continue by picking
        #a particular cell
    text.close()
    return cell0
    
#######################################################################
#A similar structure to convert .phs to .mtz
#this code works as of 5/7/18

def phs2mtz(folder,mtzfolder,out,logfile):
  for file in os.listdir(folder):
    f=str(file)
    print f
    text= open(logfile,'a')
    text.write('\n\nfor file '+f+'\n')
    name=os.path.splitext(f)[0]
    name1=name+"_in"

 
    mtzin= os.path.join(mtzfolder,name1)+".mtz"
    text.write('extracting data from mtz file '+mtzin+' using MTzData(). \n')
    text.close()
    y=MtzData(mtzin,logfile)
    
    
    assert os.path.exists(folder)
    assert os.path.exists(out)
    assert os.path.exists(mtzfolder)
    text=open(logfile,'a')
    text.write('calling f2mtz through a ccp4 dispatcher. \n')

    hklout = os.path.join(out,name)+".mtz"
    cmd = Template(' '.join(["hklin %s" %os.path.join(folder,f), "hklout %s"
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
    #print keywords
 
    d=dispatcher_builder("f2mtz", cmd, keywords)
    d.call()

    assert os.path.exists(hklout)
    text.close()
##############################################################################
#out1="/dls/science/users/ycc62267/mtzfdr/out"
#folder1= "/dls/science/users/ycc62267/phsfdr/in"
#mtzfolder1="/dls/science/users/ycc62267/mtzfdr/head"
#out2="/dls/science/users/ycc62267/mapfdr/tests"


#phs2mtz(folder1,mtzfolder1,out1)
#mtz2map(out1,out2)



