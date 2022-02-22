

```bash
# create resource group

az group create --name opengilan --location southafricanorth

az network vnet create \
    --resource-group opengilan \
    --name olanVnet \
    --address-prefix 10.0.0.0/16 \
    --subnet-name olanSubnet0 \
    --subnet-prefix 10.0.1.0/24

az network vnet subnet create \
    --resource-group opengilan \
    --vnet-name olanVnet \
    --name olanSubnet1 \
    --address-prefix 10.0.2.0/24

az network vnet subnet create \
    --resource-group opengilan \
    --vnet-name olanVnet \
    --name olanSubnet2 \
    --address-prefix 10.0.3.0/24

az network nsg create \
    --resource-group opengilan \
    --name olanSecurityGroup

az network nsg rule create \
  --resource-group opengilan \
  --nsg-name olanSecurityGroup \
  --name Allow-SSH-Internet \
  --access Allow \
  --protocol Tcp \
  --direction Inbound \
  --priority 100 \
  --source-address-prefix Internet \
  --source-port-range "*" \
  --destination-address-prefix "*" \
  --destination-port-range 22

az network public-ip create \
    --name olanPublicIp_vm1 \
    --resource-group opengilan

az network public-ip create \
    --name olanPublicIp_vm2 \
    --resource-group opengilan

az network public-ip create \
    --name olanPublicIp_vm3 \
    --resource-group opengilan

az network nic create \
    --resource-group opengilan \
    --name ANLinux_eth0_NIC_vm1 \
    --vnet-name olanVnet \
    --subnet olanSubnet0 \
    --accelerated-networking true \
    --public-ip-address olanPublicIp_vm1 \
    --network-security-group olanSecurityGroup

az network nic create \
    --resource-group opengilan \
    --name ANLinux_eth0_NIC_vm2 \
    --vnet-name olanVnet \
    --subnet olanSubnet0 \
    --accelerated-networking true \
    --public-ip-address olanPublicIp_vm2 \
    --network-security-group olanSecurityGroup

az network nic create \
    --resource-group opengilan \
    --name ANLinux_eth0_NIC_vm3 \
    --vnet-name olanVnet \
    --subnet olanSubnet0 \
    --public-ip-address olanPublicIp_vm3 \
    --network-security-group olanSecurityGroup

az network nic create \
    --resource-group opengilan \
    --name ANLinux_eth1_NIC_vm1 \
    --vnet-name olanVnet \
    --subnet olanSubnet1 \
    --accelerated-networking true

az network nic create \
    --resource-group opengilan \
    --name ANLinux_eth1_NIC_vm2 \
    --vnet-name olanVnet \
    --subnet olanSubnet1 \
    --accelerated-networking true

az network nic create \
    --resource-group opengilan \
    --name ANLinux_eth1_NIC_vm3 \
    --vnet-name olanVnet \
    --subnet olanSubnet1

az network nic create \
    --resource-group opengilan \
    --name ANLinux_eth2_NIC_vm1 \
    --vnet-name olanVnet \
    --subnet olanSubnet2 \
    --accelerated-networking true

az network nic create \
    --resource-group opengilan \
    --name ANLinux_eth2_NIC_vm2 \
    --vnet-name olanVnet \
    --subnet olanSubnet2 \
    --accelerated-networking true

az network nic create \
    --resource-group opengilan \
    --name ANLinux_eth2_NIC_vm3 \
    --vnet-name olanVnet \
    --subnet olanSubnet2

# create vm
az vm create --resource-group opengilan --name TrexUbuntuAN --image Canonical:UbuntuServer:18_04-lts-gen2:18.04.202010140 --size Standard_D16ds_v4 --admin-username azureuser --admin-password trexTesting001 --nics ANLinux_eth0_NIC_vm1 ANLinux_eth1_NIC_vm1 ANLinux_eth2_NIC_vm1

az vm create --resource-group opengilan --name DUTUbuntuAN --image Canonical:UbuntuServer:18_04-lts-gen2:18.04.202010140 --size Standard_D16ds_v4 --admin-username azureuser --admin-password trexTesting001 --nics ANLinux_eth0_NIC_vm2 ANLinux_eth1_NIC_vm2 ANLinux_eth2_NIC_vm2

az vm create --resource-group opengilan --name DUTUbuntuAN2 --image Canonical:UbuntuServer:18_04-lts-gen2:18.04.202010140 --size Standard_D16ds_v4 --admin-username azureuser --admin-password trexTesting001 --nics ANLinux_eth0_NIC_vm3 ANLinux_eth1_NIC_vm3 ANLinux_eth2_NIC_vm3
```

