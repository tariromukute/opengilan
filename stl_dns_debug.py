# get TRex APIs
from trex_stl_lib.api import *

c = STLClient(server = '127.0.0.1')
c.connect()

port_0 = 0
port_1 = 1
try:
    c.reset(ports = [port_0, port_1])

    c.set_service_mode(ports = [port_0, port_1])

    # start a capture
    id = c.start_capture(tx_ports = [port_0], rx_ports = [port_0, port_1],
	   	         limit = 100)

    # create a base packet with scapy
    base_pkt = Ether()/IP(src="16.0.0.1",dst="48.0.0.1")/UDP(sport=1025)/DNS(rd=1, qd=DNSQR(qname='openlan.mk'))
    # create a list of 100 packets

    # inject the packets
    c.push_packets(pkts = base_pkt, ports = [port_0], force = True)

    # hold until traffic ends
    c.wait_on_traffic()

    # print the capture status so far
    status = c.get_capture_status()[id['id']]
    print("Packet Capture Status:\n{0}".format(status))

    # save the packets to PCAP
    c.stop_capture(capture_id = id['id'], output = '/tmp/pings.pcap')

except STLError as e:
    print(e)

finally:
    c.set_service_mode(ports = [port_0, port_1], enabled = False)
    c.disconnect()