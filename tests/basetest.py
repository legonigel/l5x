'''
Created on 2nd Nov 2015

@author: hutcheb
'''
import unittest, l5x
from l5x.tests import common_testing

class BaseTest(common_testing.DefaultCase):

    def setUp(self):
        self.prj = l5x.Project('./tests/basetest.L5X')       
                     
    def tearDown(self):        
        pass
    
    def test_OpenProject(self):
        """Confirm test l5x file can be opened"""        
        self.assertTrue(self.prj != None)

     
    def test_ConfirmBooleanTag(self):
        """Confirm boolean1 tag exists and is correct""" 
        self.assertBaseTag(self.prj.controller.tags,\
                      'boolean1',\
                      'Test Boolean 1',\
                      'BOOL',\
                      'Read/Write',\
                      "false")  
        
    def test_ConfirmRealTag(self):
        """Confirm real1 tag exists and is correct"""  
        self.assertBaseTag(self.prj.controller.tags,\
                      'real1',\
                      'Test Real 1',\
                      'REAL',\
                      'Read/Write',\
                      "false")  

    def test_ConfirmDintTag(self):
        """Confirm DINT1 tag exists and is correct"""                
        self.assertBaseTag(self.prj.controller.tags,\
                      'dint1',\
                      'Test DINT 1',\
                      'DINT',\
                      'Read/Write',\
                      "false")  
        
    def test_ConfirmProgram(self):
        """Confirm MainProgram gets created"""  
        name = 'MainProgram' 
        test_edits = "false"
        main_routine_name = "MainRoutine"
        disabled = "false"
             
        self.assertTrue(name in self.prj.programs.names)  
        prog = self.prj.programs[name]
        self.assertEqual(prog.test_edits, test_edits) 
        self.assertEqual(prog.main_routine_name, main_routine_name) 
        self.assertEqual(prog.disabled, disabled) 
    
    def test_ConfirmRoutine(self):
        """Confirm MainRoutine gets created"""  
        program = 'MainProgram'        
        name = 'MainRoutine'   
        type = "RLL"
        rung_type = "N"
        rung_text = "JSR(TestFunctionBlockRoutine,0);"
              
        self.assertTrue(name in self.prj.programs[program].routines.names)  
        routine = self.prj.programs[program].routines[name]
        self.assertEqual(routine.type, type)
        self.assertEqual(routine.rungs['0'].type, rung_type)
        self.assertEqual(routine.rungs['0'].text, rung_text)       
    
    def test_ConfirmProgramTag(self):
        """Confirm boolean2 tag exists and is correct""" 
        program = 'MainProgram'   
        self.assertBaseTag(self.prj.programs[program].tags,\
                      'boolean2',\
                      'Test Boolean 2',\
                      'BOOL',\
                      'Read/Write',\
                      "false")   
        
    def test_multiple_element_modify(self):
        """Confirm the correct file is read back when modifying multiple elements before writing""" 
        program = 'MainProgram' 
        routine = 'TestFunctionBlockRoutine'  
        sheet = '1'
        
        self.prj.programs[program].description = "Test Modify Multiple Elements"
        self.prj.programs[program].test_edits = "true"
        self.prj.schema_revision = "2.3"
        self.prj.programs[program].routines[routine].sheet_size = "C"
        newprj = self.write_read_project()  
        self.assertEqual(newprj.programs[program].description, \
                         "Test Modify Multiple Elements")
        self.assertEqual(newprj.programs[program].test_edits, \
                         "true")
        self.assertEqual(newprj.schema_revision, \
                         "2.3")
        self.assertEqual(newprj.programs[program].routines[routine].sheet_size, \
                         "C")
    


    def test_Write(self):
        """Confirm un-modified file is written to output correctly""" 
        self.prj.write('./tests/__results__/basetest_output.L5X')

    def assertBaseTag(self, tags, tag, description, data_type, external_access, constant):
        """Asserts that the tag is found and has the correct attributes"""  
        self.assertTrue(tag in tags.names)        
        self.assertEqual(tags[tag].data_type, data_type)            
        self.assertEqual(tags[tag].description, description)     
        self.assertEqual(tags[tag].external_access, external_access) 
        self.assertEqual(tags[tag].constant, constant) 
        

               
if __name__ == "__main__": 
    unittest.main()
    