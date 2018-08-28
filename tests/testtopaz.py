
from topaz import running

def testrun():

  folder = '/topaz/tests/exampledir/folder/'
  output_dir = '/topaz/tests/exampledir/out1'
  output_dir = '/topaz/tests/exampledir/out2'
  xyzlim = '0 200 0 200 0 200'

  running.phs2map(folder,
                  output_dir,
                  output_dir2,
                  xyzlim)
  
 
