from TestbedManager import TestbedManager
from pyats import aetest, topology
import sys
import argparse
from TestbedManager import TestbedManager
class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect(self):
        devices = TestbedManager().get_devices()
        pass

    @aetest.test
    def test01(self):
        assert 0 == 1

    def test02(self):
        assert  1==1

if __name__ == '__main__':
    aetest.main()