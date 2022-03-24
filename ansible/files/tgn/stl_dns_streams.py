# get TRex APIs
from asyncio import streams
from trex_stl_lib.api import *
from argparse import ArgumentParser
from datetime import datetime
import os 
import json


c = STLClient(server = '127.0.0.1')
c.connect()

port_0 = 0
port_1 = 1

ports = [0, 1]
def create_steam(ip_src, ip_dst, pps):
    # create a base packet with scapy
    base_pkt = Ether()/IP(src=ip_src,dst=ip_dst)/UDP(sport=1025)/DNS(rd=1, qd=DNSQR(qname='openlan.mk'))

    # later on we will use the packet builder to provide more properties
    pkt = STLPktBuilder(base_pkt)

    # create a stream with a rate of 1000 PPS and continuous
    s1 = STLStream(packet = pkt, mode = STLTXCont(pps = pps))

    return s1

def send_dns_stream(args):
    try:
        ports = [i for i, v in enumerate(args.ip_src)]

        start_time = datetime.now()
        results = {
            "ports": ports,
            "traffic": "stl_dns_pcap",
            "start_time": start_time.strftime("%d-%m-%Y %H:%M:%S"),
        }

        c.reset(ports = ports)

        
        for idx, val in enumerate(args.ip_src):

            s = create_steam(val, args.ip_dst[idx], args.pps)
            
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
        
        results["end_time"] = datetime.now()

        stats.append(c.get_stats())

        end_time = datetime.now()
        results["end_time"] = end_time.strftime("%d-%m-%Y %H:%M:%S")

        stats.append(c.get_stats())

        results["stats"] = stats

        # write the results to file
        filename = "stl_dns_streams-{}.json".format(start_time.strftime("%d-%m-%Y-%H-%M-%S"))
        f = open("{}/{}".format(args.output_folder, filename), "a")
        f.write(json.dumps(results))
        f.close()

    except STLError as e:
        print(e)

    finally:
        print(ports)
        c.set_service_mode(ports = ports, enabled = False)
        c.disconnect()

if __name__ == "__main__":
    # python3 tgn/stl_dns_streams.py -t 3 -s 10.0.2.4 -d 10.0.2.5 -s 10.0.3.4 -d 10.0.3.5 -r 10
    parser = ArgumentParser(description = 'Run TRex client API and send DNS packet',
        usage = """stl_dns_streams.py [options]""" )

    parser.add_argument("-s", "--ip_src", dest="ip_src",
        action="extend", nargs="+", type=str,
        help="The source IP address to use in the DNS packet. To provide more addresses supply the field multiple times e.g., -d <address1> -d <address2>" )
    parser.add_argument("-d", "--ip_dst", dest="ip_dst",
        action="extend", nargs="+", type=str,
        help="The dest IP address to use in the DNS packet. To provide more addresses supply the field multiple times e.g., -d <address1> -d <address2>" )
    parser.add_argument("-o", "--output-folder", dest="output_folder",
        help="The folder to write the results",
        default = "/tmp/results")
    parser.add_argument("-t", "--duration", dest="duration",
        help="The duration of the sending in seconds",
        type=int, 
        default = 30 )
    parser.add_argument("-r", "--rate", dest="pps",
        type=float,
        help="The Interface link percentage to use", 
        default = 10 )

    args = parser.parse_args()
    if not os.path.exists(args.output_folder):
        os.mkdir(args.output_folder)
    send_dns_stream(args)