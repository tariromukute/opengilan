# The file docments the set up and testing of the Open5gs core network

The desired set up has two virtual machines, VM-ueransim and VM-open5gs, running the [UERANSIM](https://github.com/aligungr/UERANSIM/wiki) and the open source 5G core [Open5GS](https://open5gs.org) resepectively. The test set up will have simulated 5G traffic being sent from the VM-ueransim for load testing and validation of the set up. Executed the following steps:

- [x] Deployed two virtual machines (VM-ueransim and VM-free5gc) on Azure. Use this project ansible playbook for deployment.
- [x] Install the Open 5GS according to the [installation guide](https://open5gs.org/open5gs/docs/guide/01-quickstart/)
- [x] Install UERANSIM according to the [installation guide](https://github.com/aligungr/UERANSIM/wiki/Installation). Where as the free5gc points to checout to the version v3.1.0, Open 5GS works with the master branch. There have been changes since v3.1.0 that accomodate the changes on opn 5gs latest release.
- [x] Configure the Open 5GS config files to bind the AMF and UPF network functions to the IP of VM-open5gs. See below sections for which updates to make.
- [x] Update the Linux Host Network Settings to allow for data plane traffic from the UE to flow
- [x] Update the config file for the UERANSIM to send traffic to VM-open5gs. See below sections for which updates to make.
- [ ] Add a subscriber using the webui. To access the webui remotely you need to establish a port forwarding tunnel `ssh -L 8000:localhost:3000 azureuser@olan153sut.westeurope.cloudapp.azure.com -i ~/.ssh/id_rsa`. Username: admin, Password: 1423
- [x] Add a UE subscriber to the Open5gs. Use the default imsi from the `~/UERANSIM/config/open5gs-ue.yaml`. Run the following command on VM-open6gs `open5gs-dbctl add 999700000000001 465B5CE8B199B49FAA5F0A2EE238A6BC E8ED289DEBA952E4283B54E88E6183CA`
- [x] Start the gNB on VM-ueransim `cd ~/UERANSIM & build/nr-gnb -c config/open5gs-gnb.yaml`
- [x] Establish a PDU session for the registered UE `cd ~/UERANSIM & sudo build/nr-ue -c config/open5gs-ue.yaml`
- [x] Send a ping request using the established PDU session `ping -I uesimtun0 google.com`
- [x] Register multiple UEs for load testing. See the `Register multiple UEs for load testing` section below
- [x] Download the db dump of the subscribers for later use. To dump the db, on the VM-open5gs run the command `mongodump`. Fetch the dump from the VM-open5gs using the command `scp -r azureuser@<ip_addpress>:/home/azureuser/dump .`. You should delete the admin folder from the fetched dump.
- [ ] To restore the db later on you run the command `mongorestore` on VM-open5gs on the path with the dump folder.



*** Update the AMF config file ***

- set __NGAP_IP__ to the IP of VM-open5gs

```bash

# amf config file locates in /etc/open5gs/amf.yaml
# ngap addr configured to 5g core server ip
amf:
    sbi:
      - addr: 127.0.0.5
        port: 7777
    ngap:
      - addr: __NGAP_IP__
     
---

# restart amf services
sudo systemctl restart open5gs-amfd

---
```
*** Update the AMF config file ***

- set __GTPU_IP__ to the IP of VM-open5gs

```bash
# upf config file locates in /etc/open5gs/upf.yaml
# gtpu addr configured to 5g core server ip
upf:
    pfcp:
      - addr: 127.0.0.7
    gtpu:
      - addr: __GTPU_IP__
    subnet:
      - addr: 10.45.0.1/16
      - addr: 2001:230:cafe::1/48
      
---

# restart upf services
sudo systemctl restart open5gs-upfd

---
```

*** Update the Linux Host Network Settings ***

```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -o <dn_interface> -j MASQUERADE
sudo iptables -A FORWARD -p tcp -m tcp --tcp-flags SYN,RST SYN -j TCPMSS --set-mss 1400
sudo systemctl stop ufw
```

*** Update UERANSIM gnb config file ***

- set __NGAP_IP__ and __GTP_IP__ to the IP of VM-ueransim
- set __AMF_IP__ to the IP of VM-open5gs

```bash
# the config file is located in ~/UERANSIM/config/open5gs-gnb.yaml
----
linkIp: 127.0.0.1   # gNB's local IP address for Radio Link Simulation (Usually same with local IP)
ngapIp: __NGAP_IP__  # gNB's local IP address for N2 Interface (Usually same with local IP)
gtpIp: __GTP_IP__    # gNB's local IP address for N3 Interface (Usually same with local IP)

# List of AMF address information
amfConfigs:
  - address: __AMF_IP__
    port: 38412
```

*** Register multiple UEs for load testing ***

```bash
imsi=9997000000000001

for i in {0..9000}
do
    open5gs-dbctl add  $[imsi + i] 465B5CE8B199B49FAA5F0A2EE238A6BC E8ED289DEBA952E4283B54E88E6183CA
    echo "Registered IMSI $[imsi + i] times"
done
```