You need to increase the quota to be deploy the number of vCPUs that are needed for the testbed

```
https://portal.azure.com/#blade/Microsoft_Azure_Capacity/UsageAndQuota.ReactView/Parameters/%7B%22subscriptionId%22%3A%2270bc0bb8-73dc-4ae5-8187-2780c07018a1%22%2C%22command%22%3A%22openQuotaApprovalBlade%22%2C%22quotas%22%3A%5B%7B%22location%22%3A%22westeurope%22%2C%22providerId%22%3A%22Microsoft.Compute%22%2C%22resourceName%22%3A%22standardDDSv4Family%22%2C%22quotaRequest%22%3A%7B%22properties%22%3A%7B%22limit%22%3A16%2C%22unit%22%3A%22Count%22%2C%22name%22%3A%7B%22value%22%3A%22standardDDSv4Family%22%7D%7D%7D%7D%5D%7D

# note possible error with az

https://docs.microsoft.com/en-us/answers/questions/729574/deploy-vm-from-azure-cli-failing.html
```
## Dependencies
- sudo apt install binutils
- sudo apt-get install -y librdmacm-dev librdmacm1 build-essential libnuma-dev libmnl-dev
- sudo apt install ibverbs-utils

```bash
git clone https://github.com/cisco-system-traffic-generator/trex-core.git

git checkout v2.89
```

```yaml
cat /etc/trex_cfg.yaml
- version: 2
  interfaces: ['64da:00:02.0', 'f0e7:00:02.0']
  ext_dpdk_opt: ['--vdev=net_vdev_netvsc,ignore=0', '--vdev=net_vdev_netvsc,ignore=0']
  interfaces_vdevs : ['000d3a6b-8d3f-000d-3a6b-8d3f000d3a6b','000d3a6b-8cae-000d-3a6b-8cae000d3a6b']
  rx_desc : 1024
  tx_desc : 1024
  port_bandwidth_gb : 10
  port_speed : 10000
  port_info:
      - ip: 10.0.2.4
        default_gw: 10.0.2.5
      - ip: 10.0.3.4
        default_gw: 10.0.3.5

  platform:
      master_thread_id: 0
      latency_thread_id: 2
      dual_if:
        - socket: 0
          threads: [4, 6, 8, 10]
```

```yaml
cat /etc/trex_cfg.yaml
- version: 2
  interfaces: ['0002:00:02.0', '0003:00:02.0']
  ext_dpdk_opt: ['--vdev=net_vdev_netvsc,ignore=0', '--vdev=net_vdev_netvsc,ignore=0']
  interfaces_vdevs : ['000d3a6b-8d3f-000d-3a6b-8d3f000d3a6b','000d3a6b-8cae-000d-3a6b-8cae000d3a6b']
  rx_desc : 1024
  tx_desc : 1024
  port_bandwidth_gb : 10
  port_speed : 10000
  port_info:
    - dest_mac        :   [0x00,0x0d,0x3a,0x6b,0x89,0x84]    # router mac addr should be taken from DUT
      src_mac         :   [0x00,0x0d,0x3a,0x6b,0x8d,0x3f]  # source mac-addr - taken from ifconfig
    - dest_mac        :   [0x00,0x0d,0x3a,0x6b,0x8c,0xd9]  # router mac addr  taken from DUT
      src_mac         :   [0x00,0x0d,0x3a,0x6b,0x8c,0xae]  #source mac-addr  taken from ifconfig

  platform:
      master_thread_id: 0
      latency_thread_id: 2
      dual_if:
        - socket: 0
          threads: [4, 6, 8, 10]
```

