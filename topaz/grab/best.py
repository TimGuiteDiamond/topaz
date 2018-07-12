#this is a function to select best_symmetry from the logfile
class BestSym(object):
  def __init__(self,filename):
#e.g. filename = /dls/mx-scratch/melanie/for_METRIX/results_201710/EP_phasing/3S6E/simple_xia2_to_shelxcde.log
  
      import os.path

  #text.open(logfile, 'a')
  #text.write('MtzBestSym: getting the best symmetry for the protein')

      if filename is None:
       raise RuntimeError('Need to specify hklin filename')
      elif not os.path.exists(filename):
        raise RuntimeError('%s does not exist' %filename)
  #text.write('reading the file and creating a class')
  #self.read_file = read.object(filename)
  #self.best_sym = self.read_file.best_symmetry()

      tx=open(filename).read()
      index=tx.find('Best space group: ')
      shift=len('Best space group: ')
      start =int( index + shift)
      stop=int(tx.find(' ', start,start+10))
      print type(stop)
      print type(start)
      print start
      print stop
      self.best= tx[start:stop]
      return 

#filename1 ="/dls/mx-scratch/melanie/for_METRIX/results_201710/EP_phasing/3S6E/simple_xia2_to_shelxcde.log"
#y=BestSym(filename1).best
#print str(y)
