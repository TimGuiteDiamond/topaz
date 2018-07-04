#this is the code to convert .mtz to .mrc


from string import Template
import os
from CCP4Dispatchers import dispatcher_builder


#now code edited to alow change of folder of files and of the output folders/files
folder1= "/dls/science/users/ycc62267/mtzfdr"
out1="/dls/science/users/ycc62267/mapfdr"
def mtz2map(folder,out):
	for file in os.listdir(folder):
		f=str(file)
		print f	
		
		cmd = Template(' '.join([
		  "-stdin"]))
		cmd = cmd.substitute(os.environ)

		keywords=""" 
		mtzin """+f+""" 
		colin-fc /*/*/[FWT,PHIC]
		mapout """+out+os.path.splitext(f)[0]+""".map
		stats
		stats-radius 4.0
		"""
		d=dispatcher_builder("cfft", cmd, keywords)
		d.call()
#print "Hello"
mtz2map(folder1,out1)

































