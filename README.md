# Open Gi-LAN

The project builds the stack/infrastructure for an Open Gi-LAN or just Open LAN (Local Arear Network). The LAN sits after the mobile core network and will apply various network functions to the traffic from the core network.

## Installation

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install packages
pip install -r requirements.txt

```

## Connect to test bed with a bastion host

```bash
# generate ssh key(s). using different keys for bastion host and the testbed servers
ssh-keygen -t rsa -b 2048

# add the public key(s) to the bastion host and testbed servers (replace id_rsa.pub with key name)
cat ~/.ssh/id_rsa.pub

# copy above and put in other servers (can use ssh-copy-id instead)
mkdir ~/.ssh
echo ssh_pub_key >> ~/.ssh/authorized_keys
```

Add the following to `~/.ssh/config`

```text
Host bastion
  HostName url
    ForwardAgent yes
  User username
  IdentityFile ~/.ssh/id_rsa
```

```bash
# test connection through bastion host
ssh -o ProxyCommand="ssh -W %h:%p -q bastion" -i ~/.ssh/chpc user@10.x.x.x
```

## Run playbook

```bash
ansible-playbook -i inventory.ini collect.yml -K
```