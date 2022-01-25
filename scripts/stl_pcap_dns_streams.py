# get TRex APIs
from asyncio import streams

from trex_stl_lib.api import *
from argparse import ArgumentParser

c = STLClient(server = '127.0.0.1')
c.connect()

port_0 = 0
port_1 = 1

ports = [0, 1]

# TODO fix me. doesn't work every time
def create_steam(ip_src, ip_dst, pcap_file, link_percentage):
    vm = [
        # src                                                            <4>
        STLVmFlowVar(name="src",
                     value_list=["10.0.2.4", "10.0.3.4"],op="inc"),
        STLVmWrFlowVar(fv_name="src",pkt_offset= "IP.src"),

        # dst
        STLVmFlowVar(name="dst",
                     value_list=["10.0.2.5", "10.0.3.5"],op="inc"),
        STLVmWrFlowVar(fv_name="dst",pkt_offset= "IP.dst"),

        # checksum
        STLVmFixIpv4(offset = "IP")
    ]

    s =  STLStream(packet = STLPktBuilder(pkt=pcap_file, vm=vm), # path relative to profile and not to loader path
                         mode = STLTXCont( percentage = link_percentage ))
    
    return s

def create_vm_object(ip_src, ip_dst, link_percentage):
    vm = [
        # src                                                            <4>
        STLVmFlowVar(name="src",
                     min_value=ip_src,
                     max_value=ip_src,
                     size=4,op="inc"),
        STLVmWrFlowVar(fv_name="src",pkt_offset= "IP.src"),

        # dst
        STLVmFlowVar(name="dst",
                     min_value=ip_dst,
                     max_value=ip_dst,
                     size=4,op="inc"),
        STLVmWrFlowVar(fv_name="dst",pkt_offset= "IP.dst"),

        # checksum
        STLVmFixIpv4(offset = "IP")
    ]

    return vm

def send_dns_stream(args):
    try:
        ports = [i for i, v in enumerate(args.ip_src)]

        c.reset(ports = ports)

        
        for idx, val in enumerate(args.ip_src):
            # TODO fix me, streams are better for our use case
            # s = create_steam(val, args.ip_dst[idx], args.pcap_file, args.link_percentage)
            
            # # add the streams
            # c.add_streams(streams = [s], ports = idx)

            vm = create_vm_object(val, args.ip_dst[idx], args.link_percentage)
            
           
            # pcap packets
            c.push_pcap(args.pcap_file,             # our local PCAP file
                ports = idx,                           # use 'port'
                ipg_usec = 100,                         # IPG
                count = 1000,                              # inject only once
                vm = vm                                 # provide VM object
            )

        # start traffic with limit of args.duration in seconds (otherwise it will continue forever)
        c.start(ports = ports, duration = args.duration, force = True)

        stats = []
        

        # hold until traffic ends
        c.wait_on_traffic(ports = ports)

        stats.append(c.get_stats())

        print(stats)
        # print(c.get_stats())
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
    parser.add_argument("-t", "--duration", dest="duration",
        help="The duration of the sending in seconds",
        type=int, 
        default = 30 )
    parser.add_argument("-r", "--rate", dest="link_percentage",
        type=int,
        help="The Interface link percentage to use", 
        default = 10 )
    
    # python3 olan/stl_pcap_dns_streams.py --rate 1 -t 10 -f dns.pcap -s 10.0.3.4 -d 10.0.3.5
    args = parser.parse_args()
    send_dns_stream(args)