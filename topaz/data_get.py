###############################################################################
'''Classes for data retrieval'''
################################################################################
class BestSym(object):
  '''A class to get the best symmetry group from a log file  '''
  def __init__(self,filename):

      '''
      **Arguments:**

      * **filename:** location of logfile, e.g. filename = /dls/mx-scratch/melanie/for_METRIX/results_201710/EP_phasing/3S6E/simple_xia2_to_shelxcde.log

      '''
  
      import os.path


      if filename is None:
       raise RuntimeError('Need to specify hklin filename')
      elif not os.path.exists(filename):
        raise RuntimeError('%s does not exist' %filename)

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

############################################################

class MtzData(object):

  '''Class to retrive symmetry group and cell dimentsions from mtz file '''

  def __init__(self, filename,logfile):

    '''
    **Arguments:**

    * **filename:** location of mtz file
    * **logfile:** location of file to log progress

    '''
    from iotbx import mtz
    import os.path

    if filename is None:
      raise RuntimeError('Need to specify hklin filename')
    elif not os.path.exists(filename):
      raise RuntimeError('%s does not exist' %filename)


    self.mtz_file = mtz.object(filename)
    self.sg_num = self.mtz_file.space_group_number()
    self.cell= self._get_cell(logfile)

    text=open(logfile,'a')
    text.write('MtzData successful\n')
    text.close()

    return

  def _get_cell(self,logfile):

    '''
    This function is used to extract the unit cell information from an MTZ file.
    It also compares that the unit cells are isomorphous if more than one is
    given, and show an error if not.

    **Arguments:**

    * **logfile:** location of file to log progress

    '''
  
    text=open(logfile,'a')
    
    from libtbx.test_utils import approx_equal
    xls=self.mtz_file.crystals()
    ucs=[e.unit_cell() for e in xls]
  
    cell0 = ucs[0]
    tst=all([cell0.is_similar_to(e) for e in ucs])
  
    if not tst:
      print "multiple unit cells found! Only the firlst will be used:"
      text.write('Multiple unit cells found! Only the first will be used\n')
      for cell in ucs:
        print cell.parameters()
        text.write(str(cell.parameters()))
  
        #this could be improved by finding a way for one to continue by picking a
        #particular cell
  
    text.write('_get_cell successful\n')
    text.close()
    return cell0
###################################################################################
