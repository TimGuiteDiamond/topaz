
'''
Runs topaz. Converts phs files to map files - this is a very memory intensive
program!! 

|

'''

####################################################################
from data_get import BestSym, str2bool
from ConvCCP4 import ConvertTools
import os
import shutil
import time
import logging
#####################################################################
def phs2map(folder,output_dir,output_dir2,xyzlim,raw = False):

    '''
    Function converts phs files to map files. 
    
    Calls: BestSym, and Convert_tools

    **Arguments:**

    * **folder:** The directory to find the files (directory that includes EP_Phasing and 20171025) - this needs to be generalised.
    * **output_dir:** The directoryto output the original(non-boxed)images.
    * **output_dir2:** The directory to output the maps as boxes
    * **xyzlim:** The dimensions of the required map box <x1> <x2> <y1> <y2> <z1> <z2>.
    * **raw**: Boolean, true if using heavy atom position data. 

    **Outputs:**

    * **Map files**

    |
    
    '''
    
    if raw:
      fileend = '.pha'
    else:
      fileend = '.phs'

    trialnum=1
    date = str(time.strftime("%d%m%y"))
    while os.path.exists(os.path.join(output_dir, 'logfile_phs2map'+date+'_'+str(trialnum)+'.txt')):
      trialnum+=1

    #check that the output  directories does not already exist

    if not os.path.isdir(output_dir):
      print('creating output directory '+output_dir)
      os.mkdir(output_dir)

    if not os.path.isdir(output_dir2):
      print 'creating output directory '+output_dir2
      os.mkdir(output_dir2)

#m can be deleated after tests
    #m=0

    logfile=os.path.join(output_dir, 'logfile_phs2map'+date+'_'+str(trialnum)+'.txt')
    logging.basicConfig(filename = logfile, level = logging.DEBUG)
    logging.info('This is a log file for the process of phs2map. ')
        
    #creating a tempory directory
    print('creating a tempory directory')
    temp_out = os.path.join(output_dir,'tempfdr')
    num=0
    while os.path.isdir(temp_out):
      num+=1
      temp_out = os.path.join(output_dir,'tempfdr'+str(num))
      if num > 10:
        print 'there is a problem'
        logging.warning('there is a problem with the number of tempory directories that already exist')
        raise RuntimeError(
                'there is a problem with the number of tempory directories that already exist')
    os.mkdir(temp_out)
    if not os.path.exists(temp_out):
      logging.warning('there is a problem creating a tempory directory')
      raise RuntimeError('there is a problem creating a tempory directory')
  

    #finding all information
    protein_name_directory = os.path.join(folder,'EP_phasing')
    mtz_name_directory = os.path.join(folder,'20171025')

    for dir in os.listdir(protein_name_directory):
        protein_name=str(dir)
        print protein_name
        #protein_name, e.g. = 3S6E

        logging.info('\n\n'+protein_name+'\n')
  
        mtzfile = os.path.join(mtz_name_directory,
                                protein_name,
                                'DataFiles/AUTOMATIC_DEFAULT_free.mtz')
        if not os.path.exists(mtzfile):
          print '%s does not exist' %mtzfile
          logging.info('%s does not exist\n' %mtzfile)
          continue


        infofile =  os.path.join(protein_name_directory,
                                  protein_name,
                                  'simple_xia2_to_shelxcde.log')
        if not os.path.exists(infofile):
          print 'simple_xia2_to_shelxcde.log does not exist for '+protein_name         
          logging.info('simple_xia2_to_shelxcde.log does not exist for %s\n' %protein_name)
          continue

        print infofile
        best_symmetry = str(BestSym(infofile).best)

        #m+=1
        #if m>2:
        #  break

        phsdir = os.path.join(protein_name_directory,protein_name,best_symmetry)
        if not os.path.exists(phsdir):
          print '%s does not exist' %phsdir 
          logging.info('%s does not exist\n' %phsdir)
          continue


        for file in os.listdir(phsdir):
          if file.endswith(fileend):
            
            name=str(file)
            type_name = name[:-4]
            #name e.g. = 3S6E_i.phs
            phsfile  = os.path.join(phsdir,name) 

            logging.info('\n'+name+'\n')
                 
            print 'calling phs2mtz'
            ConvertTools.phs2mtz(phsfile,mtzfile,temp_out,type_name)

            print 'calling mtz2map'
            ConvertTools.mtz2map(temp_out,output_dir,type_name)

            print 'calling mapbox'
            ConvertTools.mapbox(output_dir,output_dir2,mtzfile,type_name,xyzlim)
        else:
          continue
  
    shutil.rmtree(temp_out)
######################################################################




########################################################################
#now try to make a module
def run():

  '''
  Calls phs2map with ability to call from command line. Run from command line by
  calling RunTopaz

  **default arguments:**

  * **folder1:** The directory to find the files, inc EP_phasing and 20171025
                Default: /dls/mx-scratch/melanie/for_METRIX/results_201710
  * **out1:** The directory to output the original (non-boxed) maps
                Default: /dls/mx-scratch/ycc62267/mapfdrraw
  * **out2:** The directory to output the maps as boxes
                Default: /dls/mx-scratch/ycc62267/mapfdrrawbox
  * **xyzlim1:** The dimensions of the map box
                Default: 0 200 0 200 0 200
  * **raw:** Boolean, whether the data should be processed, or just the heavy atom positions
                Default: False
  '''


  import argparse


  parser = argparse.ArgumentParser(description='command line argument')
  parser.add_argument('--out1',
                      dest = 'out1', 
                      type = str, 
                      help = 'the directoryto output the original(non-boxed)maps.', 
                      default ='/dls/mx-scratch/ycc62267/mapfdrraw')
  parser.add_argument('--out2',
                      dest= 'out2', 
                      type = str, 
                      help = 'the directory to output the maps as boxes', 
                      default= '/dls/mx-scratch/ycc62267/mapfdrrawbox')
  parser.add_argument('--folder1', 
                      dest = 'folder1',
                      type = str, 
                      help = 'the directory to find the files (inc EP_Phasing and 20171025)', 
                      default = '/dls/mx-scratch/melanie/for_METRIX/results_201710')
  parser.add_argument('--xyzlim1', 
                      dest = 'xyzlim1',
                      type = str, 
                      help = 'the dimensions of the map box <x1> <x2> <y1> <y2> <z1> <z2>.',
                      default = '0 200 0 200 0 200')
  parser.add_argument('--raw',
                      dest = 'raw',
                      type = str2bool,
                      help = 'boolean, whether the data should be processed or not',
                      default = False)

  args = parser.parse_args()



  phs2map(args.folder1,
          args.out1,
          args.out2,
          args.xyzlim1,
          args.raw)

#######################################################################  

if __name__ == "__main__":
  run()

#########################################################################
  

