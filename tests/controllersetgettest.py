'''
Created on 3rd Nov 2015

@author: hutcheb
'''
import unittest, l5x
from l5x.tests import common_testing

class ControllerSetGetTest(common_testing.DefaultCase):

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
        self.assertEqual(self.prj.controller.description, \
                         'Base test project to be used with l5x python package')
        self.prj.controller.description = 'Controller Description'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.description, \
                         'Controller Description')   
    
    def test_controller_use(self):
        """Test set and get controller use attribute"""
        self.assertEqual(self.prj.controller.use, \
                         'Target')
        self.prj.controller.use = 'Base'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.use, \
                         'Base')  
        
    def test_controller_processor_type(self):
        """Test set and get controller ProcessorType attribute
        
        Note that it gets written to two place. Within the module named local 
        as well as the processortype attribute of the Controller element"""
        self.assertEqual(self.prj.controller.processor_type, \
                         '1756-L75')
        self.prj.controller.processor_type = '1756-L73'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.processor_type, \
                         '1756-L73')  
        self.assertEqual(newprj.modules['Local'].element.getAttribute('CatalogNumber'), \
                         '1756-L73', \
                         'Checking Module CatalogNumber attribute')
        
    def test_controller_major_revision(self):
        """Test set and get controller MajorRev attribute
        
        Note that it gets written to two place. Within the module named local 
        as well as the MajorRev attribute of the Controller element"""
        self.assertEqual(self.prj.controller.major_revision, \
                         '20')
        self.prj.controller.major_revision = '19'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.major_revision, \
                         '19') 
        self.assertEqual(newprj.modules['Local'].element.getAttribute('Major'), \
                         '19', \
                         'Checking Module Major attribute')
        self.assertEqual(newprj.element.getAttribute('SoftwareRevision'), \
                         '19' + ".01", \
                         'Checking RSLogix Major attribute')
       
    def test_controller_minor_revision(self):
        """Test set and get controller MinorRev attribute
        
        Note that it gets written to two place. Within the module named local 
        as well as the MinorRev attribute of the Controller element"""
        self.assertEqual(self.prj.controller.minor_revision, \
                         '11')
        self.prj.controller.minor_revision = '12'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.minor_revision, \
                         '12') 
        self.assertEqual(newprj.modules['Local'].element.getAttribute('Minor'), \
                         '12', \
                         'Checking Module Minor attribute')
        self.assertEqual(newprj.element.getAttribute('SoftwareRevision'), \
                         "20." + '12', \
                         'Checking RSLogix Minor attribute')
          
    def test_controller_time_slice(self):
        """Test set and get controller time_slice attribute"""
        self.assertEqual(self.prj.controller.time_slice, \
                         '20')
        self.prj.controller.time_slice = '50'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.time_slice, \
                         '50') 

        
    def test_controller_share_unused_time_slice(self):
        """Test set and get controller share_unused_time_slice attribute"""
        self.assertEqual(self.prj.controller.share_unused_time_slice, \
                         '1')
        self.prj.controller.share_unused_time_slice = '0'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.share_unused_time_slice, \
                         '0') 
    
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
        self.assertEqual(self.prj.controller.sfc_execution_control, \
                         'CurrentActive')
        self.prj.controller.sfc_execution_control = 'LastActive'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.sfc_execution_control, \
                         'LastActive') 
    
    def test_controller_sfc_restart_position(self):
        """Test set and get controller sfc_restart_position attribute"""
        self.assertEqual(self.prj.controller.sfc_restart_position, \
                         'MostRecent')
        self.prj.controller.sfc_restart_position = 'Start'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.sfc_restart_position, \
                         'Start') 
        
    def test_controller_sfc_last_scan(self):
        """Test set and get controller sfc_last_scan attribute"""
        self.assertEqual(self.prj.controller.sfc_last_scan, \
                         'DontScan')
        self.prj.controller.sfc_last_scan = 'Scan'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.sfc_last_scan, \
                         'Scan') 
    
    def test_controller_project_sn(self):
        """Test set and get controller project_sn attribute"""
        self.assertEqual(self.prj.controller.project_sn, \
                         '16#0000_0000')
        self.prj.controller.project_sn = '16#0101_0101'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.project_sn, \
                         '16#0101_0101') 
    
    def test_controller_match_project_to_controller(self):
        """Test set and get controller match_project_to_controller attribute"""
        self.assertEqual(self.prj.controller.match_project_to_controller, \
                         'false')
        self.prj.controller.match_project_to_controller = 'true'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.match_project_to_controller, \
                         'true')
    
    def test_controller_can_use_rpi_from_producer(self):
        """Test set and get controller can_use_rpi_from_producer attribute"""  
        self.assertEqual(self.prj.controller.can_use_rpi_from_producer, \
                         'false')
        self.prj.controller.can_use_rpi_from_producer = 'true'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.can_use_rpi_from_producer, \
                         'true') 

    def test_controller_inhibit_automatic_firmware_update(self):
        """Test set and get controller inhibit_automatic_firmware_update attribute"""
        self.assertEqual(self.prj.controller.inhibit_automatic_firmware_update, \
                         '0')
        self.prj.controller.inhibit_automatic_firmware_update = '1'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.inhibit_automatic_firmware_update, \
                         '1')  
        
    def test_controller_redundancy_enabled(self):
        """Test set and get controller redundancy_enabled attribute"""
        self.assertEqual(self.prj.controller.redundancy_enabled, \
                         'false')
        self.prj.controller.redundancy_enabled = 'true'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.redundancy_enabled, \
                         'true')  

    def test_controller_redundancy_keep_test_edits_on_switchover(self):
        """Test set and get controller redundancy_keep_test_edits_on_switchover attribute"""
        self.assertEqual(self.prj.controller.redundancy_keep_test_edits_on_switchover, \
                         'false')
        self.prj.controller.redundancy_keep_test_edits_on_switchover = 'true'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.redundancy_keep_test_edits_on_switchover, \
                         'true')  
        
    def test_controller_redundancy_io_memory_pad_percentage(self):
        """Test set and get controller redundancy_io_memory_pad_percentage attribute"""
        self.assertEqual(self.prj.controller.redundancy_io_memory_pad_percentage, \
                         '90')
        self.prj.controller.redundancy_io_memory_pad_percentage = '80'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.redundancy_io_memory_pad_percentage, \
                         '80')  

    def test_controller_redundancy_datatable_pad_percentage(self):
        """Test set and get controller redundancy_datatable_pad_percentage attribute"""
        self.assertEqual(self.prj.controller.redundancy_datatable_pad_percentage, \
                         '50')
        self.prj.controller.redundancy_datatable_pad_percentage = '60'
        newprj = self.write_read_project()        
        self.assertEqual(newprj.controller.redundancy_datatable_pad_percentage, \
                         '60')   

        
if __name__ == "__main__": 
    unittest.main()