package.path = package.path ..";?.lua;test/?.lua;app/?.lua;"

require "Pktgen";

local port = "0";
local send_for_secs = 10;
local packet_size = 64;
local rate = 20;

local mac_dst = "b8:ce:f6:57:8f:18";

local ip_dst = "10.0.0.2";
local ip_src = "10.0.0.1";

local dport = 5001;
local sport = 12;

pktgen.set(port, "size", packet_size);

pktgen.set_mac(port, "dst", mac_dst);

pktgen.set_ipaddr(port, "dst", ip_dst);
pktgen.set_ipaddr(port, "src", ip_src);

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
    printf("\n[0] opackets : %d, obytes : %d, oerrors : %d, pkts_tx : %d, mbits_tx : %d\n", stats[0]["opackets"], stats[0]["obytes"], stats[0]["oerrors"], portRates[0]["pkts_tx"], portRates[0]["mbits_tx"]);
    printf("\n[1] ipackets : %d, ibytes : %d, ierrors : %d, pkts_rx : %d, mbits_rx : %d\n", stats[0]["ipackets"], stats[0]["ibytes"], stats[0]["ierrors"], portRates[0]["pkts_rx"], portRates[0]["mbits_rx"]);
    printf("\nFinished for rate %d", rate);
    rate = rate + 20;
end

printf("\nDone");