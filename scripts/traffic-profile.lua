-- CGCS Demo script
--
package.path = package.path ..";?.lua;test/?.lua;app/?.lua;../?.lua"

require "Pktgen";

-- Opens a file in append mode
file = io.open("/home/open/test.lua", "a")

-- sets the default output file as test.lua
io.output(file)

local time_step = 10;		-- seconds
local pcnt_rate = { 10, 20, 40, 60, 60, 60, 60, 60, 60, 80, 80, 80, 80, 80, 70, 70, 70, 70, 60, 60, 60, 40, 40, 70, 70, 80, 80, 40, 40, 40 };

sendport	= 0;
recvport	= 0;
pkt_size	= 64;
local mac_dst = "00:22:48:65:67:26";
local dstip = "10.0.0.5";
local srcip = "10.0.0.7";
local netmask = "/24";

local dport = 3333;

total_time = 0;

-- Take two lists and create one table with a merged value of the tables.
-- Return a set or table = { { timo, rate }, ... } 
function Set(step, list)
	local	set = { };		-- Must have a empty set first.

	for i,v in ipairs(list) do
		set[i] = { timo = step, rate = v };
	end

	return set;
end 

function main()
	local sending = 0;
	local trlst = Set(time_step, pcnt_rate);

	-- Stop the port sending and reset to 
	pktgen.stop(sendport);
	sleep(2);					-- Wait for stop to happen (not really needed)

	-- Set up the default packet size fixed value for now.
	pktgen.set(sendport, "size", pkt_size);

    pktgen.set_mac(sendport, "dst", mac_dst);

	pktgen.set_ipaddr(sendport, "dst", dstip);
	pktgen.set_ipaddr(sendport, "src", srcip);

	pktgen.set_proto(sendport..","..recvport, "udp");

    pktgen.set(sendport, "dport", dport);

	total_time = 0;
	-- v is the table to values created by the Set(x,y) function
	for _,v in pairs(trlst) do

		printf("   Percent load %d for %d seconds\n", v.rate, v.timo);

		-- Set the rate to the new value
		pktgen.set(sendport, "rate", v.rate);

		-- If not sending packets start sending them
		if ( sending == 0 ) then
			pktgen.start(sendport);
			sending = 1;
		end

        
		-- Sleep until we need to move to the next rate and timeout
		sleep(v.timo);
        stats = pktgen.portStats("all", "port");
        portRates = pktgen.portStats("all", "rate");
        printf("\n[0] opackets : %d, obytes : %d, oerrors : %d, pkts_tx : %d, mbits_tx : %d, load: %d\n", stats[0]["opackets"], stats[0]["obytes"], stats[0]["oerrors"], portRates[0]["pkts_tx"], portRates[0]["mbits_tx"], v.rate);
        printf("\n[1] ipackets : %d, ibytes : %d, ierrors : %d, pkts_rx : %d, mbits_rx : %d, load: %d\n", stats[0]["ipackets"], stats[0]["ibytes"], stats[0]["ierrors"], portRates[0]["pkts_rx"], portRates[0]["mbits_rx"], v.rate);
        pktgen.clr();
		total_time = total_time + v.timo;

	end

	-- Stop the port and do some cleanup
	pktgen.stop(sendport);
	sending = 0;
end

printf("\n**** Traffic Profile Rate for %d byte packets ***\n", pkt_size);
main();
printf("\n*** Traffic Profile Done (Total Time %d) ***\n", total_time);
pktgen.quit();