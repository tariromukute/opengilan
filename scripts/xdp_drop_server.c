/*  TC (Traffic Control) eBPF echo server
 *
 * 1. Compile with clang bpf
 *    clang -O2 -target bpf -g -c tc_drop_server.c -o tc_drop_server.o
 *    `The -g flag is important. clang to generate debug info (including .BTF ELF section) needed for loading the btf maps`
 * 2. Load program using bpftool
 *    sudo tc filter add dev <dev_name> ingress bpf da obj tc_drop_server.o sec ingress_drop
 * 3. Check if the map has been pinned
 *    sudo bpftool map dump pinned /sys/fs/bpf/tc/globals/stats_map
 *    `Found 10 elements`
 * 4. Check if program has been attached
 *    tc filter show dev <dev_name> ingress
 * 5. Print the debug messages from the bpf_trace_printk function in this xdp program
 *    sudo cat /sys/kernel/debug/tracing/trace_pipe
 * 6. Send traffic to the interface (can use any tool to do so)
 * 7. Detach the program
 *    sudo tc filter del dev <dev_name> ingress
 * 8. Delete the program and the map
 *    rm /sys/fs/bpf/tc/globals/egress_ifindex && rm /sys/fs/bpf/tc/globals/stats_map
 */
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/if_vlan.h>
#include <linux/ip.h>
#include <linux/in.h>
#include <linux/tcp.h>
#include <linux/udp.h>

#include <linux/pkt_cls.h>

#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>

/* This is the data record stored in the map */
struct datarec {
	__u64 rx_packets;
	__u64 rx_bytes;
};

#define TC_ACTION_MAX 10

struct {
__uint(type, BPF_MAP_TYPE_PERCPU_ARRAY);
__uint(max_entries, TC_ACTION_MAX);
__type(key, int);
__type(value, struct datarec);
__uint(pinning, LIBBPF_PIN_BY_NAME);
} stats_map SEC(".maps");

int record_stats(struct __sk_buff *skb, int action)
{
    void *data = (void *)(long)skb->data_end;
    void *data_end = (void *)(long)skb->data_end;
    if (action >= TC_ACTION_MAX)
		return TC_ACT_SHOT;

	/* Lookup in kernel BPF-side return pointer to actual data record */
	struct datarec *rec = bpf_map_lookup_elem(&stats_map, &action);
	if (!rec)
		return TC_ACT_SHOT;

	/* BPF_MAP_TYPE_PERCPU_ARRAY returns a data record specific to current
	 * CPU and XDP hooks runs under Softirq, which makes it safe to update
	 * without atomic operations.
	 */
	rec->rx_packets++;
	rec->rx_bytes += (skb->data_end - skb->data);

	
    return action;
}

SEC("ingress_drop")
int _ingress_drop(struct __sk_buff *skb)
{
	void *data     = (void *)(long)skb->data;
	void *data_end = (void *)(long)skb->data_end;
	struct ethhdr *eth = data;
    int action = TC_ACT_SHOT;

	if (data + sizeof(*eth) > data_end) {
        action = TC_ACT_OK;
        goto out;
    }

	/* Keep ARP resolution working */
	if (eth->h_proto == bpf_htons(ETH_P_ARP)) {
		action = TC_ACT_OK;
        goto out;
    }

out:
    return record_stats(skb, action);
}

char _license[] SEC("license") = "GPL";