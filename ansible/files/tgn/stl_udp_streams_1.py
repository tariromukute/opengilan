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

ip_range = {'src': {'start': "16.0.0.1", 'end': "16.0.0.254"},
                'dst': {'start': "48.0.0.1",  'end': "48.0.0.254"}}

# default IMIX properties
imix_table = [  {'size': 1514, 'pps': 800000,   'isg':0 },
                    {'size': 68,   'pps': 28,  'isg':0.2 },
                    {'size': 590,  'pps': 16,  'isg':0.1 } ]


def create_stream (size, pps, isg, vm ):
    # Create base packet and pad it to size
    base_pkt = Ether()/IP()/UDP(chksum=0)
    pad = max(0, size - len(base_pkt)) * 'x'

    pkt = STLPktBuilder(pkt = base_pkt/pad,
                        vm = vm)

    # create a stream with a rate of 1000 PPS and continuous
    return STLStream(isg = isg,
                        packet = pkt,
                        mode = STLTXCont(pps = pps))


def get_streams(direction):
    if direction == 0:
        src = ip_range['src']
        dst = ip_range['dst']
    else:
        src = ip_range['dst']
        dst = ip_range['src']

    # construct the base packet for the profile
    vm = STLVM()
    
    # define two vars (src and dst)
    vm.var(name="src",min_value=src['start'],max_value=src['end'],size=4,op="inc")
    vm.var(name="dst",min_value=dst['start'],max_value=dst['end'],size=4,op="inc")
    
    # write them
    vm.write(fv_name="src",pkt_offset= "IP.src")
    vm.write(fv_name="dst",pkt_offset= "IP.dst")
    
    # fix checksum
    vm.fix_chksum()
    
    # create imix streams
    # return [create_stream(x['size'], x['pps'],x['isg'] , vm) for x in imix_table]
    return create_stream(1514, 800000, 0, vm)

def send_udp_stream(args):
    try:
        # ports = [i for i, v in enumerate(args.ip_src)]

        start_time = datetime.now()
        results = {
            "ports": ports,
            "traffic": "stl_dns_pcap",
            "start_time": start_time.strftime("%d-%m-%Y %H:%M:%S"),
        }

        c.reset(ports = ports)
        
        # for idx, val in enumerate(args.ip_src):

        #     s = create_steam(val, args.ip_dst[idx], args.link_percentage)
            
        #     # add the streams
        #     c.add_streams(streams = [s], ports = idx)
        ss = get_streams(0)
        c.add_streams(streams = ss, ports = 0)
        # start traffic with limit of 3 seconds (otherwise it will continue forever)
        c.start(ports = port_0, duration = args.duration, force = True)

        stats = []
        # while c.is_traffic_active():
        #     stats.append(c.get_stats())
        #     c.clear_stats()
        #     time.sleep(5)

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
    # python3 tgn/stl_udp_streams_1.py -t 10 -s 10.0.2.4 -d 10.0.2.5 -s 10.0.3.4 -d 10.0.3.5 -r 1
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
    parser.add_argument("-r", "--rate", dest="link_percentage",
        type=float,
        help="The Interface link percentage to use", 
        default = 10 )

    args = parser.parse_args()
    if not os.path.exists(args.output_folder):
        os.mkdir(args.output_folder)
    send_udp_stream(args)