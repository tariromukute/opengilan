#!/bin/bash

export DPDK_VER=20.02
export PKTGEN_VER=20.02.0
export PCI_IF="0728:00:02.0"

echo "Setting env..."
export RTE_TARGET=x86_64-native-linuxapp-gcc
export RTE_SDK=/opt/dpdk-$DPDK_VER
ln -s /usr/bin/python2.7 /usr/bin/python

echo "Installing DPDK..."
cd dpdk-$DPDK_VER
make config T=x86_64-native-linuxapp-gcc CONFIG_RTE_EAL_IGB_UIO=y CONFIG_RTE_LIBRTE_MLX5_PMD=y
make install T=x86_64-native-linuxapp-gcc DESTDIR=install CONFIG_RTE_EAL_IGB_UIO=y CONFIG_RTE_LIBRTE_MLX5_PMD=y

cd ..

echo "Downloading pktgen..."
if [ ! -f /opt/pktgen-$PKTGEN_VER.tar.gz ]; then
    wget http://dpdk.org/browse/apps/pktgen-dpdk/snapshot/pktgen-$PKTGEN_VER.tar.gz
fi

echo "Unpacking pktgen..."
rm -rf pktgen-$PKTGEN_VER/
tar xvf pktgen-$PKTGEN_VER.tar.gz

echo "Installing DPDK..."
cd pktgen-$PKTGEN_VER
make

echo "binding dpdk interface $PCI_IF"
modprobe uio
insmod /opt/dpdk-$DPDK_VER/x86_64-native-linuxapp-gcc/kmod/igb_uio.ko
modprobe vfio-pci
modprobe uio_pci_generic
dpdkdevbind=/opt/dpdk-$DPDK_VER/usertools/dpdk-devbind.py
$dpdkdevbind --force -u $PCI_IF
$dpdkdevbind -b igb_uio $PCI_IF
$dpdkdevbind -s

echo "To run pktgen:"
echo  '/opt/pktgen-$PKTGEN_VER/app/x86_64-native-linuxapp-gcc/pktgen  -- -T -P -m "2.[0]"'
echo  '/opt/pktgen-$PKTGEN_VER/app/x86_64-native-linuxapp-gcc/pktgen  -- -T -P -m  "2/4:6/8.[0]"'

echo "
example commands:
set 0 dst mac  e4:43:4b:53:51:83
set 0 rate 1
set 0 size 128
start 0
stop 0
"