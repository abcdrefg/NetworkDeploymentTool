from pyats import aetest
from TestbedManager import TestbedManager
class CommonSetup(aetest.Testcase):
    @aetest.setup
    def connect(self):
        devices = TestbedManager().get_devices()
        pass

    @aetest.test
    def test01(self):
        assert 1==1
    @aetest.test
    def test02(self):
        assert  2==2

if __name__ == '__main__':
    aetest.main()