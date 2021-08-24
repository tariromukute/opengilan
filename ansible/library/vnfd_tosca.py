#!/usr/bin/python

DOCUMENTATION = '''
---
module: vnfd_tosca

short_description: A module that reads TOSCA based VNFD. The module parse the VNFD to specific POP descriptors
version_added: "1.0.0"

description: The module is designed agains the standard ETSI GS NFV-SOL 001 V3.3.1. This will be referenced across the implementation of this module

options:
    vnfd:
        description: The path to the vnfd file
        required: True
        type: str
    target:
        description: The POP that the vnfd is being parsed for
        required: True
        type: str

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = '''
- name: Read parse VNFD to AWS descriptors
  sample:
    vnfd: "..."
    target: aws
  register: result
'''

import yaml
from yaml.loader import SafeLoader
from ansible.module_utils.basic import *

vnfd_schema = None

# 6. VNFD TOSCA model

# 6.2.1 tosca.datatypes.nfv.CpProtocolData

def tosca_datatypes_nfv_CpProtocolData(data):
    fields = {

    }

    res = None
    return res

# 6.2.2 tosca.datatypes.nfv.AddressData
def tosca_datatypes_nfv_AddressData(data):

    fields = {

    }

    res = AnsibleModule(argument_spec=fields)
    return res

# 6.2.4 tosca.datatypes.nfv.VirtualNetworkInterfaceRequirements
def tosca_datatypes_nfv_VirtualNetworkInterfaceRequirements(data):
    fields = {
        "name": {
            "type": "str",
            "description": "Provides a human readable name for the requirement.",
            "required": False
        },
        "description": {
            "type": "str",
            "description": "Provides a human readable description of the requirement.",
            "required": False
        },
        "support_mandatory": {
            "type": "bool",
            "description": "Indicates whether fulfilling the constraint is mandatory (TRUE) for successful operation or desirable (FALSE).",
            "required": True
        },
        "network_interface_requirements": {
            "type": "map",
            "description": "The network interface requirements. A map of strings that contain a set of key-value pairs that describes the hardware platform specific  network interface deployment requirements.",
            "required": True,
            "entry_schema": {
            "type": "str"
            }
        },
        "nic_io_requirements": {
            "type": "tosca.datatypes.nfv.LogicalNodeData",
            "description": "references (couples) the CP with any logical node I/O requirements (for network devices) that may have been created. Linking these attributes is necessary so that so that I/O requirements that need to be articulated at the logical node level can be associated with the network interface requirements associated with the CP.",
            "required": False
        }
    }

    res = AnsibleModule(argument_spec=fields)
    return res.params

def parse_descriptors(file):
    # print(file)
    with open(file) as f:
        data = yaml.load(f, Loader=SafeLoader)
        # print(data)
    return data

# 5.6 Imports statement
def parse_desc_imports(file):
    data = parse_descriptors(file)
    res = data['imports'] if isinstance(data['imports'][0], str) else [x['file'] for x in data['imports']]

    # import the files

    # Read the components
    
    return res

def main():

    fields = {
        "vnfd": {"required": True, "description": "describe", "type": "str"},
        "target": { }
    }

    module = AnsibleModule(argument_spec=fields)
    data = parse_descriptors(module.params['vnfd'])
    d = parse_desc_imports(data)
    # res = { "indo": data }
    module.exit_json(changed=False, meta=vnfd_schema)


if __name__ == '__main__':
    with open('files/etsi_nfv_sol001_vnfd_types.yaml') as f:
        vnfd_schema = yaml.load(f, Loader=SafeLoader)
    main()