'''
Created on 3rd Nov 2015

@author: hutcheb
'''
import unittest, l5x

class FBDCase(unittest.TestCase):

    def setUp(self):
        self.prj = l5x.Project('./tests/basetest.L5X')       
                     
    def tearDown(self):        
        pass
    
    def test_Iref(self):
        """Confirm Iref Nodes are created correctly"""
        program = 'MainProgram'        
        routine = 'TestFunctionBlockRoutine'  
        sheet = '1'
     
        sheet = self.prj.programs[program].routines[routine].sheets[sheet]
        self.assertEqual(sheet.iref['0'].x, '160')
        self.assertEqual(sheet.iref['0'].y, '120')
        self.assertEqual(sheet.iref['0'].operand, 'boolean1')
        self.assertEqual(sheet.iref['0'].hide_desc, 'false')
        
    def test_Oref(self):
        """Confirm Oref Nodes are created correctly"""
        program = 'MainProgram'        
        routine = 'TestFunctionBlockRoutine'  
        sheet = '1'
     
        sheet = self.prj.programs[program].routines[routine].sheets[sheet]
        self.assertEqual(sheet.oref['1'].x, '500')
        self.assertEqual(sheet.oref['1'].y, '120')
        self.assertEqual(sheet.oref['1'].operand, 'boolean2')
        self.assertEqual(sheet.oref['1'].hide_desc, 'false')

    def test_TextBox(self):
        """Confirm Textbox Nodes are created correctly"""
        program = 'MainProgram'        
        routine = 'TestFunctionBlockRoutine'  
        sheet = '1'
     
        sheet = self.prj.programs[program].routines[routine].sheets[sheet]
        self.assertEqual(sheet.textbox['2'].x, '0')
        self.assertEqual(sheet.textbox['2'].y, '0')
        self.assertEqual(sheet.textbox['2'].text, 'Test Function Block Description On Sheet')
        self.assertEqual(sheet.textbox['2'].width, '0')

    def test_Wire(self):
        """Confirm Wire Nodes are created correctly"""
        program = 'MainProgram'        
        routine = 'TestFunctionBlockRoutine'  
        sheet = '1'
     
        sheet = self.prj.programs[program].routines[routine].sheets[sheet]
        self.assertEqual(sheet.wire['0'].fromID, '0')
        self.assertEqual(sheet.wire['0'].toID, '1')

    def test_A4SheetSize(self):
        """Confirm Sheet Size is written and read correctly"""
        program = 'MainProgram'        
        routine = 'TestFunctionBlockRoutine'  
        sheet = '1'

        self.assertEqual(self.prj.programs[program].routines[routine].sheet_size, \
                         'Letter')
        self.prj.programs[program].routines[routine].sheet_size = "A4"
        newprj = self.write_read_project()        
        self.assertEqual(newprj.programs[program].routines[routine].sheet_size, \
                         "A4")
        self.assertEqual(newprj.programs[program].routines[routine].get_child_element("FBDContent").getAttribute('SheetSize'), \
                         "A4 - 210x297 mm")        

    def write_read_project(self):
        self.prj.write('./tests/__results__/basetest_output.L5X')
        return l5x.Project('./tests/__results__/basetest_output.L5X')
        
        
if __name__ == "__main__": 
    unittest.main()