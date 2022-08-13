# The file documents the step to testing Free5gc

The initial step is to manually set up and configure the Free5gc and run the different test from the webiste. Used [UERANSIM - a UE/RAN Simulator](https://www.free5gc.org/installations/stage-3-sim-install/) for testing the Free5gc. Executed the following steps:

- [x] Deployed two virtual machines (VM-ueransim and VM-free5gc) on Azure in a Vnet with the following address space `192.168.0.0/16` as per the [installation guide](https://www.free5gc.org/installations/stage-3-sim-install/). VM-free5gc with static ip address `192.168.56.101` and VM-ueransim with static ip address `192.168.56.102`. See [link](https://docs.microsoft.com/en-us/azure/virtual-network/ip-services/virtual-networks-static-private-ip-arm-pportal) on how to assign static ip address.
- [x] Deploy a virtual machine with at least the minimum requirements as describe on the [repo](https://github.com/free5gc/free5gc/wiki/Environment#recommended-environment)
- [x] Install Free5gc according to the [installation guide](https://github.com/free5gc/free5gc/wiki/Installation)
- [x] Install UERANSIM according to the [installation guide](https://www.free5gc.org/installations/stage-3-sim-install/)
- [x] Install the Webconsole on free5gc and add a test subscriber (keep default, only change “Operator Code Type” field, select “OP”)
- [x] Update the Free5gc configuration files a per [guide](https://www.free5gc.org/installations/stage-3-sim-install/)
- [x] Run the Free5gc as describe in the [guide](https://github.com/free5gc/free5gc/wiki/Run), skipped the stage of running the N3IWF. Also see the [ueransim guide](https://www.free5gc.org/installations/stage-3-sim-install/)
- [x] Run UERANSIM see [guide](https://www.free5gc.org/installations/stage-3-sim-install/)
- [x] Capture the packets during successful ping using the tunnel `ping -I uesimtun0 google.com`. The setup using GTP protocol with UDP so capture the UDP packets on the main interface with `sudo tcpdump -i eth0 proto UDP`. To create a pcap file for analysing later `sudo tcpdump -i eth0 proto UDP -A -w udp_gtp.pcap`. To dump the contents of the pcap file `tcpdump -ttttnnr pcap/udp_gtp.pcap`.
- [x] Download the file to use with packet generator `scp azureuser@<ip_addpress>:/home/azureuser/udp_gtp.pcap free5gc/ -i <key>.pem`
- [x] Try the above steps using the IP address and ranges created by the OpenGiLAN - first time this didn't work. I then set up the OpenGiLAN and then deployed a new VM, VM-euransim. I changed the management interface to the IP from above `192.168.56.101` and `192.168.56.102` respectively. I ran the UERANSIM test and it worked. I went on to change the IP address of VM-euransim to the range of the testbed `10.0.2.0/24`. Changed the free5gc config on VM-sut to eth1's ip adddress `10.0.2.5` and updated the config for ueransim on VM-ueransim respectively and it worked.
- [x] Deploy a TREX and send traffic to VM-free5gc
- [x] Push the pcap file to VM-Trex `scp free5gc/udp_gtp.pcap azureuser@<ip_addpress>:/home/azureuser/udp_gtp.pcap -i <key>.pem`
- [x] Send the traffic using Trex `python3 tgn/stl_pcap_dns_push.py -t 3 -f /home/azureuser/udp_gtp.pcap -s 10.0.2.4 -d 10.0.2.5 -r 10`
- [x] Deploy the OpenGiLAN-bench and manually set up the Free5gc as above and start the tests [comment: couldn't complete this steps because the signally needs to be stateful. A stateless traffic generation using the pcap file didn't work]
- [ ] Deploy UERANSIM and run it for more than one EU (two for starters) - determine the maximum number of EUs that can be set up. For details on how to set up multiple EUs see [link](https://github.com/aligungr/UERANSIM/wiki/Usage)
- [ ] Update the ansible script with a role that instals and sets up EURANSIM
- [ ] Run Trex GTP-U for EUs that would have been registered using EURANSIM
- [ ] Update ansible script to run the above in sequencial order and increase the number of EU

## Add subscribers to Free5gc


```python
import http.client
import json

imsi="imsi-208930000000012"
base_url = "olan138sut.westeurope.cloudapp.azure.com:5000"

conn = http.client.HTTPConnection(base_url)


payload = {
    "plmnID": "20893",
    "ueId": imsi,
    "AuthenticationSubscription": {
        "authenticationManagementField": "8000",
        "authenticationMethod": "5G_AKA",
        "milenage": {"op": {
                "encryptionAlgorithm": 0,
                "encryptionKey": 0,
                "opValue": "8e27b6af0e692e750f32667a3b14605d"
            }},
        "opc": {
            "encryptionAlgorithm": 0,
            "encryptionKey": 0,
            "opcValue": ""
        },
        "permanentKey": {
            "encryptionAlgorithm": 0,
            "encryptionKey": 0,
            "permanentKeyValue": "8baf473f2f8fd09487cccbd7097c6862"
        },
        "sequenceNumber": "16f3b3f70fc2"
    },
    "AccessAndMobilitySubscriptionData": {
        "gpsis": ["msisdn-0900000000"],
        "nssai": {
            "defaultSingleNssais": [
                {
                    "sst": 1,
                    "sd": "010203",
                    "isDefault": True
                },
                {
                    "sst": 1,
                    "sd": "112233",
                    "isDefault": True
                }
            ],
            "singleNssais": []
        },
        "subscribedUeAmbr": {
            "downlink": "2 Gbps",
            "uplink": "1 Gbps"
        }
    },
    "SessionManagementSubscriptionData": [
        {
            "singleNssai": {
                "sst": 1,
                "sd": "010203"
            },
            "dnnConfigurations": {
                "internet": {
                    "sscModes": {
                        "defaultSscMode": "SSC_MODE_1",
                        "allowedSscModes": ["SSC_MODE_2", "SSC_MODE_3"]
                    },
                    "pduSessionTypes": {
                        "defaultSessionType": "IPV4",
                        "allowedSessionTypes": ["IPV4"]
                    },
                    "sessionAmbr": {
                        "uplink": "200 Mbps",
                        "downlink": "100 Mbps"
                    },
                    "5gQosProfile": {
                        "5qi": 9,
                        "arp": {"priorityLevel": 8},
                        "priorityLevel": 8
                    }
                },
                "internet2": {
                    "sscModes": {
                        "defaultSscMode": "SSC_MODE_1",
                        "allowedSscModes": ["SSC_MODE_2", "SSC_MODE_3"]
                    },
                    "pduSessionTypes": {
                        "defaultSessionType": "IPV4",
                        "allowedSessionTypes": ["IPV4"]
                    },
                    "sessionAmbr": {
                        "uplink": "200 Mbps",
                        "downlink": "100 Mbps"
                    },
                    "5gQosProfile": {
                        "5qi": 9,
                        "arp": {"priorityLevel": 8},
                        "priorityLevel": 8
                    }
                }
            }
        },
        {
            "singleNssai": {
                "sst": 1,
                "sd": "112233"
            },
            "dnnConfigurations": {
                "internet": {
                    "sscModes": {
                        "defaultSscMode": "SSC_MODE_1",
                        "allowedSscModes": ["SSC_MODE_2", "SSC_MODE_3"]
                    },
                    "pduSessionTypes": {
                        "defaultSessionType": "IPV4",
                        "allowedSessionTypes": ["IPV4"]
                    },
                    "sessionAmbr": {
                        "uplink": "200 Mbps",
                        "downlink": "100 Mbps"
                    },
                    "5gQosProfile": {
                        "5qi": 9,
                        "arp": {"priorityLevel": 8},
                        "priorityLevel": 8
                    }
                },
                "internet2": {
                    "sscModes": {
                        "defaultSscMode": "SSC_MODE_1",
                        "allowedSscModes": ["SSC_MODE_2", "SSC_MODE_3"]
                    },
                    "pduSessionTypes": {
                        "defaultSessionType": "IPV4",
                        "allowedSessionTypes": ["IPV4"]
                    },
                    "sessionAmbr": {
                        "uplink": "200 Mbps",
                        "downlink": "100 Mbps"
                    },
                    "5gQosProfile": {
                        "5qi": 9,
                        "arp": {"priorityLevel": 8},
                        "priorityLevel": 8
                    }
                }
            }
        }
    ],
    "SmfSelectionSubscriptionData": {"subscribedSnssaiInfos": {
            "01010203": {"dnnInfos": [{"dnn": "internet"}, {"dnn": "internet2"}]},
            "01112233": {"dnnInfos": [{"dnn": "internet"}, {"dnn": "internet2"}]}
        }},
    "AmPolicyData": {"subscCats": ["free5gc"]},
    "SmPolicyData": {"smPolicySnssaiData": {
            "01010203": {
                "snssai": {
                    "sst": 1,
                    "sd": "010203"
                },
                "smPolicyDnnData": {
                    "internet": {"dnn": "internet"},
                    "internet2": {"dnn": "internet2"}
                }
            },
            "01112233": {
                "snssai": {
                    "sst": 1,
                    "sd": "112233"
                },
                "smPolicyDnnData": {
                    "internet": {"dnn": "internet"},
                    "internet2": {"dnn": "internet2"}
                }
            }
        }},
    "FlowRules": []
}

payload = json.dumps(payload)
headers = {
    'Accept': "application/json",
    'Accept-Language': "en-GB,en-US;q=0.9,en;q=0.8",
    'Connection': "keep-alive",
    'Content-Type': "application/json;charset=UTF-8",
    'Token': "admin"
    }

conn.request("POST", "/api/subscriber/{}/20893".format(imsi), payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

## Notes
* Followed the installation guide while running the free5gc on the VM-sut using the default IP assigned by the prototype system `10.0.2.5` for eth1 and the ueransim on a seperate VM-ueransim. The PDU session is estabilished but the ping did not get a response. I then re-did the steps on `Linux Host Network Settings` but applied the rules to both eth0 and eth1 and this time it worked. Not sure if there is a requirement for the `Linux Host Network Settings` to be applied even when the interface is not being used. I will try to reproduce the issue and permutate the different `Linux Host Network Settings` on interfaces and see if that remains true. 
* Tested the above point. Set up the testbed again and ran `sudo iptables -t nat -A POSTROUTING -o <dn_interface> -j MASQUERADE` for all the interfaces during configuration. This time the ueransim manage to send traffic without issues. Will verify if this is a requirement by spinning the testbed again and only running `sudo iptables -t nat -A POSTROUTING -o <dn_interface> -j MASQUERADE` for the eth1 interface and see if it results in the ping not responding.
