/* clang -O2 -emit-llvm -c tc_echo.c -o - | llc -march=bpf -filetype=obj -o tc_echo.o */
/* clang -g -O2 -Wall -target bpf -I ~/iproute2/include/ -c tc_echo.c -o tc_echo.o */
#include <linux/if_ether.h>
#include <linux/pkt_cls.h>
#include <linux/ip.h>
#include <linux/ipv6.h>
#include <linux/in.h>
#include <linux/tcp.h>
#include <linux/udp.h>

int echo(struct __sk_buff *skb) {
    void *data = (void*)(long)skb->data;
    void *data_end = (void*)(long)skb->data_end;
    struct ethhdr *eth = data;
    if (unlikely((void*)(eth + 1) > data_end))
        return TC_ACT_SHOT;
    if (unlikely(eth->h_proto != htons(ETH_P_IP) && eth->h_proto != htons(ETH_P_IPV6)))
        return TC_ACT_OK;
    struct iphdr *ip = (void*)(eth + 1);
    struct ipv6hdr *ip6 = (void*)(eth + 1);
    void *ip_payload;
    u8 l4_proto;
    u16 len = 0;
    if (eth->h_proto == htons(ETH_P_IP)) {
#ifdef ENABLE_IPV4
        if (unlikely((void*)(ip + 1) > data_end))
            return TC_ACT_SHOT;
        if (ip->daddr != IPV4_DEST)
            return TC_ACT_OK;
        l4_proto = ip->protocol;
        ip_payload = (void*)(ip + 1);
#else
        return TC_ACT_OK;
#endif
    } else {
#ifdef ENABLE_IPV6
        if (unlikely((void*)(ip6 + 1) > data_end))
            return TC_ACT_SHOT;
        u64 *ipdest = (void*)&ip6->daddr;
        if (ipdest[0] != IPV6_DEST_HIGH || ipdest[1] != IPV6_DEST_LOW)
            return TC_ACT_OK;
        l4_proto = ip6->nexthdr;
        ip_payload = (void*)(ip6 + 1);
#else
        return TC_ACT_OK;
#endif
    }
    if (unlikely(l4_proto != IPPROTO_TCP && l4_proto != IPPROTO_UDP))
        return TC_ACT_OK;
    u16 *sport = ip_payload;
    if (unlikely((void*)(sport + 1) > data_end))
        return TC_ACT_SHOT;
    u16 *dport = (void*)(sport + 1);
    if (unlikely((void*)(dport + 1) > data_end))
        return TC_ACT_SHOT;
    if (*dport != DPORT)
        return TC_ACT_OK;
    if (l4_proto == IPPROTO_TCP) {
        struct tcphdr *tcp = ip_payload;
        if (unlikely((void*)(tcp + 1) > data_end))
            return TC_ACT_SHOT;
        if (tcp->syn || tcp->fin || tcp->rst)
            return TC_ACT_OK;
        u32 tmp_seq = tcp->seq;
        tcp->seq = tcp->ack_seq;
        tcp->ack_seq = tmp_seq;
    }
    u8 tmp_mac[ETH_ALEN];
    memcpy(tmp_mac, eth->h_dest, ETH_ALEN);
    memcpy(eth->h_dest, eth->h_source, ETH_ALEN);
    memcpy(eth->h_source, tmp_mac, ETH_ALEN);
    if (eth->h_proto == htons(ETH_P_IP)) {
        u32 tmp_ip = ip->saddr;
        ip->saddr = ip->daddr;
        ip->daddr = tmp_ip;
    } else {
        u64 tmp_ip;
        u64 *ipsrc = (void*)&ip6->saddr, *ipdest = (void*)&ip6->daddr;
        tmp_ip = ipsrc[0];
        ipsrc[0] = ipdest[0];
        ipdest[0] = tmp_ip;
        tmp_ip = ipsrc[1];
        ipsrc[1] = ipdest[1];
        ipdest[1] = tmp_ip;
    }
    u16 tmp_port = *sport;
    *sport = *dport;
    *dport = tmp_port;
    return TC_ACT_OK;
}