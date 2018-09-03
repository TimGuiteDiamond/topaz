###############################################################################
'''
Classes for data retrieval
'''
################################################################################
class BestSym(object):
  '''
  A class to get the best symmetry group from a log file

  **Arguments:**

  * **filename:** location of logfile containing info for best space group, e.g. filename = /dls/mx-scratch/melanie/for_METRIX/results_201710/EP_phasing/3S6E/simple_xia2_to_shelxcde.log

   |

  '''
  def __init__(self,filename):
  
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
      
      self.best= tx[start:stop]
      return 

############################################################

class MtzData(object):

  '''
  Class to retrive symmetry group and cell dimentsions from mtz file 
  
  **Arguments:**

  * **filename:** location of mtz file containing cell information
    
  |

  '''

  def __init__(self, filename):

    from iotbx import mtz
    import os.path
    import logging

    if filename is None:
      raise RuntimeError('Need to specify hklin filename')
    elif not os.path.exists(filename):
      raise RuntimeError('%s does not exist' %filename)


    self.mtz_file = mtz.object(filename)
    self.sg_num = self.mtz_file.space_group_number()
    self.cell= self._get_cell()

    logging.info('MtzData successful\n')

    return

  def _get_cell(self):

    '''
    This function is used to extract the unit cell information from an MTZ file.
    It also compares that the unit cells are isomorphous if more than one is
    given, and show an error if not.
    
    |
    
    '''
  
    
    import logging 
    from libtbx.test_utils import approx_equal
    xls=self.mtz_file.crystals()
    ucs=[e.unit_cell() for e in xls]
  
    cell0 = ucs[0]
    tst=all([cell0.is_similar_to(e) for e in ucs])
  
    if not tst:
      print "multiple unit cells found! Only the firlst will be used:"
      logging.info('Multiple unit cells found! Only the first will be used\n')
      for cell in ucs:
        print cell.parameters()
        logging.info(str(cell.parameters()))
  
        #this could be improved by finding a way for one to continue by picking a
        #particular cell
  
   
    logging.info('_get_cell successful\n')
    return cell0
###################################################################################

def str2bool(v):

  '''
  function to get argparse to recognise boolean arguments
  
  |
  
  '''

  if v.lower() in ('yes','true','True','t','y','1'):
    return True
  elif v.lower() in ('no','false','False','f','n','0'):
    return False
  else: 
    raise argparse.ArgumentTypeError('Boolean value expected')
