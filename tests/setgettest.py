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
    
    def test_controller_comm_path(self):
        """Test set and get comm path"""
        comm_path = 'AB_ETHIP-1\\192.168.1.10\\Backplane\\0'
        self.prj.controller.comm_path = comm_path
        newprj = self.write_read_project()
        self.assertEqual(self.prj.controller.comm_path, comm_path)
     
    def test_controller_description(self):
        """Test set and get controller description"""
        description = 'Controller Description'        
        self.assertEqual(self.prj.controller.description, \
                         'Base test project to be used with l5x python package')
        self.prj.controller.description = description
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.description, \
                         description)
    
    def test_controller_use(self):
        """Test set and get controller use attribute"""
        attribute = 'Base'        
        self.assertEqual(self.prj.controller.use, 'Target')
        self.prj.controller.use = attribute
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.use, \
                         attribute)
        
    def test_controller_processor_type(self):
        """Test set and get controller ProcessorType attribute
        
        Note that it gets written to two place. Within the module named local 
        as well as the processortype attribute of the Controller element"""
        attribute = '1756-L73'        
        self.assertEqual(self.prj.controller.processor_type, '1756-L75')
        self.assertEqual(self.prj.modules['Local'].catalog_number, '1756-L75')
        self.prj.controller.processor_type = attribute
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.processor_type, \
                         attribute, \
                         'Checking ProcessorType Attribute')
        self.assertEqual(newprj.modules['Local'].catalog_number, \
                         attribute, \
                         'Checking Module CatalogNumber attribute')
        
    def test_controller_major_revision(self):
        """Test set and get controller MajorRev attribute
        
        Note that it gets written to two place. Within the module named local 
        as well as the MajorRev attribute of the Controller element"""
        attribute = '19'        
        self.assertEqual(self.prj.controller.major_revision, '20')
        self.assertEqual(self.prj.modules['Local'].major, '20')
        self.prj.controller.major_revision = attribute
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.major_revision, \
                         attribute, \
                         'Checking MajorRev Attribute')
        self.assertEqual(newprj.modules['Local'].major, \
                         attribute, \
                         'Checking Module Major attribute')
       
    def test_controller_minor_revision(self):
        """Test set and get controller MinorRev attribute
        
        Note that it gets written to two place. Within the module named local 
        as well as the MinorRev attribute of the Controller element"""
        attribute = '12'        
        self.assertEqual(self.prj.controller.minor_revision, '11')
        self.assertEqual(self.prj.modules['Local'].minor, '11')
        self.prj.controller.minor_revision = attribute
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.minor_revision, \
                         attribute, \
                         'Checking MinorRev Attribute')
        self.assertEqual(newprj.modules['Local'].minor, \
                         attribute, \
                         'Checking Module Minor attribute')
          
    def test_controller_time_slice(self):
        """Test set and get controller time_slice attribute"""
        attribute = '50'        
        self.assertEqual(self.prj.controller.time_slice, '20')
        self.prj.controller.time_slice = attribute
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.time_slice, \
                         attribute)
        
    def test_controller_share_unused_time_slice(self):
        """Test set and get controller share_unused_time_slice attribute"""
        attribute = '0'        
        self.assertEqual(self.prj.controller.share_unused_time_slice, '1')
        self.prj.controller.share_unused_time_slice = attribute
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.share_unused_time_slice, \
                         attribute)
    
    def test_controller_project_creation_date(self):
        """Test set and get controller project_creation_date attribute"""
        attribute = 'Mon Oct 01 01:02:03 2022'
        self.prj.controller.project_creation_date = attribute
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.project_creation_date, \
                         attribute)
        
    def test_controller_last_modified_date(self):
        """Test set and get controller last_modified_date attribute"""
        attribute = 'Mon Oct 01 01:02:03 2022'
        self.prj.controller.last_modified_date = attribute
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.last_modified_date, \
                         attribute)    
    
    def test_controller_sfc_execution_control(self):
        """Test set and get controller sfc_execution_control attribute"""
        attribute = 'LastActive'        
        self.assertEqual(self.prj.controller.sfc_execution_control, 'CurrentActive')
        self.prj.controller.sfc_execution_control = attribute
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.sfc_execution_control, \
                         attribute)
    
    def test_controller_sfc_restart_position(self):
        """Test set and get controller sfc_restart_position attribute"""
        attribute = 'Start'        
        self.assertEqual(self.prj.controller.sfc_restart_position, 'MostRecent')
        self.prj.controller.sfc_restart_position = attribute
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.sfc_restart_position, \
                         attribute)
        
    def test_controller_sfc_last_scan(self):
        """Test set and get controller sfc_last_scan attribute"""
        attribute = 'Scan'        
        self.assertEqual(self.prj.controller.sfc_last_scan, 'DontScan')
        self.prj.controller.sfc_last_scan = attribute
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.sfc_last_scan, \
                         attribute)
    
    def test_controller_project_sn(self):
        """Test set and get controller project_sn attribute"""
        attribute = '16#0101_0101'        
        self.assertEqual(self.prj.controller.project_sn, '16#0000_0000')
        self.prj.controller.project_sn = attribute
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.project_sn, \
                         attribute)
    
    def test_controller_match_project_to_controller(self):
        """Test set and get controller match_project_to_controller attribute"""
        attribute = 'true'        
        self.assertEqual(self.prj.controller.match_project_to_controller, 'false')
        self.prj.controller.match_project_to_controller = attribute
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.match_project_to_controller, \
                         attribute)
    
    def test_controller_can_use_rpi_from_producer(self):
        """Test set and get controller can_use_rpi_from_producer attribute"""
        attribute = 'true'        
        self.assertEqual(self.prj.controller.can_use_rpi_from_producer, 'false')
        self.prj.controller.can_use_rpi_from_producer = attribute
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.can_use_rpi_from_producer, \
                         attribute)        

    def test_controller_inhibit_automatic_firmware_update(self):
        """Test set and get controller inhibit_automatic_firmware_update attribute"""
        attribute = '1'        
        self.assertEqual(self.prj.controller.inhibit_automatic_firmware_update, '0')
        self.prj.controller.inhibit_automatic_firmware_update = attribute
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.inhibit_automatic_firmware_update, \
                         attribute)
        
    def write_read_project(self):
        self.prj.write('./tests/__results__/basetest_output.L5X')
        return l5x.Project('./tests/__results__/basetest_output.L5X')
        
        
if __name__ == "__main__": 
    unittest.main()