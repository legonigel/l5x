'''
Created on Nov 3, 2015

@author: "hutcheb"
'''

import unittest
loader = unittest.TestLoader()
ts = loader.discover('./tests', pattern='*test.py')
tr = unittest.runner.TextTestRunner(verbosity=10)
tr.run(ts)
