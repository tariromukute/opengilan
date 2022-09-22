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

# OAI images
docker pull oaisoftwarealliance/oai-amf:v1.4.0
docker pull oaisoftwarealliance/oai-nrf:v1.4.0
docker pull oaisoftwarealliance/oai-spgwu-tiny:v1.4.0
docker pull oaisoftwarealliance/oai-smf:v1.4.0
docker pull oaisoftwarealliance/oai-udr:v1.4.0
docker pull oaisoftwarealliance/oai-udm:v1.4.0
docker pull oaisoftwarealliance/oai-ausf:v1.4.0
docker pull oaisoftwarealliance/oai-upf-vpp:v1.4.0
docker pull oaisoftwarealliance/oai-nssf:v1.4.0
# Utility image to generate traffic
docker pull oaisoftwarealliance/trf-gen-cn5g:latest

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

```
sudo sysctl net.ipv4.conf.all.forwarding=1
sudo iptables -P FORWARD ACCEPT
```

### Install UERANSIM on another VM

```bash
ip route add 48.0.0.0/16 via 192.168.222.186

# On terminal 1
build/nr-gnb -c config/oai-cn5g-gnb.yaml

# On terminal 2
sudo build/nr-ue -c config/oai-cn5g-ue.yaml
```

## Notes

Create VM on microstack

```bash
# Get Open stack credentials
sudo snap get microstack config.credentials.keystone-password

# Enable microstack VM to access the internet
sudo iptables -t nat -A POSTROUTING -s 10.20.20.1/24 ! -d 10.20.20.1/24 -j MASQUERADE
sudo sysctl -w net.ipv4.ip_forward=1

# Add image
microstack.openstack --insecure image create --disk-format qcow2 --min-disk 8 --min-ram 512 --file ~/Downloads/focal-server-cloudimg-amd64.img --public 20.04

# Launch instance
microstack launch -f m1.medium -n oai 20.04

microstack launch -f m1.small -n ue 20.04

# (1) Add a static route to the Router (with 48.0.0.0/16 in our case)
microstack.openstack router set <router> \
    --route destination=48.0.0.0/16,gateway=<ip-address-oai>
    
# (2) Add Allowed Address Pairs under the instance interface (48.0.0.0/16 in our case)
microstack.openstack port set <port-id> --allowed-address ip-address=48.0.0.0/16
```

- Tried running the OAI on Ubuntu 20.04 VM on microstack. The oai-amf container failed with socket error. Realised that this was due to the SCTP module missing on the kernel `lsmod | grep sctp`. I tried locating the module with `modinfo sctp` but it was not found. I ran `sudo apt install linux-generic` to get the extra modules. I could now find the module and tried loading with `insmod <path_to_module>`. This failed. Turns out I was using the `focal-server-cloudimg-amd64-disk-kvm.img` as recommended or pointed to on one of the Microstack blogs. I switched to creating a VM from image `focal-server-cloudimg-amd64.img`. This also didn't have the SCTP module load but I could find it on the system. I loaded the module `modprobe sctp` and then ran the OAI and this time it worked.