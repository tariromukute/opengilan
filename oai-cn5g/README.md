# OAI Installation

## The file documents how to set up oai-cn5g on Ubuntu 20.04 virtual machine

- Install dependencies `apt-transport-https ca-certificates curl software-properties-common python3-pip virtualenv python3-setuptools`
- Add apt keys `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -`
- Add repository `sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"`
- Update cache `apt-cache policy docker-ce`
- Install docker `sudo apt install docker-ce`
- Install docker compose plugin `sudo apt install docker-compose-plugin`
- Add docker group `sudo usermod -aG docker ${USER}`
- End session and start a new one for group changes to take effect. `exit`, then ssh  back in
- Login to docker `docker login`
- Pull the following images


```bash
docker pull ubuntu:bionic
docker pull mysql:5.7
```

*** To run OAI in debug mode pull the images from docker, else skip to manually building the images ***
```bash
# OAI images
docker pull oaisoftwarealliance/oai-amf:develop
docker pull oaisoftwarealliance/oai-nrf:develop
docker pull oaisoftwarealliance/oai-spgwu-tiny:develop
docker pull oaisoftwarealliance/oai-smf:develop
docker pull oaisoftwarealliance/oai-udr:develop
docker pull oaisoftwarealliance/oai-udm:develop
docker pull oaisoftwarealliance/oai-ausf:develop
docker pull oaisoftwarealliance/oai-upf-vpp:develop
docker pull oaisoftwarealliance/oai-nssf:develop
# Utility image to generate traffic
c

# Re tag images
docker image tag oaisoftwarealliance/oai-amf:v1.4.0 oai-amf:v1.4.0
docker image tag oaisoftwarealliance/oai-nrf:v1.4.0 oai-nrf:v1.4.0
docker image tag oaisoftwarealliance/oai-smf:v1.4.0 oai-smf:v1.4.0
docker image tag oaisoftwarealliance/oai-spgwu-tiny:v1.4.0 oai-spgwu-tiny:v1.4.0
docker image tag oaisoftwarealliance/oai-udr:v1.4.0 oai-udr:v1.4.0
docker image tag oaisoftwarealliance/oai-udm:v1.4.0 oai-udm:v1.4.0
docker image tag oaisoftwarealliance/oai-ausf:v1.4.0 oai-ausf:v1.4.0
docker image tag oaisoftwarealliance/oai-upf-vpp:v1.4.0 oai-upf-vpp:v1.4.0
docker image tag oaisoftwarealliance/oai-nssf:v1.4.0 oai-nssf:v1.4.0
docker image tag oaisoftwarealliance/trf-gen-cn5g:latest trf-gen-cn5g:latest

```

```bash
# Clone directly on the latest release tag
git clone --branch v1.4.0 https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-fed.git
cd oai-cn5g-fed
# If you forgot to clone directly to the latest release tag
git checkout -f v1.4.0


# Synchronize all git submodules
./scripts/syncComponents.sh 

```

## Reducing the logs for the file

