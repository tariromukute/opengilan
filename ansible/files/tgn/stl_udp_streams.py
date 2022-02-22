# get TRex APIs
from trex_stl_lib.api import *

c = STLClient(server = '127.0.0.1')
c.connect()

port_0 = 0
port_1 = 1
try:
    # create a base pkt
    base_pkt = Ether()/IP(src="16.0.0.1",dst="48.0.0.1")/UDP(dport=12,sport=1025)

    # create an empty VM object
    vm = STLVM()

    # add a var field matching the src IPv4 field
    vm.var(name = 'src_ipv4', min_value = '16.0.0.1',
           max_value = '16.0.0.255', size = 4,
	   step = 1, op = 'inc')

    # add a command to write the packet to IPv4 src field offset
    vm.write(fv_name = 'src_ipv4', pkt_offset = 'IP.src')

    # provide both the base packet and the VM object
    pkt = STLPktBuilder(base_pkt, vm = vm)

    # create a stream with a rate of 1000 PPS and continuous
    s1 = STLStream(packet = pkt, mode = STLTXCont(pps = 1000))

    # prepare the ports
    c.reset(ports = [port_0, port_1])

    # add the streams
    c.add_streams(s1, ports = port_0)

    # start traffic with limit of 3 seconds (otherwise it will continue forever)
    c.start(ports = port_0, duration = 30)

    # hold until traffic ends
    c.wait_on_traffic()


except STLError as e:
    print(e)

finally:

    c.disconnect()