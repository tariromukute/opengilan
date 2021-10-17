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

dpdk-testpmd -w  aa1b:00:02.0 \
  --vdev="net_vdev_netvsc0,iface=eth1" \
  -- -i \
  --port-topology=chained
```

Delete resources

```bash
az group delete --name opengilan
```


## Useful Resources

- [Setting up Virtual Machines for DPDK](https://blog.emumba.com/setting-up-virtual-machines-for-dpdk-da1b49a9bf5f)