# get TRex APIs
from trex_stl_lib.api import *
from argparse import ArgumentParser

c = STLClient(server = '127.0.0.1')
c.connect()

port_0 = 0
port_1 = 1

def send_dns_packet(args):
    try:
        c.reset(ports = [port_0, port_1])

        c.set_service_mode(ports = [port_0, port_1])

        # start a capture
        id = c.start_capture(tx_ports = [port_0], rx_ports = [port_0, port_1],
                    limit = 100)

        # create a base packet with scapy
        base_pkt = Ether()/IP(src=args.ip_src,dst=args.ip_dst)/UDP(sport=1025)/DNS(rd=1, qd=DNSQR(qname='openlan.mk'))
        # create a list of 100 packets

        # inject the packets
        c.push_packets(pkts = base_pkt, ports = [port_0], force = True)

        # hold until traffic ends
        c.wait_on_traffic()

        # print the capture status so far
        status = c.get_capture_status()[id['id']]
        print("Packet Capture Status:\n{0}".format(status))

        # save the packets to PCAP
        c.stop_capture(capture_id = id['id'], output = '/tmp/dns.pcap')

    except STLError as e:
        print(e)

    finally:
        c.set_service_mode(ports = [port_0, port_1], enabled = False)
        c.disconnect()

if __name__ == "__main__":
    parser = ArgumentParser(description = 'Run TRex client API and send DNS packet',
        usage = """stl_dns_debug.py [options]""" )

    parser.add_argument("-s", "--ip_src", dest="ip_src",
        help="The source IP address to use in the DNS packet", 
        default = '10.0.2.4' )
    parser.add_argument("-d", "--ip_dst", dest="ip_dst",
        help="The dest IP address to use in the DNS packet", 
        default = '10.0.2.5' )

    args = parser.parse_args()
    send_dns_packet(args)