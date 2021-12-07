/*
	Packet drop server using libpcap library
    gcc libpcap_drop_server.c -lpcap -o libpcap_drop_server
*/
#include <pcap.h>
#include <stdio.h>
#include <stdlib.h> // for exit()
#include <string.h> //for memset

#include <sys/socket.h>
#include <arpa/inet.h> // for inet_ntoa()
#include <net/ethernet.h>
#include <netinet/ip_icmp.h>	//Provides declarations for icmp header
#include <netinet/udp.h>	//Provides declarations for udp header
#include <netinet/tcp.h>	//Provides declarations for tcp header
#include <netinet/ip.h>	//Provides declarations for ip header
#include <net/if.h>

void drop_packet(u_char *, const struct pcap_pkthdr *, const u_char *);

int tcp=0,udp=0,icmp=0,others=0,igmp=0,total=0;	

int main(int argc, char **argv)
{
	pcap_if_t *alldevsp , *device;
	pcap_t *handle; //Handle of the device that shall be sniffed

	char errbuf[100] , *devname , devs[100][100];
	int err = 0;
	unsigned char *buffer = (unsigned char *)malloc(65536);
	memset(buffer, 0, 65536);

	/* 
	 * check command line arguments 
	 */
	if (argc != 2)
	{
		printf("usage: %s <receive interface>\n", argv[0]);
		exit(1);
	}
	
	struct ifreq ifr_rcv;
	
	memset(&ifr_rcv, 0, sizeof(ifr_rcv));

	snprintf(ifr_rcv.ifr_name, sizeof(ifr_rcv.ifr_name), argv[1]);

	//Open the device for sniffing
	printf("Opening device %s for sniffing ... " , ifr_rcv.ifr_name);
	handle = pcap_open_live(ifr_rcv.ifr_name , 65536 , 1 , 0 , errbuf);
	
	if (handle == NULL) 
	{
		printf("Couldn't open device %s : %s\n" , ifr_rcv.ifr_name, errbuf);
		exit(1);
	}
	printf("Done\n");

	
	//Put the device in sniff loop
	pcap_loop(handle , -1 , drop_packet , NULL);
	
	return 0;	
}

void drop_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *buffer)
{
	int size = header->len;
	
	//Get the IP Header part of this packet , excluding the ethernet header
	struct iphdr *iph = (struct iphdr*)(buffer + sizeof(struct ethhdr));
	++total;
	switch (iph->protocol) //Check the Protocol and do accordingly...
	{
		case 1:  //ICMP Protocol
			++icmp;
			break;
		
		case 2:  //IGMP Protocol
			++igmp;
			break;
		
		case 6:  //TCP Protocol
			++tcp;
			break;
		
		case 17: //UDP Protocol
			++udp;
			break;
		
		default: //Some Other Protocol like ARP etc.
			++others;
			break;
	}
	printf("TCP : %d   UDP : %d   ICMP : %d   IGMP : %d   Others : %d   Total : %d\r", tcp , udp , icmp , igmp , others , total);
}