Although the documentation (at the time of writing) states that the network functions produce info level logs see [docs](https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-fed/-/blob/master/docs/DEBUG_5G_CORE.md#1-building-images-in-debug-mode). The docker containers from oaisoftwarealliance tags v1.4.0 and v1.5.0 produce debug logs. When doing load testing this affects the performance of the core network. To produce info logs going to build the images from source. See below. 

```bash
# Build AMF
cd ~/

docker build --target oai-amf --tag tariromukute/oai-amf:develop \
               --file component/oai-amf/docker/Dockerfile.amf.ubuntu \
            #    --build-arg BASE_IMAGE=ubuntu:bionic \
               component/oai-amf
docker image push tariromukute/oai-amf:v1.4.0
docker image tag tariromukute/oai-amf:v1.4.0 oai-amf:v1.4.0

# Build SMF
docker build --target oai-smf --tag tariromukute/oai-smf:v1.4.0 \
               --file component/oai-smf/docker/Dockerfile.smf.ubuntu18 \
               --build-arg BASE_IMAGE=ubuntu:bionic \
               component/oai-smf
docker image push tariromukute/oai-smf:v1.4.0
docker image tag tariromukute/oai-smf:v1.4.0 oai-smf:v1.4.0

# Build NRF
docker build --target oai-nrf --tag tariromukute/oai-nrf:v1.4.0 \
               --file component/oai-nrf/docker/Dockerfile.nrf.ubuntu18 \
               --build-arg BASE_IMAGE=ubuntu:bionic \
               component/oai-nrf
docker image push tariromukute/oai-nrf:v1.4.0
docker image tag tariromukute/oai-nrf:v1.4.0 oai-nrf:v1.4.0

# Build SPGW-U
docker build --target oai-spgwu-tiny --tag tariromukute/oai-spgwu-tiny:v1.4.0 \
               --file component/oai-upf-equivalent/docker/Dockerfile.ubuntu18.04 \
               --build-arg BASE_IMAGE=ubuntu:bionic \
               component/oai-upf-equivalent
docker image push tariromukute/oai-spgwu-tiny:v1.4.0
docker image tag tariromukute/oai-spgwu-tiny:v1.4.0 oai-spgwu-tiny:v1.4.0

# Build ausf (failed)
docker build --target oai-ausf --tag tariromukute/oai-ausf:v1.4.0 \
               --file component/oai-ausf/docker/Dockerfile.ausf.ubuntu18 \
               --build-arg BASE_IMAGE=ubuntu:bionic \
               component/oai-ausf
docker image push tariromukute/oai-ausf:v1.4.0
docker image tag tariromukute/oai-ausf:v1.4.0 oai-ausf:v1.4.0

# Build UDM
docker build --target oai-udm --tag tariromukute/oai-udm:v1.4.0 \
               --file component/oai-udm/docker/Dockerfile.udm.ubuntu18 \
               --build-arg BASE_IMAGE=ubuntu:bionic \
               component/oai-udm
docker image push tariromukute/oai-udm:v1.4.0
docker image tag tariromukute/oai-udm:v1.4.0 oai-udm:v1.4.0

# Build UDR
docker build --target oai-udr --tag tariromukute/oai-udr:v1.4.0 \
               --file component/oai-udr/docker/Dockerfile.udr.ubuntu18 \
               component/oai-udr
docker image push tariromukute/oai-udr:v1.4.0
docker image tag tariromukute/oai-udr:v1.4.0 oai-udr:v1.4.0

# Build UPF
docker build --target oai-upf --tag tariromukute/oai-cn5g-upf:develop \
               --file docker/Dockerfile.upf.ubuntu \
               --build-arg BASE_IMAGE=ubuntu:bionic \
               .

docker build --network=host --target oai-upf --tag tariromukute/oai-upf:develop \
               --file component/oai-upf/docker/Dockerfile.upf.ubuntu \
               component/oai-upf

docker image push tariromukute/oai-spgwu-tiny:v1.4.0
docker image tag tariromukute/oai-spgwu-tiny:v1.4.0 oai-spgwu-tiny:v1.4.0

# Build VPP (skipped)
docker build --target oai-upf-vpp --tag tariromukute/oai-upf-vpp:v1.4.0 \
               --file component/oai-upf-vpp/docker/Dockerfile.upf-vpp.ubuntu \
               component/oai-upf-vpp
docker image push tariromukute/oai-upf-vpp:v1.4.0
docker image tag tariromukute/oai-upf-vpp:v1.4.0 oai-upf-vpp:v1.4.0

# Build NSSF
docker build --target oai-nssf --tag tariromukute/oai-nssf:v1.4.0 \
               --file component/oai-nssf/docker/Dockerfile.nssf.ubuntu18 \
               --build-arg BASE_IMAGE=ubuntu:bionic \
               component/oai-nssf
docker image push tariromukute/oai-nssf:v1.4.0
docker image tag tariromukute/oai-nssf:v1.4.0 oai-nssf:v1.4.0
```

```bash
sudo sysctl net.ipv4.conf.all.forwarding=1
sudo iptables -P FORWARD ACCEPT
```

### Install UERANSIM on another VM

```bash
ip route add 48.0.0.0/16 via 192.168.222.222

# On terminal 1
build/nr-gnb -c config/oai-cn5g-gnb.yaml

# On terminal 2
sudo build/nr-ue -c config/oai-cn5g-ue.yaml

# Or run multiple processes
seq 208950000000031 10 208950000000111 | parallel -I{} sudo timeout 10 build/nr-ue -c config/oai-cn5g-ue.yaml -i imsi-{} -n 10

# On terminal 3
ping -I uesimtun0 google.com

sudo tcpdump -i ens3 host <ueransim-ip> -A -w ueransim.pcap

# On OAI
scp -i /home/tariro/snap/microstack/common/.ssh/id_microstack ubuntu@10.20.20.112:/home/ubuntu/ueransim.pcap ./tmp
```

## Setting up local openstack cloud (testbed)

There are two options for setting up the local cloud (testbed), [using Microstack](#using-microstack) snd [using Devstack](#using-devstack). Microstack worked fine for a start but there we couple of issues I had to workaround. You can see this under the [Microstack Gotchas](#microstack-gotchas) section. One of the issues ended up reoccuring and could resolve it so had to switch to Devstack. It is possible that one might not face the issue on their environment.

### Using Microstack

**Install microstack**

```bash
sudo snap install microstack --devmode --edge

sudo microstack init --auto --control

# Get Open stack credentials
sudo snap get microstack config.credentials.keystone-password

# Confirm: Login on https://10.20.20.1 with above password
```

**Set up rules to enable networking**

```bash

# Enable microstack VM to access the internet
sudo iptables -t nat -A POSTROUTING -s 10.20.20.1/24 ! -d 10.20.20.1/24 -j MASQUERADE
sudo sysctl -w net.ipv4.ip_forward=1

# If you have docker rules
sudo iptables -I FORWARD -d 10.20.20.1/24 -j ACCEPT
sudo iptables -I FORWARD -s 10.20.20.1/24 -j ACCEPT
```

**Download and create images**

```bash
# Downloan and create Ubuntu image
wget https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img

# Copy image to a folder microstack has access to avoid permission issues
sudo cp focal-server-cloudimg-amd64.img /var/snap/microstack/common/images/

# Create Ubuntu image
microstack.openstack image create \
    --container-format bare \
    --disk-format qcow2 \
    --min-disk 8 --min-ram 512 \
    --file focal-server-cloudimg-amd64.img \
    --public 20.04

# Create flavor
microstack.openstack flavor create --public m2.medium --id auto \
    --ram 4096 --disk 50 --vcpus 2 --rxtx-factor 1
```

**Create VM on microstack**

```bash
# Launch instance
microstack launch -f m2.medium -n oai 20.04
```

**Remove microstack**

```bash
sudo snap disable microstack

sudo snap remove --purge microstack
```

#### Microstack Gotchas

If you face the error `Permission denied (publickey).` disable and re-enable microstack. See thread [here](https://serverfault.com/questions/1089057/openstack-ubuntuvm-ssh-public-key-permission-denied-on-first-boot)

This doesn't seem to work everytime. The details of the issue are described [here](https://askubuntu.com/questions/1321968/ubuntu-server-20-04-2-lts-hangs-after-bootup-cloud-init-1781-yyyy-mm-dd-h)

### Using Devstack

**Installing devstack**

```bash
# Add user
sudo useradd -s /bin/bash -d /opt/stack -m stack

# 
sudo chmod +x /opt/stack

#
echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
sudo -u stack -i

git clone https://opendev.org/openstack/devstack
cd devstack

# Switch to openstack version of choice
git checkout stable/zed
```

**Configure credentials**

Need to create credentials config file (`local.conf`) before installing the stack inside folder devstack. See example below.

`Note: putting HOST_IP=0.0.0.0 will ensure that openstack doesn't bind to you network interface IP address. This is helpful when you are on WIFI and you IP is dynamically allocated or changes depending on the network`

```
[[local|localrc]]
ADMIN_PASSWORD=secret
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD
HOST_IP=0.0.0.0
```

`Note: When installing on ubuntu 22.04 got an error of repository/PPA does not have a Release file for some of the packages. Implemented the workaround from [here](https://github.com/unetbootin/unetbootin/issues/305), which is to use PPA release files for ubuntu 20.04.`

```bash
# Change PPA configuration
sudo sed -i 's/jammy/focal/g' /etc/apt/sources.list.d/gezakovacs-ubuntu-ppa-jammy.list
sudo sed -i 's/jammy/focal/g' /etc/apt/sources.list.d/system76-ubuntu-pop-jammy.list
```

**Install Devstack**

```bash
./stack.sh
```

When you restart the service you might have issues with devstack. In my case I had error with openvswitch. Resolved it by following steps on [this](https://stackoverflow.com/questions/68001501/error-opt-stack-devstack-lib-neutron-plugins-ovn-agent174-socket) StackOverflow thread.

**Using openstack CLI**

In order to use the CLI you will need to set the env variables.

```bash
sudo su - stack
cd devstack

# username: admin, project: demo
source openrc admin demo
```

**Download and create Ubuntu image**

```bash
cd ~/
mkdir images

# Download image
wget https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img -o images/focal-server-cloudimg-amd64.img

# Create Ubuntu image
openstack image create \
    --container-format bare \
    --disk-format qcow2 \
    --min-disk 8 --min-ram 512 \
    --file images/focal-server-cloudimg-amd64.img \
    --public 20.04

# Confirm image created
openstack image list

# Create flavor we are using for testing
openstack flavor create --public m2.medium --id auto \
    --ram 4096 --disk 50 --vcpus 2 --rxtx-factor 1
```

Create ssh keys to attach to servers

```bash
# Generate keys
ssh-keygen -t rsa -b 4096

# Add key to openstack
openstack keypair create --public-key /opt/stack/.ssh/id_rsa.pub stack

# Confirm key was created
openstack keypair list
```

**Setup the rules to enable networking of the VMs with the internet**

```bash
# On HOST machine: Enable traffic to be correctly routed out of the VMs on Devstack
echo 1 > /proc/sys/net/ipv4/ip_forward
echo 1 > /proc/sys/net/ipv4/conf/<interface>/proxy_arp
iptables -t nat -A POSTROUTING -o <interface> -j MASQUERADE

# Devstack does not wire up the public network by default so we must do that before connecting to this floating IP address.
sudo ip link set br-ex up
sudo ip route add 172.24.4.0/24 dev br-ex
sudo ip addr add 172.24.4.1/24 dev br-ex

# By default, DevStack does not allow users to access VMs, to enable that, we will need to add a rule. We will allow both ICMP and SSH.
# If you get error of more than one security group with name default, use the security group id instead
openstack security group rule create --ingress --ethertype IPv4 --dst-port 22 --protocol tcp default
openstack security group rule create --ingress --ethertype IPv4 --protocol ICMP default
openstack security group rule list

# Enable DHCP for the VMs
openstack subnet set --dhcp private-subnet
openstack subnet set --dns-nameserver 8.8.8.8 private-subnet
```

**Create servers for testing (Documented instructions from [here](https://docs.openstack.org/networking-ovn/latest/contributor/testing.html))**

```bash
# Get net id for private network
PRIVATE_NET_ID=$(openstack network show private -c id -f value)

# Create server (core network)
openstack server create --flavor m2.medium \
    --image 20.04 \
    --key-name  stack \
    --nic net-id=${PRIVATE_NET_ID} \
    <server-name>

openstack floating ip create --project demo --subnet public-subnet public

openstack server add floating ip <server-name> <float-ip>
# Confirm
openstack server list

# Test ping
ping -c 4 <ip-address>

# Confirm SSH into instance
ssh ubuntu@<float-ip>
```

**Uninstall Devstack**

```bash
# Clean
./clean.sh

# Remove
./unstack.sh
```

## Setting up testbed

From the above instruction you should create a VM for the OAI (oai) and for the traffic generator (ue).

### Set up the OAI VM

We can set up OAI by running the steps from the offical site. However, created an ansible role that can set up OAI. The ansible role should make it easier. Below are the details of the two options.

**Set up using an ansible role**

To set up OAI you can follow the instruction on the offical site. Created an ansible role that can set up OAI. The role does the following.
1. Install dependencies for OAI
2. Pulls and runs the OAI docker images
3. Sets up the networking rules to allow traffic forward on VM to the docker containers
4. Add an sql dump to initialise OAI with UEs for testing 208950000000031 - 208950000100031
5. Copies docker-compose file to run OAI on network 48.0.0.0/16. This is for NRF.

```bash
# Firstly install ansible

# Run the ansible role for OAI. Replace 172.24.4.3 with the IP of the OAI VM
ansible all -i '172.24.4.3,' -u ubuntu -m include_role --args "name=olan_oai_cn5g" -e docker_username=<username> -e docker_password=<password> -e user=ubuntu

# one caveat is that ad-hoc cli commands don't have access to the ansible_facts which the role might need. To work around it, you can use caching: ANSIBLE_CACHE_PLUGIN=jsonfile ANSIBLE_CACHE_PLUGIN_CONNECTION=/tmp/ansible-cache ansible -m setup yourHostname and then ANSIBLE_CACHE_PLUGIN=jsonfile ANSIBLE_CACHE_PLUGIN_CONNECTION=/tmp/ansible-cache ansible -m include_role 
```

**Set up running the commands from OAI repo**

**Set up connection between OAI and 5G traffic generator**

`Note: on Microstack use microstack.openstack`

```bash
router="router1"
oai_ip="10.0.0.47" # from private subnet
oai_port_id="d97cbf58-a17f-492f-a568-6a01ab4e769d"

# (1) Add a static route to the Router (with 48.0.0.0/16 in our case - the subnet of the OAI docker container in docker compose)
openstack router set ${router} \
    --route destination=48.0.0.0/16,gateway=${oai_ip}
    
# (2) Add Allowed Address Pairs under the instance interface (48.0.0.0/16 in our case)
openstack port set ${oai_port_id} --allowed-address ip-address=48.0.0.0/16
```

#### OAI Gotchas

- Tried running the OAI on Ubuntu 20.04 VM on microstack. The oai-amf container failed with socket error. Realised that this was due to the SCTP module missing on the kernel `lsmod | grep sctp`. I tried locating the module with `modinfo sctp` but it was not found. I ran `sudo apt install linux-generic` to get the extra modules. I could now find the module and tried loading with `insmod <path_to_module>`. This failed. Turns out I was using the `focal-server-cloudimg-amd64-disk-kvm.img` as recommended or pointed to on one of the Microstack blogs. I switched to creating a VM from image `focal-server-cloudimg-amd64.img`. This also didn't have the SCTP module load but I could find it on the system. I loaded the module `modprobe sctp` and then ran the OAI and this time it worked.

- When I restarted my machine sometimes microstack would become unavailable. You are able to get the login page but ultimately you can't see the dashboard. Running `sudo snap logs microstack` showed one of the error to be `Can't connect to MySQL server on '192.168.100.11' ([Errno 113] No route to host`. In general all the error logs had to do with connection. Turns out that microstack hardcoded the external ip address during installation. On my environment, a laptop using wifi and dynamic ip allocation, the external ip address changes on reboot. This is bug is also discussed on https://bugs.launchpad.net/microstack/+bug/1942741. The resolution was to set the wifi interface to a static ip address. I after this I had to reboot my machine, disable then enable microstack. Maybe one of those steps might not be necessary. These steps resolved my issue.



```
(208950000000132, 5G_AKA, 0C0A34601D4F07677303652C0462535B, 0C0A34601D4F07677303652C0462535B,{"sqn": "000000000020", "sqnScheme": "NON_TIME_BASED", "lastIndexes": {"ausf": 0}}, 8000, milenage, 63bfa50ee6523365ff14c1f45f88737d, NULL, NULL,NULL,NULL,208950000000132);
```

```bash
#Login to mysql container once the container is running
(docker-compose-host)$ docker exec -it mysql /bin/bash
(mysql-container)$ mysql -uroot -plinux -D oai_db
```

### Set up the UE VM

```bash
sudo apt update
git clone https://github.com/tariromukute/core-tg.git
cd core-tg/
git submodule init
git submodule update

sudo apt-get install python3-dev
sudo apt install python3.8-venv
python3 -m venv .venv
source .venv/bin/activate

pip install pycrate
pip install pysctp

pip install cryptography

sudo apt-get install build-essential

cd CryptoMobile && python3 setup.py install

pip install pyyaml

```

### Start expriement

**Start the 5G Core**

```bash
cd oai-cn5g-fed/docker-compose/
docker compose -f docker-compose-basic-nrf-1.yaml up -d

# Confirm all services are healthy. This may take time
docker ps
```

**Start the 5G core traffic generator**

```bash
cd ~/core-tg/
source .venv/bin/activate

# -t : duration of the traffic generator should run for>
# -n : number of UE to register, starting with the UE is IMSI in the ai-cn5g-ue.yaml
# -f : file to write logs to
# -u : config file for UE
# -g : config file for GNB
src/app.py -t 20 -i 0 -n 1 -f /tmp/core-tg -u src/config/oai-cn5g-ue.yaml -g src/config/oai-cn5g-gnb.yaml
```


After much headache I found the answer. Could not resolve 'archive.ubuntu.com' can be fixed by making the following changes:

Uncomment the following line in /etc/default/docker
DOCKER_OPTS="--dns 8.8.8.8 --dns 8.8.4.4"

Restart the Docker service sudo service docker restart

Delete any images which have cached the invalid DNS settings.

Build again and the problem should be solved.

## Simulate PCFP with UPF

```bash
docker run -d --name oai-upf -p 2152:2152 -p 8805:8805 -p 8080:8080 --net=demo-oai oai-upf:develop
```