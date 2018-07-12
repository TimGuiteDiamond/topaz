#this is to call the phs2mtz and the mtz2map functions
#this is probably not a good thing to do- needs lots of memory for a while
#in running_grab.py i am trying to see if looping in phs2map works better


from ConvCCP4_grab import phs2mtz
from ConvCCP4_grab import mtz2map
from best import BestSym
import os
import shutil
#####################################################################
def phs2map(folder,output_dir):
    #check that the temp directory does not already exist

    if not os.path.isdir(output_dir):
      print('creating output directory '+output_dir)
      os.mkdir(output_dir)

#m can be deleated after tests
    m=0

    logfile=os.path.join(output_dir, 'logfile_phs2map.txt')
    text = open(logfile,'a')
    text.write('This is a log file for the process of phs2map. \n')

    
    #creating a tempory directory
    print('creating a tempory directory')
    #text.write('creating a tempory directory\n')
    temp_out = os.path.join(output_dir,'tempfdr')
    num=0
    while os.path.isdir(temp_out):
      num+=1
      temp_out = os.path.join(output_dir,'tempfdr'+str(num))
      if num > 10:
        print 'there is a problem'
        text.write('there is a problem with the number of tempory directories that already exist')
        raise RuntimeError('there is a problem with the number of tempory directories that already exist')
    os.mkdir(temp_out)
    if not os.path.exists(temp_out):
      text.write('there is a problem creating a tempory directory')
      raise RuntimeError('there is a problem creating a tempory directory')
    text.close()


#finding all information
    protein_name_directory = os.path.join(folder,'EP_phasing')
    mtz_name_directory = os.path.join(folder,'20171025')

    for dir in os.listdir(protein_name_directory):
        protein_name=str(dir)
        print protein_name
        #protein_name, e.g. = 3S6E

        text=open(logfile,'a')
        text.write('\n\n'+protein_name+' \n')
         
        mtzfile = os.path.join(mtz_name_directory,protein_name,'DataFiles/AUTOMATIC_DEFAULT_free.mtz')
        if not os.path.exists(mtzfile):
          print '%s does not exist' %mtzfile
          text.write('%s does not exist\n' %mtzfile)
          continue


        infofile =  os.path.join(protein_name_directory,protein_name,'simple_xia2_to_shelxcde.log')
        if not os.path.exists(infofile):
          print 'simple_xia2_to_shelxcde.log does not exist for '+protein_name
          text.write('simple_xia2_to_shelxcde.log does not exist for %s\n ' %protein_name)
          continue
        text.close()

        print infofile
        best_symmetry = str(BestSym(infofile).best)

     #   m+=1
     #   if m>3:
     #     break

        phsdir = os.path.join(protein_name_directory,protein_name,best_symmetry)
        if not os.path.exists(phsdir):
          print '%s does not exist' %phsdir
          text=open(logfile,'a')
          text.write('%s does not exist\n' %phsdir)
          text.close()
          continue


        for file in os.listdir(phsdir):
          if file.endswith('.phs'):
            
            name=str(file)
            type_name = name[:-4]
            #name e.g. = 3S6E_i.phs
            phsfile = os.path.join(phsdir,name)

            text=open(logfile,'a')
            text.write('\n'+name+'\n')
            text.close()
     
            #text=open(logfile,'a')
            print('calling phs2mtz')
            #text.write('calling phs2mtz. \n\n')
            #text.close()
            phs2mtz(phsfile,mtzfile,temp_out,logfile,type_name)

            print('calling mtz2map')
            #text = open(logfile,'a') 
            #text.write('calling mtz2map. \n\n')
            #text.close()
            mtz2map(temp_out,output_dir,logfile,type_name)
        else:
          continue

#for testing i will limit the number of itterations
      #  if m>2:
      #    break
      #  else:
      #    m+=1


   # text = open(logfile,'a')
   # text.write('deleating tempory directory \n')  
    shutil.rmtree(temp_out)
   # text.close()
######################################################################

out1="/dls/mx-scratch/ycc62267/mapfdr"
folder1 = "/dls/mx-scratch/melanie/for_METRIX/results_201710"


phs2map(folder1,out1)


