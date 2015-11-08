import unittest, l5x
from l5x.tests import common_testing

class CreateTest(common_testing.DefaultCase):

    def setUp(self):
        self.prj = l5x.Project()       
                     
    def tearDown(self):        
        pass
    
    def test_OpenProject(self):
        """Confirm test l5x file can be opened"""        
        self.assertTrue(self.prj != None)
    
    def test_project_create(self):
        """Confirm a new project can be created with default settings"""     
        self.assertEqual(self.prj.controller.target_name, \
                         '')
    
    def test_create_Controller(self):
        self.assertEqual(self.prj.controller.time_slice, \
                 '20')
        
    def test_controller_name_create(self):
        self.assertEqual(self.prj.controller.target_name, \
                 '')
        self.prj.controller.target_name = 'CreateTestName'
        self.prj.controller.slot = '2'
        self.prj.controller.processor_type = '1756-L75'
        self.prj.controller.major_revision = '20'
        self.prj.controller.minor_revision = '11'
        self.prj.modules['Local'].ports[1].address = '4'
        self.write_read_project()
        

    def write_read_project(self):
        self.prj.write('./tests/__results__/createtest_output.L5X')
        return l5x.Project('./tests/__results__/createtest_output.L5X')

