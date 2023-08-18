# Tool(s) for inspecting the performance of SCTP

The folder details the development of tool(s) to get the performance of STCP. The context of the work is for the 5G network during registration estabilshment. Want to measure and compare the performance of different 5G core networks during registration procedure.

**Existing tools**
- [iperf](https://iperf.fr): it can measure bandwidth, report MSS/MTU size etc, however it can't inspect and provide the measures for a connection active between other applications. Therefore for our use cases - inspecting the performance of SCTP between 5G traffic generator and 5G CN it won't work.
- [NetPerfMeter](https://doc.omnetpp.org/inet/api-current/neddoc/inet.applications.netperfmeter.NetPerfMeter.html) similar limitation to iperf
- [netstat]() Can be used for monitoring the network status 


**Monitoring SCTP netwowk status with netstat**

Install netstat `sudo apt install net-tools`

- To monitor the network status we can use `netstat -S`. However this throws an error `netstat: no support for `AF INET (sctp)' on this system.` when the kernel headers for SCTP are not present.

***netstat command***

There are a couple of options from netstat that can give us different information
- `netstat -S -c`: this will print STCP stats every minute (continously `-c`).
    - From this we can get the changes in the `Recv-Q` and `Send-Q`.
    - We get the number of connections and there state, ESTABLISHED etc
- `netstat -S -s`: this will print the summary statistics for SCTP connects see below for a sample

For  information on what some of the keys mean like InECT0Pkts see [this](https://docs.kernel.org/networking/snmp_counter.html) and [SCTP counters is in RFC 3873](https://www.ietf.org/rfc/rfc3873.txt) or [man page](https://linux.die.net/man/7/sctp)
```txt
IcmpMsg:
    InType0: 5
    InType3: 92
    OutType3: 92
    OutType8: 10
UdpLite:
IpExt:
    InOctets: 116600152
    OutOctets: 4339692
    InNoECTPkts: 34697
    InECT0Pkts: 3499
Sctp:
    0 Current Associations
    10 Active Associations
    0 Passive Associations
    1 Number of Aborteds 
    9 Number of Graceful Terminations
    0 Number of Out of Blue packets
    0 Number of Packets with invalid Checksum
    3241 Number of control chunks sent
    5614 Number of ordered chunks sent
    0 Number of Unordered chunks sent
    3488 Number of control chunks received
    3897 Number of ordered chunks received
    0 Number of Unordered chunks received
    0 Number of messages fragmented
    0 Number of messages reassembled 
    3510 Number of SCTP packets sent
    3499 Number of SCTP packets received
    SctpDelaySackExpireds: 1
    SctpInPktSoftirq: 3493
    SctpInPktBacklog: 6
```

Results for running `netstat -S -c` on the cn-tg VM

```txt
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
sctp       0      0 ue:59058                48.0.70.132:38412       ESTABLISHED
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
sctp       0      0 ue:59058                48.0.70.132:38412       ESTABLISHED
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
sctp       0   1024 ue:59058                48.0.70.132:38412       ESTABLISHED
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
sctp       0   1024 ue:59058                48.0.70.132:38412       ESTABLISHED
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
sctp       0   2048 ue:59058                48.0.70.132:38412       ESTABLISHED
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
sctp       0   3072 ue:59058                48.0.70.132:38412       ESTABLISHED
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
sctp       0   1024 ue:59058                48.0.70.132:38412       ESTABLISHED
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
sctp       0      0 ue:59058                48.0.70.132:38412       ESTABLISHED
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
sctp       0   2048 ue:59058                48.0.70.132:38412       ESTABLISHED
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
sctp       0   2048 ue:59058                48.0.70.132:38412       ESTABLISHED
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
sctp       0      0 ue:59058                48.0.70.132:38412       ESTABLISHED
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
sctp       0   9216 ue:59058                48.0.70.132:38412       ESTABLISHED
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
sctp       0  15360 ue:59058                48.0.70.132:38412       ESTABLISHED
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
sctp       0   5120 ue:59058                48.0.70.132:38412       ESTABLISHED
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
sctp       0   6144 ue:59058                48.0.70.132:38412       ESTABLISHED
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
sctp       0  17408 ue:59058                48.0.70.132:38412       ESTABLISHED
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
sctp       0   9216 ue:59058                48.0.70.132:38412       ESTABLISHED
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
```

We can see that the Send-Q grows whereas the Recv-Q remains at 0.

**Monitoring SCTP netwowk status with nstat**

netstat is being depricated in favour of nstat. One advantage of nstat is it should stats from the previous run, however it doesn't show the stats of the Queues.

Load the SCTP kernel headers.

`Note: When using VM on Openstack the ****-disk-kvm.img image fail to load the module. Try ****-amd64.img`

```bash
# Check if sctp module is loaded
lsmod | grep sctp

# Locate the sctp module (if it's not loaded)
modinfo sctp

# Linux extra modules which will include sctp module (if the sctp module was not located above)
sudo apt install linux-generic

# Check for module location
modinfo sctp

# Load the sctp module
insmod <path_to_module>
```

**Developing bpf tool**

- list all kprobes and tracepoints associated with sctp either using bpftrace `sudo bpftrace -l | grep sctp` or with bcc tools `sudo python3 tplist.py | grep sctp`, the bcc one list tracepoints only.
- To see the arguments for kprobe or tracepoint `bpftrace -lv tracepoint:syscalls:sys_enter_open`

```bash
# bpftrace -lv "struct path"
struct path {
        struct vfsmount *mnt;
        struct dentry *dentry;
};
```
- Check out [this](https://blog.quarkslab.com/defeating-ebpf-uprobe-monitoring.html) article on how to leverage uprobes. This can be using to inspect sctp performance from user space.

When the kernel module for sctp is not installed, only a few security kprobes for SCTP are present. To get more kprobes and tracepoints for SCTP install the kernel modules for SCTP. See the guide above on how to load the kernel modules.

- Kernel injects the sctp_probe tracepoint https://github.com/torvalds/linux/blob/4d6d4c7f541d7027beed4fb86eb2c451bd8d6fff/net/sctp/sm_statefuns.c#L3360 and sctp_probe_path https://github.com/torvalds/linux/blob/4d6d4c7f541d7027beed4fb86eb2c451bd8d6fff/net/sctp/outqueue.c#L1243

**Getting SCTP RTT**
- Linux defines 30 seconds HEARTBEAT interval https://elixir.bootlin.com/linux/v5.4/source/include/net/sctp/constants.h#L245. It then defines a HB interval for each transport (remote address) https://elixir.bootlin.com/linux/v5.4/source/include/net/sctp/structs.h#L773. It also defines it in the association struct https://elixir.bootlin.com/linux/v5.4/source/include/net/sctp/structs.h#L1551
- The Linux sctp_sock struct has a parameter to change the heartbeat interval https://elixir.bootlin.com/linux/v5.4/source/include/net/sctp/constants.h#L245
- Handles the notification of the SCTP app (ULP) on HB, there are different conditions to it though https://elixir.bootlin.com/linux/v5.4/source/net/sctp/associola.c#L779
- https://elixir.bootlin.com/linux/v5.4/source/net/sctp/outqueue.c#L824 sends the HB to transport
- Linux has a kprobe for creating the heartbeat and heartbeat_ack chuck https://elixir.bootlin.com/linux/v5.4/source/net/sctp/sm_make_chunk.c#L1142 and https://elixir.bootlin.com/linux/v5.4/source/net/sctp/sm_make_chunk.c#L1171
- Linux has a kprobe for generating heartbeat, it delays sending heartbeak if the socket it busy `if (sock_owned_by_user(sk)) {` https://elixir.bootlin.com/linux/v5.4/source/net/sctp/sm_sideeffect.c#L362
- The kprobe `sctp_do_8_2_transport_strike` https://elixir.bootlin.com/linux/v5.4/source/net/sctp/sm_sideeffect.c#L525 handles expiration of T3-rtx timer which is also happens for heartbeat
- Helper function to handle the reception of an HEARTBEAT ACK https://elixir.bootlin.com/linux/v5.4/source/net/sctp/sm_sideeffect.c#L717
- Linux has a helper function Update transport's RTO based on the newly calculated RTT `sctp_transport_update_rto`. https://elixir.bootlin.com/linux/v5.4/source/net/sctp/transport.c#L330. Can use this to check the changes in the HB. However this is called from two different points
1. When handling a HB https://elixir.bootlin.com/linux/v5.4/source/net/sctp/sm_sideeffect.c#L778
2. When chunk is being used for RTT https://elixir.bootlin.com/linux/v5.4/source/net/sctp/outqueue.c#L1466 

We can use iperf to test the tool. On the server `iperf3 -s` and on the client either `iperf3 -c 10.0.0.21 --sctp`.

`Note: An SCTP program needs to be running in order for the sctp kprobe to attach`

```bash
# BCC
# Throws error could not determine address of symbol sctp_transport_update_rto in /lib/x86_64-linux-gnu/libc.so.6
sudo python3 argdist.py -C 'p:c:sctp_transport_update_rto(struct sctp_transport *tp, __u32 rtt):u32:rtt'

# bpftrace

# List arguments.
# This is not supported, didn't produce results
bpftrace -l 'kprobe:sctp_transport_update_rto' -v 

# Check if we can get the rtt values
bpftrace -e 'kprobe:sctp_transport_update_rto { printf("%-6d %-16s %d\n", pid, comm, arg1); }'

# Check the struct, only works when BTF is enabled.
# This is not enable on the system currently
bpftrace -lv "struct sctp_transport"

# Count the number of occurance for a rtt difference
bpftrace -e 'kprobe:sctp_transport_update_rto { @[arg1] = count(); }'

# Show the histogram for the calculated rtt
bpftrace -e 'kprobe:sctp_transport_update_rto { @rtt = hist(arg1); }'

# Get the rtt per transport. This will print per memory address of the transport
bpftrace -e '
#include <net/sctp/structs.h>
#include <linux/socket.h>
#include <net/sctp/sctp.h>
kprobe:sctp_transport_update_rto { 
    $tp = (struct sctp_transport *)arg0;
    $sk = $tp->ipaddr.v4;
    $saddr = ntop(0);
    $saddr = ntop(AF_INET, $sk.sin_addr.s_addr);
    @rtt[$saddr] = hist(arg1); }'

bpftrace -e '
#include <net/sctp/structs.h>
#include <net/sctp/sctp.h>
#ifndef BPFTRACE_HAVE_BTF
#include <linux/socket.h>
#include <net/sock.h>
#else
#include <sys/socket.h>
#endif
kprobe:sctp_transport_update_rto { 
    $tp = (struct sctp_transport *)arg0;
    $saddr = ntop(0);
    if ($tp->ipaddr.sa.sa_family == AF_INET) {
        $sk = $tp->ipaddr.v4;
        $saddr = ntop(AF_INET, $sk.sin_addr.s_addr);
    } else {
        // AF_INET6
        $sk6 = $tp->ipaddr.v6;
        $saddr = ntop(AF_INET6, $sk6.sin6_addr.in6_u.u6_addr8);
    }
    @rtt[$saddr] = hist(arg1); }'
```

The kprobe sctp_transport_update_rto is called a lot of times mainly by chunk is being used for RTT https://elixir.bootlin.com/linux/v5.4/source/net/sctp/outqueue.c#L1466. The frequency provides granular results by will have high overhead. To reduce the overhead we need a tool that calculates the RTT from HB packates only. These are sent every 30 seconds be default see [code](https://elixir.bootlin.com/linux/v5.4/source/include/net/sctp/constants.h#L245). This can be changed when setting up the connection. The kprobe `sctp_cmd_transport_on`  handles the reception of HEARTBEAT ACK and calculates the RTT. Since the RTT is calculated internally and not exposed through arguments or return values, the bpftrace script has to calculate the RTT like the kprobe does.

```bash
# List arguments.
# This is not supported, didn't produce results
bpftrace -l 'kprobe:sctp_cmd_transport_on' -v

# Get struct with details to calculate rtt (sctp_sender_hb_info)
# Getting error: ERROR: Unknown identifier: 'jiffies'
bpftrace -e '
#include <net/sctp/structs.h>
#include <linux/jiffies.h>
kprobe:sctp_cmd_transport_on {
    $hbinfo = (struct sctp_sender_hb_info *)arg3->skb->data;
    $rtt = jiffies - $hbinfo->sent_at;
    @[$rtt] = count();
    }'

```

**Getting the SCTP cwnd and rwnd overtime**

- The tracepoint `sctp_probe_path` https://elixir.bootlin.com/linux/v5.4/source/include/trace/events/sctp.h#L11 has an argument that gives cwnd
- The tracepoint `sctp_probe` https://elixir.bootlin.com/linux/v5.4/source/include/trace/events/sctp.h#L50 has an argument that gives rwnd
- Initialises the cwnd for an association https://elixir.bootlin.com/linux/v5.4/source/net/sctp/associola.c#L680, this seem to be done also on https://elixir.bootlin.com/linux/v5.4/source/net/sctp/socket.c#L524
- Applications can retrive the SCTP stats by calling https://elixir.bootlin.com/linux/v5.4/source/net/sctp/socket.c#L5423. The app will need to supply the above details
- Applications can retrive information about SCTP peer https://elixir.bootlin.com/linux/v5.4/source/net/sctp/socket.c#L5503
- [] Can bpftrace call kernel functions, e.g., the one above?
- `sctp_transport_raise_cwnd` increase the cwnd and partial_bytes acknowledged https://elixir.bootlin.com/linux/v5.4/source/net/sctp/transport.c#L397. However it's always that the cwnd will be increased. If certain conditions are not met the function returns without increasing the transport cwnd
    - This called from `sctp_check_transmitted`
        - This called in `sctp_outq_sack` when the SACK are being processed. https://elixir.bootlin.com/linux/v5.4/source/net/sctp/outqueue.c#L1221. We can get the rwnd from this probe
- `sctp_transport_lower_cwnd` descreases the cwnd and partial_bytes acknowledged https://elixir.bootlin.com/linux/v5.4/source/net/sctp/transport.c#L495. The kprobe also takes the reason for lowering the cwnd. When the reason is `SCTP_LOWER_CWND_FAST_RTX` it is possible that the function returns without updating cwnd due to some conditions not being met.
    - Called from `sctp_retransmit`
- `sctp_transport_burst_limited` updates the cwnd depending, not always that it's updated
    - Called from `sctp_outq_select_transport` and `sctp_outq_flush_data`
- `sctp_transport_burst_reset` resets the cwnd
    - Called from `sctp_outq_flush_transports`
- `sctp_transport_reset` resets the variables to initial values.
    - Called from `sctp_assoc_update`
- We can inspect on extry and exit to compute whether there is change in cwnd
- The `sctp_gen_sack` sets the advertised window when sending a SACK https://elixir.bootlin.com/linux/v5.4/source/net/sctp/sm_sideeffect.c#L138
- The `sctp_cmd_interpreter` also show the rwnd https://elixir.bootlin.com/linux/v5.4/source/net/sctp/sm_sideeffect.c#L1252
- `sctp_packet_append_data` does management when adding DATA chunk which includes updating the rwnd
- `sctp_assoc_rwnd_increase` updates the receive window https://elixir.bootlin.com/linux/v5.4/source/net/sctp/associola.c#L1467
- `sctp_assoc_rwnd_decrease` updates the receive window https://elixir.bootlin.com/linux/v5.4/source/net/sctp/associola.c#L1526
- 

**Build for cwnd**
```bash
# List arguments.
# This is not supported, didn't produce results
bpftrace -lv t:sctp:sctp_probe_path

# Check is we get the cwnd argument
# This returns error: ERROR: tracepoint not found: sctp:sctp_probe_path, need to make sure the sctp lib is loaded (run the application making use of SCTP)
# The tracepoint seems to be implement in the source code but it doesn't show on the list of tracepoints
bpftrace -e '
#include <net/sctp/structs.h>
tracepoint:sctp:sctp_probe_path { printf("%s %d\n", comm, args->cwnd); }'

# Use the probe for raising cwnd
# This is not supported, didn't produce results
bpftrace -lv kprobe:sctp_transport_raise_cwnd

# Check for the value of cwnd when system is asking for it to be raised
bpftrace -e '
#include <net/sctp/structs.h>
kprobe:sctp_transport_raise_cwnd { 
    $tp = (struct sctp_transport *)arg0;
    $saddr = ntop(0);
    if ($tp->ipaddr.sa.sa_family == AF_INET) {
        $sk = $tp->ipaddr.v4;
        $saddr = ntop(AF_INET, $sk.sin_addr.s_addr);
    } else {
        // AF_INET6
        $sk6 = $tp->ipaddr.v6;
        $saddr = ntop(AF_INET6, $sk6.sin6_addr.in6_u.u6_addr8);
    }
    @cwnd[$saddr] = hist($tp->cwnd);
    }'

# Check for the value of cwnd when system is asking for it to be lowered
bpftrace -e '
#include <net/sctp/structs.h>
kprobe:sctp_transport_lower_cwnd { 
    $tp = (struct sctp_transport *)arg0;
    $saddr = ntop(0);
    if ($tp->ipaddr.sa.sa_family == AF_INET) {
        $sk = $tp->ipaddr.v4;
        $saddr = ntop(AF_INET, $sk.sin_addr.s_addr);
    } else {
        // AF_INET6
        $sk6 = $tp->ipaddr.v6;
        $saddr = ntop(AF_INET6, $sk6.sin6_addr.in6_u.u6_addr8);
    }
    @cwnd[$saddr, arg1] = hist($tp->cwnd);
    printf("%s %d\n", comm, $tp->cwnd);
    }'

# Record when the cwnd only when changes
bpftrace -e '
#include <net/sctp/structs.h>
BEGIN { 
    @cwnd = (uint32) 0;
}

tracepoint:sctp:sctp_probe_path /@cwnd != args->cwnd / {
    $addr = (union sctp_addr *)args->ipaddr; 
    $saddr = ntop(0);
    if ($addr->sa.sa_family == AF_INET) {
        $sk = $addr->v4;
        $saddr = ntop(AF_INET, $sk.sin_addr.s_addr);
    } else {
        // AF_INET6
        $sk6 = $addr->v6;
        $saddr = ntop(AF_INET6, $sk6.sin6_addr.in6_u.u6_addr8);
    }
    @cwnd = args->cwnd;
    @delta[$saddr, strftime("%H:%M:%S:%f", nsecs)] = args->cwnd;
}

END {
    clear(@cwnd)
}'
```

**Build for rwnd**

```bash
# List arguments.
bpftrace -lv t:sctp:sctp_probe

# Check is we get the rwnd argument
bpftrace -e '
#include <net/sctp/structs.h>
tracepoint:sctp:sctp_probe { printf("%s rwnd %d asoc %d bind_port %d peer_port %d unack_data %d \n", comm, args->rwnd, args->asoc, args->bind_port, args->peer_port, args->unack_data); }'

# Record when the rwnd only when changes
bpftrace -d -e '
#include <net/sctp/structs.h>
BEGIN { 
    @rwnd = (uint32) 0;
}

tracepoint:sctp:sctp_probe /@rwnd != args->rwnd / {
    @rwnd = args->rwnd;
    @delta[nsecs] = args->rwnd;
}

END {
    clear(@rwnd)
}'
```


Test rtt using iperf and the cn-tg. With OAI the amf is running inside a container. We need to run the iperf server inside the container. The default iperf installed from apt on the container has issue with SCTP connections see [issue](https://github.com/esnet/iperf/issues/620#issuecomment-385615317). Installed a version X from source. The installation from source on a container didn't work. It always seemed to install the wrong version to the one downloaded.

```bash
wget https://downloads.es.net/pub/iperf/iperf-3.7.tar.gz

tar -xf iperf-3.7.tar.gz

cd iperf-3.7
apt install -y libtool
apt install -y make
./configure --disable-dependency-tracking
make
make install

```
## Gotchas
- Seems like there is no way to reset the stats from netstat either than reboot the machine and possibly putting the interface down and up. It will always show cummulative stats and not delta values. An alternative tool nstat can show delta values, see [thread](https://superuser.com/questions/1590901/reset-netstat-statistics)