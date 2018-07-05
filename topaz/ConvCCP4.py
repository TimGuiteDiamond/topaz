#this is the code to convert .mtz to .mrc

from __future__ import division
from string import Template
import os
from CCP4Dispatchers import dispatcher_builder

####################################################################
#Code edited to allow a change of input
#easiest way to call CCP4 functions into python code 
#cmd = Template(' '.join([
#  "-stdin"]))
#cmd = cmd.substitute(os.environ)
#
##this askes to input the file location
#f=raw_input("""/dls/science/users/ycc62267/3a5isf_refmac1.mtz""")
#
#keywords="""
#mtzin """+f+"""
#colin-fc /*/*/[FWT,PHIC]
#mapout /home/ycc62267/Desktop/3a5isf_fft1.map
#stats
#stats-radius 4.0
#"""
#
#d=dispatcher_builder("cfft", cmd, keywords)
#print cmd
#
#d.call()
#print "Hello"
###################################################################
#This is the origninal code from monday 2/7/18
#easiest way to call CCP4 functions into python code 
#cmd = Template(' '.join([
#  "-stdin"]))
#cmd = cmd.substitute(os.environ)

#keywords="""
#mtzin /dls/science/users/ycc62267/3a5isf_refmac1.mtz
#colin-fc /*/*/[FWT,PHIC]
#mapout /home/ycc62267/Desktop/3a5isf_fft1.map
#stats
#stats-radius 4.0
#"""
#
#d=dispatcher_builder("cfft", cmd, keywords)
#d.call()
#################################################################
#now code edited to alow change of folder of files and of the output folders/files
#this code is currently working
#folder1= "/dls/science/users/ycc62267/mtzfdr/tests"

def mtz2map(folder,out):
  for file in os.listdir(folder):
    f=str(file)
    print f	
    assert os.path.exists(folder)
    assert os.path.exists(out)
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
    assert os.path.exists(mapout)

####################################################################
##code for calling mtzdmp
##this is to find the information for unit cell a b c, and for the space group
##using Melaine's code with small adjustments



class MtzData(object):
  def __init__(self, filename):
    from iotbx import mtz
    import os.path

    #check if an MTZ file has been provided, return error is not
    if filename is None:
      raise RuntimeError('Need to specify hklin filename')
    elif not os.path.exists(filename):
      raise RuntimeError('%s does not exist' %filename)
    self.mtz_file= mtz.object(filename)
    self.sg_num = self.mtz_file.space_group_number()
    self.cell = self._get_cell()
    #cols = self.nuz_file.column_labels()
    #col_types = self.mtz_file.column_types()
    #
    ##here i have commented out the inclusing of f type columns because they are
    ##not needed for this code
    #
    ##pull out first column of type F; if there are multiple F and Q columns then
    ##subsequent ones will be ignored; this may need amending for different
    ##phasing methods
    ##getting column with structure factors F
    #findex = col_types.index('F')
    #self.F = cols[findex]
    ##getting column with errors of structure factors 'Q'
    #qindex = findex +1
    #assert col_types[qindex]=='Q'
    #self.Q = cols[qindex]
    #
    #this may be a good place to fine phslayout
    return 

  def _get_cell(self):
    #this function is used to extract the unit cell information from an MTZ
    #file. it also compares that the unit cells are isomorphous if more than one
    #is given, and shows an error if not.

    from libtbx.test_utils import approx_equal
    xls = self.mtz_file.crystals()
    ucs = [e.unit_cell() for e in xls]

    cell0 = ucs[0]
    #this tests all cells to be similar
    tst = all([cell0.is_similar_to(e) for e in ucs])

    if not tst:
      print "multiple unit cells found! Only the first will be used:"
      for cell in ucs: print cell.parameters()

        #this could be improved by finding a way for one to continue by picking
        #a particular cell
    return cell0
    
#######################################################################
#A similar structure to convert .phs to .mtz
#this code works as of 5/7/18

def phs2mtz(folder,mtzfolder,out):
  for file in os.listdir(folder):
    f=str(file)
    print f

    name=os.path.splitext(f)[0]
    name1=name+"_in"
    mtzin= os.path.join(mtzfolder,name1)+".mtz"
    y=MtzData(mtzin)

    assert os.path.exists(folder)
    assert os.path.exists(out)
    assert os.path.exists(mtzfolder)

    hklout = os.path.join(out,name)+".mtz"
    cmd = Template(' '.join(["hklin %s" %os.path.join(folder,f), "hklout %s"
    %hklout
     ]))
    cmd = cmd.substitute(os.environ)

    celllengths = str(y.cell).strip('(').strip(')') 
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

    assert os.path.exists(hklout)
##############################################################################
out1="/dls/science/users/ycc62267/mtzfdr/out"
folder1= "/dls/science/users/ycc62267/phsfdr/in"
mtzfolder1="/dls/science/users/ycc62267/mtzfdr/head"
out2="/dls/science/users/ycc62267/mapfdr/tests"


phs2mtz(folder1,mtzfolder1,out1)
mtz2map(out1,out2)



