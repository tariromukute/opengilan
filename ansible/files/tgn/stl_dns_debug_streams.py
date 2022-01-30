# get TRex APIs
from asyncio import streams
from trex_stl_lib.api import *
from argparse import ArgumentParser

c = STLClient(server = '127.0.0.1')
c.connect()

port_0 = 0
port_1 = 1
def send_dns_stream(args):
    try:
        c.reset(ports = [port_0, port_1])

        c.set_service_mode(ports = [port_0, port_1])

        # start a capture
        tx_capture = c.start_capture(tx_ports = [port_0],
                    limit = 10)

        rx_capture = c.start_capture(rx_ports = [port_0],
                    limit = 10)

        
        # create a base packet with scapy
        base_pkt = Ether()/IP(src=args.ip_src,dst=args.ip_dst)/UDP(sport=1025)/DNS(rd=1, qd=DNSQR(qname='openlan.mk'))

        # later on we will use the packet builder to provide more properties
        pkt = STLPktBuilder(base_pkt)

        # create a stream with a rate of 1000 PPS and continuous
        s1 = STLStream(packet = pkt, mode = STLTXCont(pps = 1000))

        # add the streams
        c.add_streams(streams = [s1], ports = port_0)

        # start traffic with limit of 3 seconds (otherwise it will continue forever)
        c.start(ports = port_0, duration = 10, force = True)

        # hold until traffic ends
        c.wait_on_traffic(ports = port_0)

        # check out the stats
        stats = c.get_stats()

        # examine stats for port_0
        print("port_0 stats:")
        print(stats[port_0])

        # examine stats for port_1
        print("port_1 stats:")
        print(stats[port_1])

        # print the capture status so far
        tx_status = c.get_capture_status()[tx_capture['id']]
        print("TX Packet Capture Status:\n{0}".format(tx_status))

        rx_status = c.get_capture_status()[rx_capture['id']]
        print("RX Packet Capture Status:\n{0}".format(rx_status))

        # save the packets to PCAP
        c.stop_capture(capture_id = tx_status['id'], output = '/tmp/tx_dns.pcap')

        c.stop_capture(capture_id = rx_status['id'], output = '/tmp/rx_dns.pcap')

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
    send_dns_stream(args)