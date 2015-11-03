'''
Created on 3rd Nov 2015

@author: hutcheb
'''
import unittest, l5x

class SetGetTest(unittest.TestCase):

    def setUp(self):
        self.prj = l5x.Project('./tests/basetest.L5X')       
                     
    def tearDown(self):        
        pass
    
       
if __name__ == "__main__": 
    unittest.main()