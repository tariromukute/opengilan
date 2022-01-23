# get TRex APIs
from trex_stl_lib.api import *

c = STLClient(server = '127.0.0.1')
c.connect()

port_0 = 0
port_1 = 1
try:
    # create a base pkt
    base_pkt =  Ether()/IP()/UDP(sport=1025)/DNS(rd=1, qd=DNSQR(qname='openlan.mk'))

    # later on we will use the packet builder to provide more properties
    pkt = STLPktBuilder(base_pkt)

    # create a stream with a rate of 1000 PPS and continuous
    s1 = STLStream(packet = pkt, mode = STLTXCont(pps = 1000))

    # prepare the ports
    c.reset(ports = [port_0, port_1])

    c.set_service_mode(ports = port_0)

    id = c.start_capture(tx_ports = [port_0, port_1], rx_ports = [port_0, port_1],
	   	         limit = 100, bpf_filter = 'udp or arp')
    
    status = c.get_capture_status()[id['id']]
    print("Packet Capture Status:\n{0}".format(status))

    # add the streams
    c.add_streams(s1, ports = port_0)

    # start traffic with limit of 3 seconds (otherwise it will continue forever)
    c.start(ports = port_0, duration = 3)

    # hold until traffic ends
    c.wait_on_traffic()

    # save the packets to PCAP
    c.stop_capture(capture_id = id['id'], output = '/tmp/dns.pcap')

except STLError as e:
    print(e)

finally:
    c.set_service_mode(ports = [port_0, port_1], enabled = False)
    c.disconnect()