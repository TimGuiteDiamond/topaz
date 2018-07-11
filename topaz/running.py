#this is to call the phs2mtz and the mtz2map functions
#this is probably not a good thing to do- needs lots of memory for a while
from ConvCCP4 import phs2mtz
from ConvCCP4 import mtz2map
import os
import shutil
#####################################################################
def phs2map(folder,mtzfolder,output_dir):
    #check that the temp directory does not already exist

    if not os.path.isdir(output_dir):
      print('creating output directory '+output_dir)
      os.mkdir(output_dir)
    logfile=os.path.join(output_dir, 'logfile_phs2map.txt')
    text = open(logfile,'a')
    text.write('this is a log file for the process of phs2map. \n\n')

    num=0
    #creating a tempory directory
    print('creating a tempory directory')
    text.write('creating a tempory directory\n')
    temp_out = os.path.join(output_dir,'tempfdr')
    while os.path.isdir(temp_out):
      num+=1
      temp_out = os.path.join(output_dir,'tempfdr'+str(num))
      if num > 10:
        print 'there is a problem'
        text.write('there is a problem')
        break

    os.mkdir(temp_out)
    print('calling phs2mtz')
    text.write('calling phs2mtz. \n\n')
    text.close()
    phs2mtz(folder,mtzfolder,temp_out,logfile)
    print('calling mtz2map')
    text = open(logfile,'a') 
    text.write('calling mtz2map. \n\n')
    text.close()
    mtz2map(temp_out,output_dir,logfile)
    text = open(logfile,'a')
    text.write('deleating tempory directory \n')  
    shutil.rmtree(temp_out)
    text.close()
######################################################################

out1="/dls/science/users/ycc62267/mapfdr/tests/runtest"
folder1 = "/dls/science/users/ycc62267/phsfdr/in/runtest"
mtzfolder1 = "/dls/science/users/ycc62267/mtzfdr/head/runtest"

phs2map(folder1,mtzfolder1,out1)


