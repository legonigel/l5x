"""Common testing methods"""

import unittest, l5x
    
class DefaultCase(unittest.TestCase): 
          
    def read_write_attribute(self, element, attr_value, value, new_value, message):
        """Default Read/Write Test Case"""             
        self.assertEqual(attr_value, value)
        element = new_value
        newprj = self.write_read_project(element)
        return newprj
        
    def write_read_project(self):
        self.prj.write('./tests/__results__/basetest_output.L5X')
        return l5x.Project('./tests/__results__/basetest_output.L5X')