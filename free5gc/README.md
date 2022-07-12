# The file documents the step to testing Free5gc

The initial step is to manually set up and configure the Free5gc and run the different test from the webiste. Used [UERANSIM - a UE/RAN Simulator](https://www.free5gc.org/installations/stage-3-sim-install/) for testing the Free5gc. Executed the following steps:

- [x] Deployed two virtual machines (VM-ueransim and VM-free5gc) on Azure in a Vnet with the following address space `192.168.0.0/16` as per the [installation guide](https://www.free5gc.org/installations/stage-3-sim-install/). VM-free5gc with static ip address `192.168.56.101` and VM-ueransim with static ip address `192.168.56.102`. See [link](https://docs.microsoft.com/en-us/azure/virtual-network/ip-services/virtual-networks-static-private-ip-arm-pportal) on how to assign static ip address.
- [x] Deploy a virtual machine with at least the minimum requirements as describe on the [repo](https://github.com/free5gc/free5gc/wiki/Environment#recommended-environment)
- [x] Install Free5gc according to the [installation guide](https://github.com/free5gc/free5gc/wiki/Installation)
- [x] Install UERANSIM according to the [installation guide](https://www.free5gc.org/installations/stage-3-sim-install/)
- [x] Install the Webconsole on free5gc and add a test subscriber (keep default, only change “Operator Code Type” field, select “OP”)
- [x] Update the Free5gc configuration files a per [guide](https://www.free5gc.org/installations/stage-3-sim-install/)
- [x] Run the Free5gc as describe in the [guide](https://github.com/free5gc/free5gc/wiki/Run), skipped the stage of running the N3IWF. Also see the [ueransim guide](https://www.free5gc.org/installations/stage-3-sim-install/)
- [x] Run UERANSIM see [guide](https://www.free5gc.org/installations/stage-3-sim-install/)
- [x] Capture the packets during successful ping using the tunnel `ping -I uesimtun0 google.com`. The setup using GTP protocol with UDP so capture the UDP packets on the main interface with `sudo tcpdump -i eth0 proto UDP`. To create a pcap file for analysing later `sudo tcpdump -i eth0 proto UDP -A -w pcap/udp_gtp.pcap`. To dump the contents of the pcap file `tcpdump -ttttnnr pcap/udp_gtp.pcap`.
- [x] Download the file to use with packet generator `scp -i <key>.pem azureuser@<ip_addpress>:/home/azureuser/pcap/udp_gtp.pcap free5gc/`
- [ ] Deploy a TREX and send traffic to VM-free5gc
- [ ] Deploy the OpenGiLAN-bench and manually set up the Free5gc as above and start the tests