#this is the code to convert .mtz to .mrc


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
folder1= "/dls/science/users/ycc62267/mtzfdr"
out1="/dls/science/users/ycc62267/mapfdr"
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
    "colin-fc /*/*/[FWT,PHIC]",
    "mapout %s" %mapout,
    "stats",
    "stats-radius 4.0"
    ])
    d=dispatcher_builder("cfft", cmd, keywords)
    d.call()
    assert os.path.exists(mapout)
mtz2map(folder1,out1)
####################################################################
#code for calling mtzdmp
#this is to find the information for unit cell a b c, and for the space group
#this code is currently incomplete
folder1="/dls/science/users/ycc62267/mtzfdr"

def mtzdump(folder):
  for file in os.listdir(folder):
    f=str(file)
    print f
    assert os.path.exists(folder)
    cmd = Template(' '.join([
     "-stdin"])
    keywords='\n'.join([
    "hklin %s" %os.path.join(folder,f),
    "HEADER[space group]"
    ])
    #i am unsure and need to sort the keywords here to only select the relavent
    #information preferably as a string)
    d=dispatcher_builder("mtzdump", cmd,keywords)
    d.call()
    
#mtzdump(folder1)
print(mtzdump(folder1))

######################################################################
#A similar structure to convert .phs to .mtz
#this code is currently incomplete
folder1= "/dls/science/users/ycc62267/phsfdr"
out1="/dls/science/users/ycc62267/mtzfdr"
def phs2mtz(folder,out):
  for file in os.listdir(folder):
    f=str(file)
    print f
    assert os.path.exists(folder)
    assert os.path.exists(out)
    cmd = Template(' '.join([
     "-stdin"]))
    cmd = cmd.substitute(os.environ)

    mtzout = os.path.join(out,os.path.splitext(f)[0])+".mtz"
    celllengths = ??????
    phslayout= ?????
    spacegroup=?????

    keywords='\n'.join([
    "hklin %s" %os.path.join(folder,f),
    "cell %s" %celllenghts,
    "colin %s" %phslayout,
    "spacegroup %s" %spacegroup,
    "mtzout %s" %mtzout
    ])
    #need to change -colin according to the columns actually present in the file 
    d=dispatcher_builder("convert2mtz", cmd, keywords)
    d.call()
    assert os.path.exists(mtzout)
phs2mtz(folder1,out1)



