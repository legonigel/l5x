"""
Tests to confirm that the program module is working correctly

When naming test cases the following format should be used.
test_<Class>_<Description>
"""
import unittest, l5x
from l5x.tests import common_testing

class ProgramCase(common_testing.DefaultCase):

    def setUp(self):
        self.prj = l5x.Project('./tests/basetest.L5X')       
                     
    def tearDown(self):        
        pass
  
    def test_Project_schema_revision(self):
        """Test set and get controller schema revision attribute"""
        self.assertEqual(self.prj.schema_revision, \
                         '1.0')
        self.prj.schema_revision = '1.1'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.schema_revision, \
                         '1.1')   

    def test_Project_target_type(self):
        """Test set and get controller target type attribute"""
        self.assertEqual(self.prj.target_type, \
                         'Controller')
        self.prj.target_type = 'Routine'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.target_type , \
                         'Routine')  

    def test_Project_contains_context(self):
        """Test set and get controller contains context attribute"""
        self.assertEqual(self.prj.contains_context, \
                         'false')
        self.prj.contains_context = 'true'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.contains_context , \
                         'true')  
        
    def test_Project_owner(self):
        """Test set and get controller Owner attribute"""
        self.assertEqual(self.prj.owner, \
                         'Default')
        self.prj.owner = 'Python'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.owner , \
                         'Python')  
        
    def test_Project_export_options(self):
        """Test set and get controller export options attribute"""
        self.assertEqual(self.prj.export_options, \
                         'DecoratedData ForceProtectedEncoding AllProjDocTrans')
        self.prj.export_options = 'No Options'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.export_options , \
                         'No Options')  
            