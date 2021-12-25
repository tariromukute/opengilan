# Open Gi-LAN

The project builds the stack/infrastructure for an Open Gi-LAN or just Open LAN (Local Arear Network). The LAN sits after the mobile core network and will apply various network functions to the traffic from the core network.

## Installation

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install packages
pip install -r requirements.txt

```

## Connect to test bed with a bastion host

```bash
# generate ssh key(s). using different keys for bastion host and the testbed servers
ssh-keygen -t rsa -b 2048

# add the public key(s) to the bastion host and testbed servers (replace id_rsa.pub with key name)
cat ~/.ssh/id_rsa.pub

# copy above and put in other servers (can use ssh-copy-id instead)
mkdir ~/.ssh
echo ssh_pub_key >> ~/.ssh/authorized_keys
```

Add the following to `~/.ssh/config`

```text
Host bastion
  HostName url
    ForwardAgent yes
  User username
  IdentityFile ~/.ssh/id_rsa
```

```bash
# test connection through bastion host
ssh -o ProxyCommand="ssh -W %h:%p -q bastion" -i ~/.ssh/chpc user@10.x.x.x
```

## Run playbook

```bash
ansible-playbook -i inventory.ini monitor.yml -K
```

## Notes
iperf -P can help influence the bandwidth results

## Useful Resources

- https://www.researchgate.net/publication/349761932_Measuring_with_JPerf_and_PsPing_Throughput_and_Estimated_Packet_Delivery_Delay_vs_TCP_Window_Size_Parallel_Streams

mst wasn't working, to install it see [link](https://community.mellanox.com/s/article/getting-started-with-mellanox-firmware-tools--mft--for-linux)
- wget https://content.mellanox.com/ofed/MLNX_OFED-5.4-1.0.3.0/MLNX_OFED_LINUX-5.4-1.0.3.0-ubuntu20.04-x86_64.tgz
- wget https://content.mellanox.com/ofed/MLNX_OFED-4.9-4.0.8.0/MLNX_OFED_LINUX-4.9-4.0.8.0-ubuntu18.04-x86_64.tgz

install dpdk - [link](https://doc.dpdk.org/guides/linux_gsg/build_dpdk.html)

for mellanox - [link](https://doc.dpdk.org/guides/nics/mlx5.html)
- wget tar mlx5 ofed
- extract from it and run install

install pktgen - [link](https://pktgen-dpdk.readthedocs.io/en/latest/getting_started.html)
- sudo apt install -y python3-pyelftools python-pyelftools lua5.3 liblua5.3-dev 
- sudo apt install make
- sudp apt install cmake
- * the pkg-config can be put in different folder
- sudo apt install libpcap-dev libnuma-dev pkg-config build-essential librdmacm-dev libnuma-dev libmnl-dev meson
- sudo apt install libibverbs-dev libmlx5-1 ibverbs-providers

edit cfg/xdp-40.cfg in pktgen

run pktgen - ./tools/run.py xdp-40 (might need to set it up first ./tools/run.py -s xdp-40)

check free huge pages - grep -i huge /proc/meminfo

sudo -E ./app/pktgen -l 0-3 -n 3 --proc-type auto -w 0000:41:00.0 -- -P -m "[1:3].0"

meson --reconfigure -Denable_lua=true Builddir

ninja -C Builddir

custom lua scripts tutorial - https://mishal.dev/running-dpdk-with-pktgen

blog - https://medium.com/codex/nvidia-mellanox-bluefield-2-smartnic-hands-on-tutorial-rig-for-dive-part-vii-b-contd-afaffce7af4f

sudo tc qdisc add dev ens3 root netem loss 100%

sudo tc qdisc show dev ens3

sudo tc qdisc del dev ens3 root netem loss 100%

sudo tc qdisc show dev ens3

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_and_managing_networking/getting-started-with-nftables_configuring-and-managing-networking

Why we will need deep inspectors for network function - https://ungleich.ch/u/blog/nftables-magic-redirect-all-ports-to-one-port/

UDP server - https://gist.github.com/karupanerura/00c8ff6a48d98dd6bec2

https://cs.baylor.edu/~donahoo/practical/CSockets/practical/

https://github.com/chronoxor/CppServer#example-udp-echo-server
  - sudo apt install binutils-dev uuid-dev libssl-dev
  - sudo apt install python3-pip
  - sudo pip3 install --prefix /usr/local gil
  - sudo apt install cmake

With a udp echo server from the above packets are always dropped from xxx
  - add permenent arp record to resolve that: sudo arp -s 10.0.0.7 00:22:48:65:6e:cf

https://dev.to/aws-builders/100g-networking-in-aws-a-network-performance-deep-dive-3bg0
- In the world of NICs, these ‘workers’ are queues

sudo ethtool -L
sudo ethtool -U eth1 flow-type udp4 dst-port 3333 action 2

https://blog.cloudflare.com/how-to-drop-10-million-packets/

## Pktgen integration

- Managed to set up pktgen on azure. There were issues when trying to use the latest versions of DPDK and Pktgen.
- Managed to get it working with DPDK_VER=20.02 and PKTGEN_VER=20.02.0
- Ran lua scripts successfully but had the following issues:
  - The stats reported for tx where almost always the same, even when rate is changing. Not sure if this an issue with the Lua script or the pktgen
  - When I start return traffic from the DUT, pktgen stops printing stats (it freezes). I have to stop the DUT from returning traffic and wait for a while for the pktgen console to be responsive. This because an issue in this use case where I want to automate reading and reporting of stats.

## Netsvc

- [Hyper-V network driver](https://www.kernel.org/doc/html/v5.12/networking/device_drivers/ethernet/microsoft/netvsc.html)

## Bpftrace

- [Linux Extended BPF (eBPF) Tracing Tools](https://www.brendangregg.com/ebpf.html#bpftrace)

sudo cat /sys/kernel/debug/tracing/events/napi/napi_poll/format

tracepoint:tcp
tracepoint:udp
tracepoint:sock
tracepoint:napi
tracepoint:net
tracepoint:skb
tracepoint:irq
tracepoint:raw_syscalls

- [Taming Tracepoints in the Linux Kernel](https://blogs.oracle.com/linux/post/taming-tracepoints-in-the-linux-kernel)
- [Event Tracing](https://www.kernel.org/doc/Documentation/trace/events.txt)

- [A Guide to Using Raw Sockets](https://www.opensourceforu.com/2015/03/a-guide-to-using-raw-sockets/)

Test scenarios

1. UDP packet where all parts of the stack are used - eth, ip, transport, sock, and user
2. RAW packets AF_PACKET
3. Hooks inbetweeen
4. Raw sockets where - eth, sock, user
5. XDP & TC

- [XDP support on Azure](https://mjmwired.net/kernel/Documentation/networking/device_drivers/microsoft)
- [Support for XDP on Hyper-V](https://elixir.bootlin.com/linux/v5.8/source/Documentation/networking/device_drivers/microsoft/netvsc.rst)

StorPerf provides the following metrics:
• IOPS
• Bandwidth (number of kilobytes read or written per second)
• Latency
2. Hooks inbetweeen
3. Raw sockets where - eth, sock, user
4. XDP & TC

## AF_PACKET

- [Send an arbitrary Ethernet frame using an AF_PACKET socket in C](http://www.microhowto.info/howto/send_an_arbitrary_ethernet_frame_using_an_af_packet_socket_in_c.html)
  - Touch on reasons for using AF_PACKET and alternatives to AF_PACKET
  - Also the portable way of using AF_PACKET (libpcap)
- [Send an arbitrary Ethernet frame using libpcap](http://www.microhowto.info/howto/send_an_arbitrary_ethernet_frame_using_libpcap.html)


## Notes

- For ease we can use BTF with tc programs. This will allow us to see the maps as json hence can do without a custom userspace programs for reading the stats from the maps. We can the use bpftool to print out the maps
- However this requires the latest iproute (from tag 5.11.0) configured with support for libbpf. Might need to compile it from source.
- For running tc (iproute2) with libbpf support set the PKG_CONFIG_PATH with the path to libpf.pc (PKG_CONFIG_PATH=/usr/local/lib64/pkgconfig) and configure
- http://www.policyrouting.org/iproute2.doc.html
- We install bpftrace from source because ......

## Test with Open Source VNFs
- [OPNFV List Of VNFs](https://wiki.opnfv.org/display/functest/List+Of+VNFs)
- [OSM List of VNFs](https://osm.etsi.org/wikipub/index.php/VNFs)
