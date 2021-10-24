package.path = package.path ..";?.lua;test/?.lua;app/?.lua;"

require "Pktgen";

local port = "0";
local send_for_secs = 5;
local packet_size = 64;
local rate = 20;

local mac_dst = "00:22:48:65:67:26";

local ip_dst = "10.0.0.5";
local ip_src = "10.0.0.7";

local dport = 3333;
local sport = 12;

-- Opens a file in append mode
file = io.open("/home/open/test.lua", "a")

-- sets the default output file as test.lua
io.output(file)


pktgen.set(port, "size", packet_size);

pktgen.set_mac(port, "dst", mac_dst);

pktgen.set_ipaddr(port, "dst", ip_dst);
pktgen.set_ipaddr(port, "src", ip_src);

pktgen.set(port, "dport", 3333);

pktgen.set_proto(port, "udp");

while rate < 100 do
    pktgen.set(port, "rate", rate);
    pktgen.start(port);
    local start_time = os.time();

    while os.difftime(os.time(), start_time) < send_for_secs do
        sleep(1);
    end

    pktgen.stop(port);
    stats = pktgen.portStats("all", "port");
    portRates = pktgen.portStats("all", "rate");
    printf("\n[0] opackets : %d, obytes : %d, oerrors : %d, pkts_tx : %d, mbits_tx : %d, rate : %d\n", stats[0]["opackets"], stats[0]["obytes"], stats[0]["oerrors"], portRates[0]["pkts_tx"], portRates[0]["mbits_tx"], rate);
    printf("\n[1] ipackets : %d, ibytes : %d, ierrors : %d, pkts_rx : %d, mbits_rx : %d, rate : %d\n", stats[0]["ipackets"], stats[0]["ibytes"], stats[0]["ierrors"], portRates[0]["pkts_rx"], portRates[0]["mbits_rx"], rate);
    print("\nEnd "..os.time());
    rate = rate + 20;
end

printf("\nDone");
pktgen.quit();