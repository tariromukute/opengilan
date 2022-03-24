from scapy.all import *

packets = []

for j in range(10, 99):
    for i in range(10, 99):
        pkt = Ether(src="00:0D:3A:24:4E:16", dst="12:34:56:78:9A:BC")/IP(src="10.0.2.4",dst="10.0.2.5")/UDP(sport=1025)/DNS(rd=1, qd=DNSQR(qname='open{}{}lan.mk'.format(j, i)))
        packets.append(pkt)

wrpcap("/tmp/rx_dns.pcap", packets)