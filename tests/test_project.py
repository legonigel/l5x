'''
Created on 2nd Nov 2015

@author: hutcheb
'''
import unittest, l5x

class TagTestCase(unittest.TestCase):

    def setUp(self):
        self.prj = l5x.Project('basetest.L5X')       
                     
    def tearDown(self):        
        pass
    
    def test_OpenProject(self):
        """Confirm test l5x file can be opened"""
        if self.prj == None:
            self.assertTrue(False)  
        self.assertTrue(True)  
     
    def test_ConfirmBooleanTag(self):
        """Confirm boolean1 tag exists and is correct"""  
        description = 'Test Boolean 1'
        tag = 'boolean1'
        data_type = 'BOOL'   
        external_access = 'Read/Write'
        constant = "false"
        
        ctl_tags = self.prj.controller.tags
        tag_names = ctl_tags.names                
        self.assertTrue(tag in tag_names)        
        self.assertEqual(ctl_tags[tag].data_type, data_type)            
        self.assertEqual(ctl_tags[tag].description, description)     
        self.assertEqual(ctl_tags[tag].external_access, external_access) 
        
    def test_ConfirmRealTag(self):
        """Confirm real1 tag exists and is correct"""  
        description = 'Test Real 1'
        tag = 'real1'
        data_type = 'REAL'   
        external_access = 'Read/Write'
        constant = "false"     
        
        ctl_tags = self.prj.controller.tags
        tag_names = ctl_tags.names                
        self.assertTrue(tag in tag_names)        
        self.assertEqual(ctl_tags[tag].data_type, data_type)            
        self.assertEqual(ctl_tags[tag].description, description)     
        self.assertEqual(ctl_tags[tag].external_access, external_access) 
        self.assertEqual(ctl_tags[tag].constant, constant) 

    def test_ConfirmDintTag(self):
        """Confirm DINT1 tag exists and is correct"""  
        description = 'Test DINT 1'
        tag = 'dint1'
        data_type = 'DINT'   
        external_access = 'Read/Write'
        constant = "false"     
        
        ctl_tags = self.prj.controller.tags
        tag_names = ctl_tags.names                
        self.assertTrue(tag in tag_names)        
        self.assertEqual(ctl_tags[tag].data_type, data_type)            
        self.assertEqual(ctl_tags[tag].description, description)     
        self.assertEqual(ctl_tags[tag].external_access, external_access) 
        self.assertEqual(ctl_tags[tag].constant, constant) 
            

if __name__ == "__main__": 
    unittest.main()