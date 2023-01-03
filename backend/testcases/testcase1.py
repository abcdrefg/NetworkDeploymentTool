from pyats import aetest
from TestbedManager import TestbedManager
from genie.abstract import Lookup
from genie.libs import ops
from genie.libs import parser

class R3RoutingTest(aetest.Testcase):
    @aetest.setup
    def connect(self):
        tbm = TestbedManager()
        self.testbed = tbm.create_testbed()
        self.testbed.connect()
        pass

    @aetest.test
    def check_neighbour_in_area0(self):
        r3 = self.testbed.devices["R3"]
        output = r3.parse('show ip ospf neighbor')
        assert '192.168.4.1' in output['interfaces']['FastEthernet0/0']['neighbors']

    @aetest.test
    def check_lsa_routers(self):
        r3 = self.testbed.devices["R3"]
        summary_out = r3.parse('show ip ospf database')
        assert 3 == len(summary_out['vrf']['default']['address_family']['ipv4']['instance']['1']['areas']['0.0.0.1']['database']['lsa_types'][1]['lsas'].keys())
        assert 2 == len(summary_out['vrf']['default']['address_family']['ipv4']['instance']['1']['areas']['0.0.0.0']['database']['lsa_types'][1]['lsas'].keys())

    @aetest.test
    def check_vlan(self):
        r3 = self.testbed.devices['R3']
        # vlan_brief = r3.parse('show vlans')
        # print(vlan_brief)


class R1RoutingTest(aetest.Testcase):

    @aetest.setup
    def connect(self):
        tbm = TestbedManager()
        self.testbed = tbm.create_testbed()
        self.testbed.connect()
        pass

    @aetest.test
    def check_lsa_routers(self):
        r1 = self.testbed.devices["R3"]
        summary_out = r1.parse('show ip ospf database')
        assert 3 == len(
            summary_out['vrf']['default']['address_family']['ipv4']['instance']['1']['areas']['0.0.0.1']['database'][
                'lsa_types'][1]['lsas'].keys())

    @aetest.test.loop(destination = ('192.168.1.1', '192.168.2.1', '192.168.11.1', '192.168.3.1', '192.168.4.1'))
    def test_connectivity(self, destination):
        r1_router = self.testbed.devices["R1"]
        try:
            result = r1_router.ping(destination)
        except:
            self.failed('Ping to {} failed'.format(destination))

    @aetest.test
    def check_connection_with_server(self):
        r1_router = self.testbed.devices["R1"]
        try:
            result = r1_router.ping('192.168.100.10')
        except:
            self.failed('Cannot reach server')

    @aetest.test
    def check_lag(self):
        s11 = self.testbed.devices['S11']
        ether_channel = s11.parse('show etherchannel summary')
        assert 1 == len(ether_channel['interfaces'].keys())

# class S11VlanTest(aetest.Testcase):
#
#     @aetest.setup
#     def connect(self):
#         tbm = TestbedManager()
#         self.testbed = tbm.create_testbed()
#         self.testbed.connect()
#         pass


if __name__ == '__main__':
    aetest.main()