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

# Install packages for deploying with Azure
pip install -r requirements-azure.txt

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
- We install bpftrace from source because ...... __data_loc couldn't be printed in the default package version

## Test with Open Source VNFs
- [OPNFV List Of VNFs](https://wiki.opnfv.org/display/functest/List+Of+VNFs)
- [OSM List of VNFs](https://osm.etsi.org/wikipub/index.php/VNFs)

## VNF Lifecycle Docs
- [Network Functions Virtualisation (NFV) Release 3; Protocols and Data Models; RESTful protocols specification for the Or-Vnfm Reference Point](https://www.etsi.org/deliver/etsi_gs/NFV-SOL/001_099/003/03.05.01_60/gs_NFV-SOL003v030501p.pdf)

tcpdump -ttttnnr cap2/dns.pcap  

*Install libs for access TREX python API*

https://trex-tgn.cisco.com/trex/doc/cp_stl_docs/index.html#how-to-install

export PYTHONPATH=/home/azureuser/trex-core/scripts/automation/trex_control_plane/interactive

```bash
while true; do echo -n "hello" > /dev/udp/10.0.2.4/8000; done
```

```bash
sudo ip r add 16.0.0.0/16 via 10.0.2.5 dev eth2

sudo ip r add 48.0.0.0/16 via 10.0.3.5 dev eth1
```

To debug whether packets are being deliver, in our case testing UDR configurations we use nping to send raw packets.

```bash
sudo nping --send-ip --source-mac 00:0d:3a:2e:43:f9 --dest-mac 00:0d:3a:2d:48:5e --source-ip 48.0.1.7 --dest-ip 16.0.1.6 --udp -g 5000 -p 5001 --data-length 16

sudo tcpdump -eni eth0 host 48.0.1.7
```

```bash
scp -i ~/.ssh/id_rsa azureuser@olan151trex.southafricanorth.cloudapp.azure.com:/home/azureuser/tpstat/offcputime.out ~/Documents/personal/phd/dev/opengilan/ansible/.results/stl_dns_streams-rate_20-trex.json
```

scp -i ~/.ssh/id_rsa -r azureuser@olan151trex.southafricanorth.cloudapp.azure.com:/tmp/results ~/Documents/personal/phd/dev/opengilan/ansible/.results/trex

lsb-release

gnupg

apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 4052245BD4284CDD

### bcc tools from source

sudo apt install -y bison build-essential cmake flex git libedit-dev \
  libllvm7 llvm-7-dev libclang-7-dev python zlib1g-dev libelf-dev libfl-dev python3-distutils

sudo apt-get -y install luajit libluajit-5.1-dev

sudo apt install -y iperf3 netperf

export PYTHONPATH=$(dirname `find /usr/lib -name bcc`):$PYTHONPATH

:/usr/src/5.10.76-linuxkit/include/:$C_INCLUDE_PATH

### BCC tools tracings

```bash
docker build -t docker-bpf .

git clone --depth 1 --branch v5.6.11-linuxkit https://github.com/linuxkit/linux 5.10.76-linuxkit

docker run -it --rm \
  --privileged \
  -v /lib/modules:/lib/modules:ro \
  -v /Volumes/LinuxWorkspace/5.10.76-linuxkit:/usr/src/5.10.76-linuxkit \
  -v /etc/localtime:/etc/localtime:ro \
  --workdir /usr/share/bcc/tools \
  docker-bpf

docker run -it --rm \
  --privileged \
  -v /lib/modules:/lib/modules \
  -v /Volumes/LinuxWorkspace/5.10.76-linuxkit:/usr/src/5.10.76-linuxkit \
  -v /etc/localtime:/etc/localtime \
  --workdir /usr/share/bcc/tools \
  ubuntu:20.04

 docker run -it --rm \
  --privileged \
  -v /Volumes/LinuxWorkspace/5.10.76-linuxkit:/lib/modules/5.10.76-linuxkit/source \
  -v /Volumes/LinuxWorkspace/5.10.76-linuxkit:/lib/modules/5.10.76-linuxkit/build \ 
  -v /Volumes/LinuxWorkspace/5.10.76-linuxkit:/usr/src/5.10.76-linuxkit \
  --workdir /usr/share/bcc/tools \
  docker-bpf

 docker run -it --rm \
  --privileged \
  -v /Volumes/LinuxWorkspace/5.10.76-linuxkit:/lib/modules/5.10.76-linuxkit/source -v /Volumes/LinuxWorkspace/5.10.76-linuxkit:/lib/modules/5.10.76-linuxkit/build -v /Volumes/LinuxWorkspace/5.10.76-linuxkit:/usr/src/5.10.76-linuxkit \
  --workdir /usr/share/bcc/tools \
  ubuntu:20.04

  sudo docker run --rm -it --privileged \
  -v /lib/modules:/lib/modules \
  -v /Volumes/LinuxWorkspace/5.10.76-linuxkit:/lib/modules/5.10.76-linuxkit/build \
  -v /sys:/sys \
  -v /usr/src:/usr/src \
  alpine:3.12

 apt-get install aptitude

 aptitude install libssl-dev 
stackcount -f -P -D 10 ktime_get > out.stackcount01.txt


```

To compile the linux code you need to be on a case sensitive filesystem. To create one

```bash
Launch Disk Utility
Choose "New Image"
Enter a nice Name for your Volume, e.g "LinuxWorkspace"
Set the size to something that will most likely fit your needs (resizing is a whole another story)
Select "APFS (Case Sensitive)" in "Format".
Select "Single Partition - GUID partition map" in "Partitions"
Ensure "read/write disk format" is set in "Image Format".
Save it somewhere on your hard drive
```

```bash
git clone https://github.com/iovisor/bcc.git
mkdir bcc/build; cd bcc/build
cmake ..
make
sudo make install
cmake -DPYTHON_CMD=python3 .. # build python3 binding
pushd src/python/
make
sudo make install
popd
```


## Lessons

Azure has limits for concurrent connections per VM see [link](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#networking-limits)
The limit is 500,000, up to 1,000,000 for two or more NICs.
It also has a list on the number of flows 250k see [link](https://docs.microsoft.com/en-us/azure/virtual-network/virtual-machine-network-throughput#flow-limits-and-active-connections-recommendations)

tx_bps tx_pps tx_util sut_total_rx_pps - duration was 10s on trex
287342528.0 500291.25 3.6738912800000003 2101315 (500kpps)
574196480.0 996902.25 7.337008399999998 1946131 (1Mpps)
779903104.0 1355321.125 9.96754484 2636674 (set % to 10)
3128658688.0 5424779.0 39.966233280000004 3052634 (set % to 40)

The SUT at some level seems to roughly maintain the number of received packets. The bytes can go up as we increase the packet size but the number of packets seems to be roundabout the same range.

The Inbound flows on the SUT seems to be around 250 for sum. The limit on active flows is 250k. Not sure if the number of flows is the issue or the recording from the inbound flows is wrong or off by 1k. Regardless the Inbound flows seem to be ~250 everytime. Calculating the packets per second 500kpps if these are directly proportional to flows then we are probably getting to the limit of 500k flows with 250k flows per second.

The Azure Monitor doesn't record any outbound packets on the Trex VM. This maybe due to the DPDK being used, might need to verify with docs, see the screenshots in assests folder.