```yaml
cat /etc/trex_cfg.yaml
- version: 2
  interfaces: ['0002:00:02.0', '0003:00:02.0']
  ext_dpdk_opt: ['--vdev=net_vdev_netvsc,ignore=0', '--vdev=net_vdev_netvsc,ignore=0']
  interfaces_vdevs : ['000d3a6b-8d3f-000d-3a6b-8d3f000d3a6b','000d3a6b-8cae-000d-3a6b-8cae000d3a6b']
  rx_desc : 1024
  tx_desc : 1024
  port_bandwidth_gb : 10
  port_speed : 10000
  port_info:
    - dest_mac        :   [0x00,0x0d,0x3a,0x6b,0x89,0x84]    # router mac addr should be taken from DUT
      ip              :   10.0.2.5  # source mac-addr - taken from ifconfig
    - dest_mac        :   [0x00,0x0d,0x3a,0x6b,0x8c,0xd9]  # router mac addr  taken from DUT
      ip              :   10.0.3.5  #source mac-addr  taken from ifconfig

  platform:
      master_thread_id: 0
      latency_thread_id: 2
      dual_if:
        - socket: 0
          threads: [4, 6, 8, 10]
```

```bash
sudo route add -net 16.0.0.0 netmask 255.0.0.0 gw 10.90.130.202
sudo route add -net 48.0.0.0 netmask 255.0.0.0 gw 10.90.23.202

sudo ethtool -K enP2s2 tso off gro off gso off
sudo ethtool -K enP3s3 tso off gro off gso off
```

```bash
sudo ./t-rex-64 -i -c 2 -v 7 --no-ofed-check

./trex-console
trex> tui
tui> start -f stl/bench.py -m 800kpps --port 0 1 --force -t size=1514
```
```json
{
  "fqdns": "",
  "id": "/subscriptions/4a773cbf-c3ed-42a2-8080-bb5ff4a3340d/resourceGroups/opengilan/providers/Microsoft.Compute/virtualMachines/TrexUbuntuAN",
  "location": "southafricanorth",
  "macAddress": "00-0D-3A-6B-8A-85,00-0D-3A-6B-8D-3F,00-0D-3A-6B-8C-AE",
  "powerState": "VM running",
  "privateIpAddress": "10.0.1.4,10.0.2.4,10.0.3.4",
  "publicIpAddress": "20.87.24.255",
  "resourceGroup": "opengilan",
  "zones": ""
}
```

```json
{
  "fqdns": "",
  "id": "/subscriptions/4a773cbf-c3ed-42a2-8080-bb5ff4a3340d/resourceGroups/opengilan/providers/Microsoft.Compute/virtualMachines/DUTUbuntuAN",
  "location": "southafricanorth",
  "macAddress": "00-0D-3A-6B-7B-73,00-0D-3A-6B-89-84,00-0D-3A-6B-8C-D9",
  "powerState": "VM running",
  "privateIpAddress": "10.0.1.5,10.0.2.5,10.0.3.5",
  "publicIpAddress": "102.37.124.134",
  "resourceGroup": "opengilan",
  "zones": ""
}
```

## Notes
- Had issues with running trex. Trex sends an ARP request first then uses the returned to send traffic. On azure, the ARP is responded to by the same MAC `12:34:56:78:9a:bc`. See [link](https://www.untangled.eu/2017/07/networking-in-microsoft-azure-part-1/) for more details.

- Turns out the above is not the issue. For azure to route the traffic from the TREX VM to the DUT VM (Which acts as a Virtual Appliance in our case) need to add User Defined Route see [link](https://github.com/uglide/azure-content/blob/master/articles/virtual-network/virtual-networks-udr-overview.md) for more details. Also need to enable IP forwarding on the NIC and in the VM.

# Useful Resources
- [Azure with netvsc DPDK driver (v2.89)](https://github.com/cisco-system-traffic-generator/trex-core/wiki/Azure-with-netvsc-DPDK-driver-(v2.89))
- [TREX always getting same MAC on ARP before starting - NETWORKING IN MICROSOFT AZURE – PART I](https://www.untangled.eu/2017/07/networking-in-microsoft-azure-part-1/)
- [What are User Defined Routes and IP Forwarding?](https://github.com/uglide/azure-content/blob/master/articles/virtual-network/virtual-networks-udr-overview.md)