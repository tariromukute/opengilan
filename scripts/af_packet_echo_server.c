/* Note: run this program as root user
 * https://man7.org/linux/man-pages/man7/packet.7.html
 * Author: Tariro Mukute 
 * gcc af_packet_echo_server.c -g -o af_packet_echo_server (two interfaces)
 */
#include <stdio.h>
#include <malloc.h>
#include <string.h>
#include <signal.h>
#include <stdbool.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/ioctl.h>

#include <linux/if_packet.h>
#include <netinet/in.h>
#include <netinet/if_ether.h> // for ethernet header
#include <netinet/ip.h>		  // for ip header
#include <netinet/ip6.h>
#include <netinet/udp.h> // for udp header
#include <netinet/tcp.h>
#include <arpa/inet.h> // to avoid warning at inet_ntoa
#include <unistd.h>

#include <sys/ioctl.h>
#include <net/if.h>

int total, tcp, udp, icmp, igmp, other, iphdrlen;

struct sockaddr saddr;
struct sockaddr_in source, dest;

/*
 * Swaps destination and source MAC addresses inside an Ethernet header
 */
static void swap_src_dst_mac(struct ethhdr *eth)
{
	__u8 h_tmp[ETH_ALEN];

	memcpy(h_tmp, eth->h_source, ETH_ALEN);
	memcpy(eth->h_source, eth->h_dest, ETH_ALEN);
	memcpy(eth->h_dest, h_tmp, ETH_ALEN);
}

/*
 * Swaps destination and source IPv6 addresses inside an IPv6 header
 */
static void swap_src_dst_ipv6(struct ip6_hdr *ipv6)
{
	struct in6_addr tmp = ipv6->ip6_src;

	ipv6->ip6_src = ipv6->ip6_dst;
	ipv6->ip6_dst = tmp;
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

void ethernet_header(unsigned char *buffer, int buflen)
{
	struct ethhdr *eth = (struct ethhdr *)(buffer);

	// Do work

	swap_src_dst_mac(eth);
}

void ip_header(unsigned char *buffer, int buflen)
{
	struct iphdr *iph = (struct iphdr *)(buffer + sizeof(struct ethhdr));

	// iphdrlen = iph->ihl * 4;

	// Do work on ip header

	swap_src_dst_ipv4(iph);
}

void payload(unsigned char *buffer, int buflen)
{
	// Do work on payload
}

void tcp_header(unsigned char *buffer, int buflen)
{
	ethernet_header(buffer, buflen);
	ip_header(buffer, buflen);

	struct tcphdr *tcp = (struct tcphdr *)(buffer + iphdrlen + sizeof(struct ethhdr));

	// Do work

	payload(buffer, buflen);
}

void udp_header(unsigned char *buffer, int buflen)
{
	ethernet_header(buffer, buflen);
	ip_header(buffer, buflen);

	struct udphdr *udp = (struct udphdr *)(buffer + iphdrlen + sizeof(struct ethhdr));

	// Do work

	payload(buffer, buflen);
}

void data_process(unsigned char *buffer, int buflen)
{
	struct iphdr *ip = (struct iphdr *)(buffer + sizeof(struct ethhdr));
	++total;
	/* we will se UDP Protocol only*/
	switch (ip->protocol) //see /etc/protocols file
	{

	case 6:
		++tcp;
		tcp_header(buffer, buflen);
		break;

	case 17:
		++udp;
		udp_header(buffer, buflen);
		break;

	default:
		++other;
	}
	printf("TCP: %d  UDP: %d  Other: %d  Total: %d  \r", tcp, udp, other, total);
}

void set_ifindex(int sock_s, struct ifreq *ifr)
{
	if ((ioctl(sock_s, SIOCGIFINDEX, ifr)) < 0)
		printf("error in index ioctl reading if name %s", ifr->ifr_name);

	printf("index=%d\n", ifr->ifr_ifindex);
}

int echo_packet(int sock_r, unsigned char *buffer, int buflen, int offset, struct ifreq ifreq_i, struct sockaddr_ll *sadr_ll)
{
	struct ethhdr *eth = (void *)buffer;
	
	return sendto(sock_r, buffer, buflen, offset, (const struct sockaddr *)sadr_ll, sizeof(struct sockaddr_ll));
}

int create_sock(struct sockaddr_ll *sadr_ll)
{
	int fd, rc;

	fd = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
	if (fd < 0)
	{
		printf("error in socket\n");
		return -1;
	}

	
	return fd;
}

int bind_sock(int sockfd, struct ifreq ifr, struct sockaddr_ll *sadr_ll)
{
	int err = 0;
	sadr_ll->sll_ifindex = ifr.ifr_ifindex;
	sadr_ll->sll_halen   = ETH_ALEN;
	sadr_ll->sll_family = AF_PACKET;
	sadr_ll->sll_protocol = htons(ETH_P_ALL);
	err = bind(sockfd, (const struct sockaddr *) sadr_ll, (socklen_t) sizeof(struct sockaddr_ll));
	if (err < 0) {
		printf("\nFailed to bind socket %s errno %d", ifr.ifr_name, err);
	}

	return err;
}

int main(int argc, char **argv)
{
	int err = 0;
	int sock_r, sock_s, buflen, saddr_len;
	unsigned char *buffer = (unsigned char *)malloc(65536);
	memset(buffer, 0, 65536);

	/* 
	 * check command line arguments 
	 */
	if (argc != 3)
	{
		fprintf(stderr, "usage: %s <receive interface> <send interface>\n", argv[0]);
		err = -1;
		goto out;
	}

	struct ifreq ifr_rcv, ifr_send;
	struct sockaddr_ll sadr_ll_rcv, sadr_ll_send;
	
	memset(&ifr_rcv, 0, sizeof(ifr_rcv));
	memset(&ifr_send, 0, sizeof(ifr_send));

	// Set the interface name
	snprintf(ifr_rcv.ifr_name, sizeof(ifr_rcv.ifr_name), argv[1]);
	snprintf(ifr_send.ifr_name, sizeof(ifr_send.ifr_name), argv[2]);

	// create AF_PACKET socket to receive traffic from
	sock_r = create_sock(&sadr_ll_rcv);
	if (sock_r < 0)
	{
		printf("\nFailed to create receive socket");
		err = -1;
		goto out;
	}

	sock_s = create_sock(&sadr_ll_send);
	if (sock_s < 0)
	{
		printf("\nFailedto create send socket");
		err = -1;
		goto out;
	}

	set_ifindex(sock_s, &ifr_send);
	set_ifindex(sock_r, &ifr_rcv);

	// create AF_PACKET socket to receive traffic from
	err = bind_sock(sock_r, ifr_rcv, &sadr_ll_rcv);
	if (err < 0)
	{
		printf("\nFailed to create receive socket");
		goto out;
	}

	err = bind_sock(sock_s, ifr_send, &sadr_ll_send);
	if (err < 0)
	{
		printf("\nFailedto create send socket");
		goto out;
	}

	printf("starting .... \n");
	socklen_t sock_siz = sizeof(struct sockaddr_ll);
	while (1)
	{
		saddr_len = sizeof saddr;
		buflen = recvfrom(sock_r, buffer, 65536, 0, (struct sockaddr *) &sadr_ll_rcv, &sock_siz);

		if (buflen < 0)
		{
			printf("error in reading recvfrom function\n");
			err = -1;
			goto out;
		}
		data_process(buffer,buflen);
		echo_packet(sock_s, buffer, buflen, 0, ifr_send, &sadr_ll_send);
	}
out:

	close(sock_r); // use signals to close socket
	printf("DONE!!!!\n");
}