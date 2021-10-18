# Deploy test servers for accelerated networking

Create resource group

```bash
az group create --name opengilan --location southafricanorth
```

Deploy ARM template

Get public key

```bash
publickey=$(cat ~/.ssh/id_rsa.pub) 
```

```bash
az deployment group create \
  --name OpenGiLANTemplate \
  --resource-group opengilan \
  --template-file azuredeploy.json \
  --parameters adminUsername=open dnsLabelPrefix=opengilan adminPasswordOrKey="$publickey"
```

ssh into machine

```bash
ssh open@opengilan-gen.southafricanorth.cloudapp.azure.com -i ~/.ssh/id_rsa
```

```bash
# Install dpdk dev
sudo apt install libibverbs-dev libmlx5-1 ibverbs-providers
sudo apt-get install dpdk-dev libdpdk-dev

# Install dpdk
sudo apt-get install dpdk

dpdk-testpmd -w  134d:00:02.0 \
  --vdev="net_vdev_netvsc0,iface=eth1" \
  -- -i \
  --port-topology=chained
```

Delete resources

```bash
az group delete --name opengilan
```

Faced some errors compling the latest versions of DPDK and Pktgen. The note below on the Pktgen repo

`Pktgen: Created 2010-2020 by Keith Wiles @ Intel.com
---

Note: In DPDK 19.08-rc0 a large number of defines and function names were
      changed. In Pktgen  3.7.0 I added a pg_compat.h header to help
      compatibility issues with these name changes. This means versions
      3.6.6 and below will have trouble building with DPDK starting with
      19.08-rc0 or just after the 19.05 release.
`

Mentions that there were changes to DPDK causing compatibility issues. To resolve this compiled with the versions that were tested with, export DPDK version 20.02 and PKTGEN version 20.02.0.

For netvsc
- https://doc.dpdk.org/guides/nics/vdev_netvsc.html

For mlx5 build
- Install OFED
- ./mlnxofedinstall --upstream-libs --dpdk
- gcc automake libnl-route-3-200 graphviz debhelper dpatch libltdl-dev chrpath quilt dkms autoconf swig libnl-route-3-dev libnl-3-dev autotools-dev m4 make
- https://doc.dpdk.org/guides/nics/mlx5.html
## Useful Resources

- [Setting up Virtual Machines for DPDK](https://blog.emumba.com/setting-up-virtual-machines-for-dpdk-da1b49a9bf5f)