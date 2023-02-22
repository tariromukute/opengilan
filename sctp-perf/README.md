# Tool(s) for inspecting the performance of SCTP

The folder details the development of tool(s) to get the performance of STCP. The context of the work is for the 5G network during registration estabilshment. Want to measure and compare the performance of different 5G core networks during registration procedure.

**Existing tools**
- [iperf](https://iperf.fr): it can measure bandwidth, report MSS/MTU size etc, however it can't inspect and provide the measures for a connection active between other applications. Therefore for our use cases - inspecting the performance of SCTP between 5G traffic generator and 5G CN it won't work.
- [NetPerfMeter](https://doc.omnetpp.org/inet/api-current/neddoc/inet.applications.netperfmeter.NetPerfMeter.html) similar limitation to iperf
- [netstat]() Can be used for monitoring the network status 


**Monitoring SCTP netwowk status with netstat**

- To monitor the network status we can use `netstat -S`. However this throws an error `netstat: no support for `AF INET (sctp)' on this system.` when the kernel headers for SCTP are not present.

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

**Developing bpftrace tool**

- `sudo bpftrace -l | grep sctp` list all kprobes and tracepoints associated with sctp
- Check out [this](https://blog.quarkslab.com/defeating-ebpf-uprobe-monitoring.html) article on how to leverage uprobes. This can be using to inspect sctp performance from user space.

When the kernel module for sctp is not installed, only a few security kprobes for SCTP are present. To get more kprobes and tracepoints for SCTP install the kernel modules for SCTP. See the guide above on how to load the kernel modules.

