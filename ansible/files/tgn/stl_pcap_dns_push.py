# get TRex APIs
from asyncio import streams

from trex_stl_lib.api import *
from argparse import ArgumentParser
from datetime import datetime
import os 
import json
import math

c = STLClient(server = '127.0.0.1')
c.connect()

port_0 = 0
port_1 = 1

ports = [0, 1]

# TODO implment streams. doesn't work every time

def create_vm_object(ip_src, ip_dst):
    vm = [
        # src                                                            <4>
        STLVmFlowVar(name="src",
                     value_list=[ip_src],op="inc"),
        STLVmWrFlowVar(fv_name="src",pkt_offset= "IP.src"),

        # dst
        STLVmFlowVar(name="dst",
                     value_list=[ip_dst],op="inc"),
        STLVmWrFlowVar(fv_name="dst",pkt_offset= "IP.dst"),

        # checksum
        STLVmFixIpv4(offset = "IP")
    ]

    return vm

def push_dns_packets(args):
    try:
        ports = [i for i, v in enumerate(args.ip_src)]

        start_time = datetime.now()
        results = {
            "ports": ports,
            "traffic": "stl_dns_pcap",
            "start_time": start_time.strftime("%d-%m-%Y %H:%M:%S"),
        }

        c.reset(ports = ports)

        ipg_usec = 1000000 / args.pps
        packets = rdpcap(args.pcap_file)
        pkt_count = len(packets)
        count = max(1, math.ceil((args.pps / pkt_count) * args.duration))

        for idx, val in enumerate(args.ip_src):

            vm = create_vm_object(val, args.ip_dst[idx])
            
           
            # pcap packets
            c.push_pcap(args.pcap_file,             # our local PCAP file
                ports = idx,                           # use 'port'
                ipg_usec = ipg_usec,                         # IPG
                count = count,                              # inject only once
                duration=args.duration,
                vm = vm                                 # provide VM object
            )

        stats = []
        

        # hold until traffic ends
        c.wait_on_traffic(ports = ports)

        results["end_time"] = datetime.now()

        stats.append(c.get_stats())

        end_time = datetime.now()
        results["end_time"] = end_time.strftime("%d-%m-%Y %H:%M:%S")

        stats.append(c.get_stats())

        results["stats"] = stats

        # write the results to file
        filename = "stl_pcap_dns_push-{}.json".format(start_time.strftime("%d-%m-%Y-%H-%M-%S"))
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
    parser = ArgumentParser(description = 'Run TRex client API and send DNS packet',
        usage = """stl_dns_debug.py [options]""" )

    parser.add_argument("-s", "--ip_src", dest="ip_src",
        action="extend", nargs="+", type=str,
        help="The source IP address to use in the DNS packet. To provide more addresses supply the field multiple times e.g., -d <address1> -d <address2>" )
    parser.add_argument("-d", "--ip_dst", dest="ip_dst",
        action="extend", nargs="+", type=str,
        help="The dest IP address to use in the DNS packet. To provide more addresses supply the field multiple times e.g., -d <address1> -d <address2>" )
    parser.add_argument("-f", "--file", dest="pcap_file",
        help="The pcap file to generate streams from")
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
        default = 10)
    
    # python3 tgn/stl_pcap_dns_push.py -t 3 -f /tmp/rx_dns.pcap -s 10.0.2.4 -d 10.0.2.5 -r 10
    args = parser.parse_args()
    if not os.path.exists(args.output_folder):
        os.mkdir(args.output_folder)
     
    push_dns_packets(args)