# get TRex APIs
from asyncio import streams

from trex_stl_lib.api import *
from argparse import ArgumentParser
from datetime import datetime
import os
import json
import math

c = STLClient(server='127.0.0.1')

port_0 = 0
port_1 = 1

ports = [0, 1]

try:

    c.connect()
    port = 0
    c.reset(ports=[port])

    file_name = "/tmp/rx_dns.pcap"
    ip_src="10.0.2.4"
    ip_dst="10.0.2.5"
    pps = 10000
    duration = 3

    packets = rdpcap("/tmp/rx_dns.pcap")
    pkt_count = len(packets)
    print('Packets {}'.format(len(packets)))
    
    vm = [
        # src                                                            <4>
        STLVmFlowVar(name="src",
                     value_list=[ip_src], op="inc"),
        STLVmWrFlowVar(fv_name="src", pkt_offset="IP.src"),

        # dst
        STLVmFlowVar(name="dst",
                     value_list=[ip_dst], op="inc"),
        STLVmWrFlowVar(fv_name="dst", pkt_offset="IP.dst"),

        # checksum
        STLVmFixIpv4(offset="IP")
    ]

    ipg_usec = 1000000 / pps
    count = max(1, math.ceil((pps / pkt_count) * duration))

    c.push_pcap(file_name,             # our local PCAP file
                ports=port,                           # use 'port'
                ipg_usec=ipg_usec,                         # IPG
                count=count,                              # inject only once
        vm=vm                                 # provide VM object
        )

    c.wait_on_traffic()

    stats = c.get_stats()
    opackets = stats[port]['opackets']
    print("{0} packets were Tx on port {1}\n".format(opackets, port))

except STLError as e:
    print(e)
    sys.exit(1)

finally:
    c.disconnect()