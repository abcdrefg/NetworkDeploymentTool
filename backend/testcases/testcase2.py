from TestbedManager import TestbedManager
from pyats import aetest, topology
import sys
import argparse
from TestbedManager import TestbedManager
class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect(self):
        tbm = TestbedManager()
        self.testbed = tbm.create_testbed()
        self.testbed.connect()
        pass

class testcase01(aetest.Testcase):
    @aetest.test
    def test01(self):
        assert 0 == 1

if __name__ == '__main__':
    aetest.main()