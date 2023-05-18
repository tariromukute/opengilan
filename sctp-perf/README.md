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
- Check out [this](https://blog.quarkslab.com/defeating-ebpf-uprobe-monitoring.html) article on how to leverage uprobes. This can be using to inspect sctp performance from user space.

When the kernel module for sctp is not installed, only a few security kprobes for SCTP are present. To get more kprobes and tracepoints for SCTP install the kernel modules for SCTP. See the guide above on how to load the kernel modules.

- Kernel injects the sctp_probe tracepoint https://github.com/torvalds/linux/blob/4d6d4c7f541d7027beed4fb86eb2c451bd8d6fff/net/sctp/sm_statefuns.c#L3360 and sctp_probe_path https://github.com/torvalds/linux/blob/4d6d4c7f541d7027beed4fb86eb2c451bd8d6fff/net/sctp/outqueue.c#L1243

## Gotchas
- Seems like there is no way to reset the stats from netstat either than reboot the machine and possibly putting the interface down and up. It will always show cummulative stats and not delta values. An alternative tool nstat can show delta values, see [thread](https://superuser.com/questions/1590901/reset-netstat-statistics)