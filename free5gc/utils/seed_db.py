import http.client
import json
import argparse


def send_subscriber_data(imsi, data):
    headers = {
        'Accept': "application/json",
        'Accept-Language': "en-GB,en-US;q=0.9,en;q=0.8",
        'Connection': "keep-alive",
        'Content-Type': "application/json;charset=UTF-8",
        'Token': "admin"
    }
    conn.request("POST", "/api/subscriber/{}/20893".format(imsi),
                 json.dumps(data), headers)
    response = conn.getresponse()
    print(response.status, response.reason, imsi)
    conn.close()


def subscribe_users(initial_imsi, number_of_users):
    # for loop to create users
    base_imsi = initial_imsi[:-10]
    for i in range(number_of_users):
        imsi = base_imsi + format(int(initial_imsi[-10:]) + i, '010d')
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
        send_subscriber_data(imsi, payload)


# main function takes the command line arguments and calls the appropriate functions
if __name__ == "__main__":
    global conn
    parser = argparse.ArgumentParser(description="Free5GC subscriber helper")
    parser.add_argument("-i", "--imsi", help="imsi", required=True)
    parser.add_argument("-n", "--n_users", help="n_users", required=True)
    parser.add_argument("-u", "--base_url", help="base_url", required=True)
    args = parser.parse_args()
    imsi = args.imsi
    n_users = int(args.n_users)
    base_url = args.base_url
    if n_users < 1:
        print("n_users must be greater than 0")
        exit(1)
    print("Starting subscriber helper for imsi {}".format(imsi))
    conn = http.client.HTTPConnection(base_url)
    subscribe_users(imsi, n_users)