#!/usr/bin/python

DOCUMENTATION = '''
---
module: sample
short_description: A sample module for reading yaml file and returning the content
'''

EXAMPLES = '''
- name: Read variables from yaml file
  sample:
    file: "..."
  register: result
'''

import yaml
from yaml.loader import SafeLoader
from ansible.module_utils.basic import *

def parse_descriptors(file):
	# print(file)
	with open(file) as f:
		data = yaml.load(f, Loader=SafeLoader)
		# print(data)
	return data

def main():

	fields = {
		"file": {"required": True, "type": "str"},
	}

	module = AnsibleModule(argument_spec=fields)
	response = {"hello": "world"}
	data = parse_descriptors(module.params['file'])
	# res = { "indo": data }
	module.exit_json(changed=False, meta=data)


if __name__ == '__main__':
    main()