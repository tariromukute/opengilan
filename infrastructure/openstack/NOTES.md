
```bash
# Login openstack cli
source OpenCN-tg-openrc.sh

# Get net id for private network
PRIVATE_NET_ID=$(openstack network show opencn_tg-vxlan -c id -f value)

# Create ports
openstack port create --network $PRIVATE_NET_ID --fixed-ip subnet=bba3391a-e76c-4cfa-bcee-07d01a4d6886 tx-port-1 --vnic-type direct-physical

openstack port create --network $PRIVATE_NET_ID --fixed-ip subnet=36552a55-0918-423f-8e46-4892f48a2e09 tx-port-2 --vnic-type direct-physical

openstack port create --network $PRIVATE_NET_ID --fixed-ip subnet=cf008c1e-c0cd-4453-b8fd-71d03fba2bbe tx-port-3

# Enable Virtio-net multiqueue
openstack image set --property hw_vif_multiqueue_enabled=true $IMAGE

# Create server (core network)
openstack server create --flavor M4.medium \
    --image 23.04 \
    --key-name  stack \
    --nic port-id= \
    --nic port-id= \
    tx

openstack floating ip create --project demo --subnet public-subnet public

openstack server add floating ip <server-name> <float-ip>
# Confirm
openstack server list

# Test ping
ping -c 4 <ip-address>

# Confirm SSH into instance
ssh ubuntu@<float-ip>
```

Ensure xdp redirect can run. It needs [separate RX and TX queues](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=672aafd5d88a951f394334802b938b502010d9eb)

```bash
devname=
# Check the number of queues supported
ethtool -l $devname

# Set the number of queues to the number of vCPUs
N=<n# of vCPUs>

ethtool -L $devname combined 2*$N
```

Debug for XDP_REDIRECT

```bash
# Check if xdp program is throwing any errors
sudo bpftrace -e \ 'tracepoint:xdp:xdp_redirect*_err {@redir_errno[-args->err] = count();}  tracepoint:xdp:xdp_devmap_xmit {@devmap_errno[-args->err] = count();}'

# or
echo 1 > /sys/kernel/debug/tracing/events/xdp/enable
cat /sys/kernel/debug/tracing/trace_pipe
```

```python
from scapy.contrib.gtp import GTP_U_Header, GTPPDUSessionContainer
from scapy.all import *
sendp(Ether(dst="02:42:c0:a8:46:86")/
    IP(src="192.168.70.1",dst="192.168.70.134")/
    UDP(dport=2152)/GTP_U_Header(teid=1234)/ GTPPDUSessionContainer(type=1, QFI=5)/ 
    IP(src="12.1.1.1",dst="8.8.8.8",version=4)/
    ICMP(), iface="vethbcccbfd", count=10)
```

## Useful resources
- [XDP ate my packets, and how I debugged it](https://fedepaol.github.io/blog/2023/09/11/xdp-ate-my-packets-and-how-i-debugged-it/)
- [XDP offload with virtio-net](https://netdevconf.info/wiki/doku.php?id=0x13:reports:d2t1t04-xdp-offload-with-virtio-net)
- [Re: XDP redirect throughput with multi-CPU i40e](https://www.spinics.net/lists/xdp-newbies/msg02225.html)
- [error loading xdp program on virtio nic](https://www.spinics.net/lists/xdp-newbies/msg01447.html)
- [Reference bpf_redirect_info via task_struct on PREEMPT_RT](https://www.spinics.net/lists/netdev/msg974458.html)

