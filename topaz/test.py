from ConvCCP4 import ConvertTools

phsfile = '/dls/tmp/ghp45345/EP_phasing/m200_e1/4DGU/C2221/4DGU_i.phs'
mtzfile = '/dls/tmp/ghp45345/xia2_stresstest/20180816/4DGU/DataFiles/AUTOMATIC_DEFAULT_free.mtz'
out = '/dls/mx-scratch/ycc62267/mapm200_e1/tempfdr3'
name = '4DGU_i'

ConvertTools.phs2mtz(phsfile,mtzfile,out,name)



phsfile = '/dls/tmp/ghp45345/EP_phasing/m200_e1/4DGU/C2221/4DGU.phs'
mtzfile = '/dls/tmp/ghp45345/xia2_stresstest/20180816/4DGU/DataFiles/AUTOMATIC_DEFAULT_free.mtz'
out = '/dls/mx-scratch/ycc62267/mapm200_e1/tempfdr3'
name = '4DGU'

ConvertTools.phs2mtz(phsfile,mtzfile,out,name)
