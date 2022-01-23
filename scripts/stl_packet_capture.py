# get TRex APIs
from trex_stl_lib.api import *

c = STLClient(server = '127.0.0.1')
c.connect()

port_0 = 0
port_1 = 1
try:
    c.acquire(ports = [port_0, port_1])

    c.set_service_mode(ports = [port_0, port_1])

    # start a capture
    id = c.start_capture(tx_ports = [port_0], rx_ports = [port_1],
	   	         limit = 100)

    # generate some ping packets from port 0 to port 1 with 200 bytes
    c.ping_ip(src_port = port_0, dst_ip = '10.0.2.5', pkt_size = 200, count = 5)

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