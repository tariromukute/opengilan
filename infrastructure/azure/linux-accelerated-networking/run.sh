#!/bin/bash

export DPDK_VER=20.02
export PKTGEN_VER=20.02.0
export PCI_IF="b812:00:02.0"

cd /opt/pktgen-$PKTGEN_VER && ./app/x86_64-native-linuxapp-gcc/pktgen --vdev="net_vdev_netvsc0,iface=eth1" -- -T -P -m "2.[0]" -f /home/open/pktgen.lua