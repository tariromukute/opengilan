import socket

# Addresses and data
# Set this to your Ethernet interface (e.g. eth0, eth1, ...)
interface = "eth1"
protocol = 0  # 0 = ICMP, 6 = TCP, 17 = UDP, ...

# Create a raw socket with address family PACKET
s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)

# Bind the socket to an interface using the specific protocol
s.bind((interface, protocol))

# Create an Ethernet frame header
# - Destination MAC: 6 Bytes
# - Source MAC: 6 Bytes
# - Type: 2 Bytes (IP = 0x0800)
# Change the MAC addresses to match the your computer and the destination
ethernet_hdr = [0x12, 0x34, 0x56, 0x78, 0x9a, 0xbc,  # 12:34:56:78:9a:bc
                0x00, 0x22, 0x48, 0x66, 0x67, 0x85,  # 00:22:48:65:67:85
                0x08, 0x00]

# ------------
# First packet
# Lets create an Ethernet frame where the data is "Hello". The ethernet header
# is already created above, now we just need the data. Note that if you capture
# this frame in Wireshark it may report "Malformed packet" which means Wireshark
# does not understand the protocol used. Thats ok, the packet was still sent.

# Frame structure:
# etherent_hdr | ethernet_data
#    14 B   |    5 B

# ethernet_data_str = "Hello"

# # Convert byte sequences to strings for sending
# ethernet_hdr_str = "".join(map(chr, ethernet_hdr))

# # Send the frame
# s.send(ethernet_hdr_str + ethernet_data_str)


# -------------
# Second packet
# Now lets create a more complex/realistic packet. This time a ping echo request
# with the intention of receiving a ping echo reply. This requires us to create
# the IP header, ICMP header and ICMP data with exact values of each field given
# as bytes. The easiest way to know what bytes is to capture a normal packet in
# Wireshark and then view the bytes. In particular look at the IP ahd ICMP
# checksums - they need to be correct for the receiver to reply to a ping Echo
# request. The following example worked on my computer, but will probably not
# work on your computer without modification. Especially modify the addresses
# and checksums.

# Frame structure:
# etherent_hdr | ip_hdr | icmp_hdr | icmp_data
#    14 B   | 20 B |  16 B  |  48 B

# Create IP datagram header
# - Version, header length: 1 Byte (0x45 for normal 20 Byte header)
# - DiffServ: 1 Byte (0x00)
# - Total length: 2 Bytes
# - Identificaiton: 2 Bytes (0x0000)
# - Flags, Fragment Offset: 2 Bytes (0x4000 = Dont Fragment)
# - Time to Line: 1 Byte (0x40 = 64 hops)
# - Protocol: 1 Byte (0x01 = ICMP, 0x06 = TCP, 0x11 = UDP, ...)
# - Header checksum: 2 Bytes
# - Source IP: 4 Bytes
# - Destination IP: 4 Bytes
ip_hdr = [0x45,
          0x00,
          0x00, 0x54,
          0x80, 0xc6,
          0x40, 0x00,
          0x40,
          0x01,
          0x9b, 0xda,  # checksum - change this!
          0x0a, 0x00, 0x02, 0x05,  # 10.0.2.5 0a.00.02.05
          0x10, 0x00, 0x02, 0x04]  # 16.0.2.4 10.00.02.04 

# ICMP Ping header
# - Type: 1 Byte (0x08 = Echo request, 0x00 = Echo reply)
# - Code: 1 Byte (0x00)
# - Checksum: 2 Bytes (try 0x0000, then in Wireshark look at correct value)
# - Identifier: 2 Bytes
# - Sequence number: 2 Bytes
# - Timestamp: 8 Bytes
icmp_hdr = [0x08,
            0x00,
            0xc2, 0x4d,  # checksum - change this!
            0x00, 0x00,
            0x00, 0x01,
            0xab, 0x5c, 0x8a, 0x54, 0x00, 0x00, 0x00, 0x00]

# ICMP Ping data
# - Data: 48 Bytes
icmp_data = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
             0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
             0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
             0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
             0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
             0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

# Convert byte sequences to strings for sending
ethernet_hdr_str = "".join(map(chr, ethernet_hdr))
ip_hdr_str = "".join(map(chr, ip_hdr))
icmp_hdr_str = "".join(map(chr, icmp_hdr))
icmp_data_str = "".join(map(chr, icmp_data))

pkt_str = ethernet_hdr_str + ip_hdr_str + icmp_hdr_str + icmp_data_str

# Send the frame
s.send(ethernet_hdr_str + ip_hdr_str + icmp_hdr_str + icmp_data_str)

# while true; do sleep 1; sudo python2.7 send_raw_packet.py; done