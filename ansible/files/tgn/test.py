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


# TODO fix me. doesn't always work
def create_steam(ip_src="10.0.2.4", ip_dst="10.0.2.5", pcap_file="/tmp/rx_dns.pcap", pps=10):
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

    s =  STLStream(packet = STLPktBuilder(pkt=pcap_file, vm=vm), # path relative to profile and not to loader path
                        int_mac_src_override_by_pkt = 1,
                        mode = STLTXCont(pps = pps))

    print(s.has_custom_mac_addr())

    return s

create_steam()