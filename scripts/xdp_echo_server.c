/*  TC (Traffic Control) eBPF echo server
 *
 * 1. Compile with clang bpf
 *    clang -O2 -target bpf -g -c tc_echo_server.c -o tc_echo_server.o
 *    `The -g flag is important. clang to generate debug info (including .BTF ELF section) needed for loading the btf maps`
 * 2. Load program using bpftool
 *    sudo tc filter add dev <dev_name> ingress bpf da obj tc_echo_server.o sec ingress_redirect
 * 3. Check if the map has been pinned
 *    sudo bpftool map dump pinned /sys/fs/bpf/tc/globals/egress_ifindex
 *    `Found 1 elements`
 *    sudo bpftool map dump pinned /sys/fs/bpf/tc/globals/stats_map
 *    `Found 10 elements`
 * 4. Insert values into map
 *    bpftool map update pinned /sys/fs/bpf/maps/egress_ifindex key hex FF FF FF FF FF FF FF FF value hex 11 11 11 11 11 11 11 11
 * 5. Check if program has been attached
 *    tc filter show dev <dev_name> ingress
 * 6. Print the debug messages from the bpf_trace_printk function in this xdp program
 *    sudo cat /sys/kernel/debug/tracing/trace_pipe
 * 7. Send traffic to the interface (can use any tool to do so)
 * 8. Detach the program
 *    sudo tc filter del dev <dev_name> ingress
 * 9. Delete the program and the map
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

struct datarec
{
        __u64 rx_packets;
        __u64 rx_bytes;
};

#define TC_ACTION_MAX 10

struct
{
        __uint(type, BPF_MAP_TYPE_ARRAY);
        __uint(max_entries, 1);
        __type(key, int);
        __type(value, int);
        __uint(pinning, LIBBPF_PIN_BY_NAME);
} egress_ifindex SEC(".maps");

struct
{
        __uint(type, BPF_MAP_TYPE_PERCPU_ARRAY);
        __uint(max_entries, TC_ACTION_MAX);
        __type(key, int);
        __type(value, struct datarec);
        __uint(pinning, LIBBPF_PIN_BY_NAME);
} stats_map SEC(".maps");

/*
 * Swaps destination and source MAC addresses inside an Ethernet header
 */
static void swap_src_dst_mac(struct ethhdr *eth)
{
        __u8 h_tmp[ETH_ALEN];

        __builtin_memcpy(h_tmp, eth->h_source, ETH_ALEN);
        __builtin_memcpy(eth->h_source, eth->h_dest, ETH_ALEN);
        __builtin_memcpy(eth->h_dest, h_tmp, ETH_ALEN);
}

/*
 * Swaps destination and source IPv4 addresses inside an IPv4 header
 */
static void swap_src_dst_ipv4(struct iphdr *iphdr)
{
        __be32 tmp = iphdr->saddr;

        iphdr->saddr = iphdr->daddr;
        iphdr->daddr = tmp;
}

int process_packet(struct __sk_buff *skb)
{
        void *data_end = (void *)(long)skb->data_end;
        struct ethhdr *eth = (void *)(long)skb->data;
        if (eth + 1 > data_end)
                return TC_ACT_SHOT;

        swap_src_dst_mac(eth);

        struct iphdr *ip = (struct iphdr *)(skb->data + sizeof(struct ethhdr));
        if (ip + 1 > data_end)
                return TC_ACT_SHOT;

        swap_src_dst_ipv4(ip);

        return 0;
}

int record_stats(struct __sk_buff *skb, int action)
{
        void *data_end = (void *)(long)skb->data_end;
        if (action >= TC_ACTION_MAX)
                return TC_ACT_SHOT;

        /* Lookup in kernel BPF-side return pointer to actual data record */
        struct datarec *rec = bpf_map_lookup_elem(&stats_map, &action);
        if (!rec)
                return TC_ACT_SHOT;

        rec->rx_packets++;
        rec->rx_bytes += (skb->data_end - skb->data);

        return action;
}

SEC("ingress_redirect")
int _ingress_redirect(struct __sk_buff *skb)
{
        void *data = (void *)(long)skb->data;
        void *data_end = (void *)(long)skb->data_end;
        struct ethhdr *eth = data;
        int key = 0, ifindex = 4; /* Put values here: `sudo cat /sys/class/net/<iface>/ifindex` to get the ifindex */
        int action = TC_ACT_OK;

        if (data + sizeof(*eth) > data_end)
        {
                action = TC_ACT_OK;
                goto out;
        }

        /* Keep ARP resolution working */
        if (eth->h_proto == bpf_htons(ETH_P_ARP))
        {
                action = TC_ACT_OK;
                goto out;
        }

        process_packet(skb);

        action = bpf_redirect(ifindex, 0); // __bpf_tx_skb / __dev_xmit_skb

out:
        return record_stats(skb, action);
}

char _license[] SEC("license") = "GPL";