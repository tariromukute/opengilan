/*
	Packet sniffer using libpcap library
    gcc libpcap_echo_server.c -lpcap -o libpcap_echo_server
	https://www.devdungeon.com/content/using-libpcap-c
*/
#include <pcap.h>
#include <stdio.h>
#include <stdlib.h> // for exit()
#include <string.h> //for memset

#include <sys/socket.h>
#include <net/ethernet.h>
#include <netinet/ip_icmp.h>	//Provides declarations for icmp header
#include <netinet/udp.h>	//Provides declarations for udp header
#include <netinet/tcp.h>	//Provides declarations for tcp header
#include <netinet/ip.h>	//Provides declarations for ip header
#include <net/if.h>

void process_packet(const struct pcap_pkthdr *, const u_char *);
void handle_ip_packet(const u_char * , int);
void handle_ip_packet(const u_char * , int);
void handle_tcp_packet(const u_char *  , int );
void handle_udp_packet(const u_char * , int);
void handle_icmp_packet(const u_char * , int );

int tcp=0,udp=0,icmp=0,others=0,igmp=0,total=0,i,j;	

int main(int argc, char **argv)
{
	pcap_t *rcv_handle, *send_handle; //Handle of the device that shall be sniffed

	char errbuf[100];
	int err = 0;
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
	
	memset(&ifr_rcv, 0, sizeof(ifr_rcv));
	memset(&ifr_send, 0, sizeof(ifr_send));

	// Set the interface name
	snprintf(ifr_rcv.ifr_name, sizeof(ifr_rcv.ifr_name), argv[1]);
	snprintf(ifr_send.ifr_name, sizeof(ifr_send.ifr_name), argv[2]);
	
	//Open the device for sniffing
	printf("Opening receive device  %s for sniffing ... " , ifr_rcv.ifr_name);
	rcv_handle = pcap_open_live(ifr_rcv.ifr_name , 65536 , 1 , 0 , errbuf);
	if (rcv_handle == NULL) 
	{
		fprintf(stderr, "Couldn't open device %s : %s\n" , ifr_rcv.ifr_name , errbuf);
		exit(1);
	}

	printf("Opening receive device  %s for sniffing ... " , ifr_send.ifr_name);
	send_handle = pcap_open_live(ifr_send.ifr_name , 65536 , 1 , 0 , errbuf);
	if (send_handle == NULL) 
	{
		fprintf(stderr, "Couldn't open device %s : %s\n" , ifr_send.ifr_name , errbuf);
		exit(1);
	}
	printf("Done\n");
	
	const u_char *packet;
	struct pcap_pkthdr packet_header;
	while (1)
	{
		do {
			packet = pcap_next(rcv_handle, &packet_header);
		} while(!packet);

		process_packet(&packet_header, packet);
		pcap_inject(send_handle, (const void *) packet, packet_header.len);
	}
out:
	
	return 0;	
}

void process_packet(const struct pcap_pkthdr *header, const u_char *buffer)
{
	int size = header->len;
	
	//Get the IP Header part of this packet , excluding the ethernet header
	struct iphdr *iph = (struct iphdr*)(buffer + sizeof(struct ethhdr));
	++total;
	switch (iph->protocol) //Check the Protocol and do accordingly...
	{
		case 1:  //ICMP Protocol
			++icmp;
			handle_icmp_packet( buffer , size);
			break;
		
		case 2:  //IGMP Protocol
			++igmp;
			break;
		
		case 6:  //TCP Protocol
			++tcp;
			handle_tcp_packet(buffer , size);
			break;
		
		case 17: //UDP Protocol
			++udp;
			handle_udp_packet(buffer , size);
			break;
		
		default: //Some Other Protocol like ARP etc.
			++others;
			break;
	}
	printf("TCP : %d   UDP : %d   ICMP : %d   IGMP : %d   Others : %d   Total : %d\r", tcp , udp , icmp , igmp , others , total);
}

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
 * Swaps destination and source IPv4 addresses inside an IPv4 header
 */
static void swap_src_dst_ipv4(struct iphdr *iphdr)
{
	__be32 tmp = iphdr->saddr;

	iphdr->saddr = iphdr->daddr;
	iphdr->daddr = tmp;
}

void handle_ethernet_header(const u_char *buffer, int Size)
{
	struct ethhdr *eth = (struct ethhdr *)(buffer);

	// Do work

	swap_src_dst_mac(eth);
}

void handle_ip_header(const u_char * buffer, int Size)
{
	handle_ethernet_header(buffer , Size);
		
	struct iphdr *iph = (struct iphdr *)(buffer  + sizeof(struct ethhdr) );
	
	// Do work on ip header

	swap_src_dst_ipv4(iph);
}

void handle_tcp_packet(const u_char * buffer, int size)
{
	// unsigned short iphdrlen;
	
	// struct iphdr *iph = (struct iphdr *)( buffer  + sizeof(struct ethhdr) );
	// iphdrlen = iph->ihl*4;
	
	// struct tcphdr *tcph=(struct tcphdr*)(buffer + iphdrlen + sizeof(struct ethhdr));
			
	// int header_size =  sizeof(struct ethhdr) + iphdrlen + tcph->doff*4;
	
	// Do work
		
	handle_ip_header(buffer, size);
		
}

void handle_udp_packet(const u_char *buffer , int size)
{
	
	// unsigned short iphdrlen;
	
	// struct iphdr *iph = (struct iphdr *)(buffer +  sizeof(struct ethhdr));
	// iphdrlen = iph->ihl*4;
	
	// struct udphdr *udph = (struct udphdr*)(buffer + iphdrlen  + sizeof(struct ethhdr));
	
	// int header_size =  sizeof(struct ethhdr) + iphdrlen + sizeof udph;
	
	// Do work

	handle_ip_header(buffer, size);			
	
}

void handle_icmp_packet(const u_char * buffer , int Size)
{
	// unsigned short iphdrlen;
	
	// struct iphdr *iph = (struct iphdr *)(buffer  + sizeof(struct ethhdr));
	// iphdrlen = iph->ihl * 4;
	
	// struct icmphdr *icmph = (struct icmphdr *)(buffer + iphdrlen  + sizeof(struct ethhdr));
	
	// int header_size =  sizeof(struct ethhdr) + iphdrlen + sizeof icmph;
	
	// Do work

	handle_ip_header(buffer , Size);
		
}