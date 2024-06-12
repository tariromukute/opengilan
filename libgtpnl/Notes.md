

## Install

```bash
docker run -d -t --name gtpu_lib \
           --privileged \
           --cap-add=ALL -d \
           -v /dev:/dev \
           -v /lib/modules:/lib/modules \
           ubuntu:23.04

# Install prerequisites
# Removed from the list libmnl-dev
sudo apt install autoconf libtool build-essential git wget

# Install libmnl from source
wget https://netfilter.org/projects/libmnl/files/libmnl-1.0.5.tar.bz2
tar -xf libmnl-1.0.5.tar.bz2
cd libmnl-1.0.5
./configure --prefix=/usr
make
make install
whereis libmnl.so
ldd /usr/lib/libmnl.so

git clone https://gitea.osmocom.org/cellular-infrastructure/libgtpnl

# Build
autoreconf -fi

./configure

make

make install

ldconfig
```

## Running

This is failing on openstack VM with error `cannot create GTP device: Operation not permitted`
```bash
cd tools
./gtp-link add gtp1 ip
```


-----

## Run in container

```bash
# Probably need to load these on host instead of from docker
#

# Create a container that has access to kernel modules
docker run -d -t --name gtpu_container \
           --privileged \
           --cap-add=ALL -d \
           -v /dev:/dev \
           -v /lib/modules:/lib/modules \
           ubuntu:23.04

# Install packages to load kernel modules
apt install kmod
```

```bash
apt install build-essential git
apt install linux-headers-$(uname -r)
git clone https://github.com/free5gc/gtp5g.git && cd gtp5g

make clean
make
```

Install GTP module
```bash
# Uncomment the deb-src in sources.list
# Then

sudo apt install libncurses-dev gawk flex bison openssl libssl-dev dkms libelf-dev libudev-dev libpci-dev libiberty-dev autoconf llvm

apt source linux-image-unsigned-$(uname -r)

make oldconfig

make prepare --jobs=$(grep -c ^processor /proc/cpuinfo) --max-load=$(grep -c ^processor /proc/cpuinfo)
make modules_prepare --jobs=$(grep -c ^processor /proc/cpuinfo) --max-load=$(grep -c ^processor /proc/cpuinfo)
make SUBDIRS=scripts/mod --jobs=$(grep -c ^processor /proc/cpuinfo) --max-load=$(grep -c ^processor /proc/cpuinfo)
make SUBDIRS=drivers/net/ modules --jobs=$(grep -c ^processor /proc/cpuinfo) --max-load=$(grep -c ^processor /proc/cpuinfo)
sudo cp drivers/net/gtp.ko /lib/modules/6.5.0-1016-azure/kernel/drivers/net/

depmod
modprobe gtp
```

Following the above I get error `modprobe: ERROR: could not insert 'gtp': Exec format error` on both Azure and OpenStack VMs.

```bash
make SUBDIRS=drivers/net/ modules

# make SUBDIRS=drivers/net/ modules_install

sudo cp drivers/net/gtp.ko /lib/modules/6.2.16/
depmod
modprobe gtp
```

```bash
apt install linux-headers-$(uname -r)
apt install linux-source-$(uname -r)
make -C /lib/modules/6.2.0-39-generic/build/ M=$PWD modules

```

NOTE: I was not able to get this working

## Useful resources

- [Using GTP on Linux with libgtpnl](https://www.slideshare.net/kentaroebisawa/using-gtp-on-linux-with-libgtpnl)
- https://www.linuxfromscratch.org/blfs/view/svn/basicnet/libmnl.html
- https://serverfault.com/questions/674415/compiling-an-individual-kernel-module-debian-ubuntu
- https://open-cells.com/index.php/blog/
- https://askubuntu.com/questions/168279/how-do-i-build-a-single-in-tree-kernel-module#338403
- [Error building header modules on VM](https://askubuntu.com/a/303815)