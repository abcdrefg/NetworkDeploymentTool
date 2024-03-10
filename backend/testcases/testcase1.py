from pyats import aetest
from TestbedManager import TestbedManager


class R3RoutingTest(TestbedManager):

    def __init__(self):
        super().__init__()

    def start_tests(self):
        self.check_lsa_routers()

    def check_lsa_routers(self):
        r3 = self.devices["R3"]
        summary_out = r3.get_eth_ints()
        assert len(summary_out) > 0
        return True

if __name__ == '__main__':
    R3RoutingTest().start_tests()