"""
Tests to confirm the FBD portion is performming correctly

When naming test cases the following format should be used.
test_<Module>_<Class>_<Description>
"""
import unittest, l5x

class FBDCase(unittest.TestCase):

    def setUp(self):
        self.prj = l5x.Project('./tests/basetest.L5X')       
                     
    def tearDown(self):        
        pass
    
    def test_net_object_Iref_attributes_present(self):
        """Confirm Iref Nodes are created correctly"""
        program = 'MainProgram'        
        routine = 'TestFunctionBlockRoutine'  
        sheet = '1'
      
        iref = self.prj.programs[program].routines[routine].sheets[sheet].blocks['0']
        self.assertEqual(iref.x, '160')
        self.assertEqual(iref.y, '120')
        self.assertEqual(iref.operand, 'boolean1')
        self.assertEqual(iref.hide_desc, 'false')
        
    def test_net_object_Oref_attributes_present(self):
        """Confirm Oref Nodes are created correctly"""
        program = 'MainProgram'        
        routine = 'TestFunctionBlockRoutine'  
        sheet = '1'
     
        oref = self.prj.programs[program].routines[routine].sheets[sheet].blocks['1']
        self.assertEqual(oref.x, '500')
        self.assertEqual(oref.y, '120')
        self.assertEqual(oref.operand, 'boolean2')
        self.assertEqual(oref.hide_desc, 'false')

    def test_net_object_Textbox_attributes_present(self):
        """Confirm Textbox Nodes are created correctly"""
        program = 'MainProgram'        
        routine = 'TestFunctionBlockRoutine'  
        sheet = '1'
     
        textbox = self.prj.programs[program].routines[routine].sheets[sheet].blocks['2']
        self.assertEqual(textbox.x, '0')
        self.assertEqual(textbox.y, '0')
        self.assertEqual(textbox.text, 'Test Function Block Description On Sheet')
        self.assertEqual(textbox.width, '0')
        self.assertTrue(type(textbox) is l5x.net_object.FBD_TextBox)

    def test_net_object_Wire_attributes_present(self):
        """Confirm Wire Nodes are created correctly"""
        program = 'MainProgram'        
        routine = 'TestFunctionBlockRoutine'  
        sheet = '1'
     
        sheet = self.prj.programs[program].routines[routine].sheets[sheet]
        self.assertEqual(sheet.wire['0'].fromID, '0')
        self.assertEqual(sheet.wire['0'].toID, '1')

    def test_program_SheetSize_read_write(self):
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
        
    def test_program_SheetOrientation_read_write(self):
        """Confirm Sheet Size is written and read correctly"""
        program = 'MainProgram'        
        routine = 'TestFunctionBlockRoutine'  
        sheet = '1'

        self.assertEqual(self.prj.programs[program].routines[routine].sheet_orientation, \
                         'Landscape')
        self.prj.programs[program].routines[routine].sheet_orientation = "Portrait"
        newprj = self.write_read_project()        
        self.assertEqual(newprj.programs[program].routines[routine].sheet_orientation, \
                         "Portrait")        

    def write_read_project(self):
        self.prj.write('./tests/__results__/basetest_output.L5X')
        return l5x.Project('./tests/__results__/basetest_output.L5X')
        
        
if __name__ == "__main__": 
    unittest.main()