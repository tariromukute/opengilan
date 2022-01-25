# get TRex APIs
from asyncio import streams
from trex_stl_lib.api import *
from argparse import ArgumentParser

c = STLClient(server = '127.0.0.1')
c.connect()

port_0 = 0
port_1 = 1

ports = [0, 1]
def create_steam(ip_src, ip_dst, link_percentage):
    # create a base packet with scapy
    base_pkt = Ether()/IP(src=ip_src,dst=ip_dst)/UDP(sport=1025)/DNS(rd=1, qd=DNSQR(qname='openlan.mk'))

    # later on we will use the packet builder to provide more properties
    pkt = STLPktBuilder(base_pkt)

    # create a stream with a rate of 1000 PPS and continuous
    s1 = STLStream(packet = pkt, mode = STLTXCont(percentage = link_percentage))

    return s1

def send_dns_stream(args):
    try:
        ports = [i for i, v in enumerate(args.ip_src)]

        c.reset(ports = ports)

        
        for idx, val in enumerate(args.ip_src):

            s = create_steam(val, args.ip_dst[idx], args.link_percentage)
            
            # add the streams
            c.add_streams(streams = [s], ports = idx)

        # start traffic with limit of 3 seconds (otherwise it will continue forever)
        c.start(ports = ports, duration = args.duration, force = True)

        stats = []
        while c.is_traffic_active():
            stats.append(c.get_stats())
            c.clear_stats()
            time.sleep(5)

        # hold until traffic ends
        c.wait_on_traffic(ports = ports)

        print(stats)

    except STLError as e:
        print(e)

    finally:
        print(ports)
        c.set_service_mode(ports = ports, enabled = False)
        c.disconnect()

if __name__ == "__main__":
    parser = ArgumentParser(description = 'Run TRex client API and send DNS packet',
        usage = """stl_dns_debug.py [options]""" )

    parser.add_argument("-s", "--ip_src", dest="ip_src",
        action="extend", nargs="+", type=str,
        help="The source IP address to use in the DNS packet. To provide more addresses supply the field multiple times e.g., -d <address1> -d <address2>" )
    parser.add_argument("-d", "--ip_dst", dest="ip_dst",
        action="extend", nargs="+", type=str,
        help="The dest IP address to use in the DNS packet. To provide more addresses supply the field multiple times e.g., -d <address1> -d <address2>" )
    parser.add_argument("-t", "--duration", dest="duration",
        help="The duration of the sending in seconds",
        type=int, 
        default = 30 )
    parser.add_argument("-r", "--rate", dest="link_percentage",
        type=int,
        help="The Interface link percentage to use", 
        default = 10 )

    args = parser.parse_args()
    send_dns_stream(args)