import unittest, l5x
from l5x.tests.basetest import BaseTest
from l5x.tests.controllersetgettest import ControllerSetGetTest
from l5x.tests.fbdtest import FBDCase
from l5x.tests.program_test import ProgramCase
from l5x.program import *

class CreateTest():
    
    @classmethod
    def common_setup(cls):
        prj = l5x.Project()
        prj.controller.target_name = 'CreateTestName'
        prj.controller.slot = '2'
        prj.controller.processor_type = '1756-L75'
        prj.controller.major_revision = '20'
        prj.controller.minor_revision = '11'
        prj.controller.description = 'Base test project to be used with l5x python package'
        prj.modules['Local'].ports[1].address = '4'
        program = prj.programs['MainProgram']
        RLLRoutine.create(program, 'TestLadderRoutine')       
        FBDRoutine.create(program, 'TestFunctionBlockRoutine')
        SFCRoutine.create(program, 'TestSeqFunctionChartRoutine')   
        STRoutine.create(program, 'TestStructuredTextRoutine') 
        program.description = 'Test Program Description'
        
        routine = program.routines['TestLadderRoutine'] 
        Rung.create(routine, 'XIC(boolean1)OTE(boolean2);')
        Rung.create(routine, 'XIC(boolean1)OTE(boolean2);')
        Rung.create(routine, 'XIC(boolean1)OTE(boolean2);')
        
        routine = program.routines['MainRoutine']
        Rung.create(routine, 'JSR(TestFunctionBlockRoutine,0);')
        Rung.create(routine, 'JSR(TestSeqFunctionChartRoutine,0);')
        Rung.create(routine, 'JSR(TestLadderRoutine,0);')
        Rung.create(routine, 'JSR(TestStructuredTextRoutine,0);')
        
        routine = program.routines['TestFunctionBlockRoutine']        
        routine.description = 'Test Function Block Routine'
        sheet = Sheet.create(routine)
        iref = FBD_IRef.create(sheet, 'boolean1', 160, 120)
        oref = FBD_ORef.create(sheet, 'boolean2', 500, 120)        
        Wire.create(sheet, iref, oref)
        FBD_TextBox.create(sheet, 'Test Function Block Description On Sheet')
        
        #Create tags
        Tag.create(prj.controller, prj, 'Base', 'boolean1', 'BOOL', 1, 'Test Boolean 1')
        Tag.create(prj.controller, prj, 'Base', 'real1', 'REAL', 0.4, 'Test Real 1')
        Tag.create(prj.controller, prj, 'Base', 'dint1', 'DINT', 1, 'Test DINT 1')
        Tag.create(program, prj, 'Base', 'boolean2', 'BOOL', 1, 'Test Boolean 2')
        
        #Create alias tag
        Tag.create(prj.controller, prj, 'Base', 'dint1', 'DINT', 1, 'Test DINT 1')
        return prj

class CreateBaseTest(BaseTest):
    def setUp(self):
        self.prj = CreateTest.common_setup()
        
    def write_read_project(self):
        self.prj.write('./tests/__results__/createtest_output.L5X')
        return l5x.Project('./tests/__results__/createtest_output.L5X')

class CreateControllerSetGetTest(ControllerSetGetTest):
    def setUp(self):
        self.prj = CreateTest.common_setup()
        
    def write_read_project(self):
        self.prj.write('./tests/__results__/createtest_output.L5X')
        return l5x.Project('./tests/__results__/createtest_output.L5X')
    
class CreateControllerSetGetTest(FBDCase):
    def setUp(self):
        self.prj = CreateTest.common_setup()
        
    def write_read_project(self):
        self.prj.write('./tests/__results__/createtest_output.L5X')
        return l5x.Project('./tests/__results__/createtest_output.L5X')

