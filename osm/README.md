
## Install OSM

```bash
wget https://osm-download.etsi.org/ftp/osm-11.0-eleven/install_osm.sh
chmod +x install_osm.sh
./install_osm.sh 2>&1 | tee osm_install_log.txt
```

Login details. Host: localhost, user:admin, password: admin

`Added 'osm' model on k8scloud with credential 'k8scloud' for user 'admin'`

`Note: If you already have helm installed, make sure it's >= v3.2. The installation uses helm to install openebs. It creates a namespace for the openebs using the --create-namespace tag which is only supported >= 3.2. I ran into this issue where openebs was failing to install and hence OSM.`

## Local development environment using microk8s

```bash
# install Microk8s 
sudo snap install microk8s  --classic
sudo usermod -a -G microk8s `whoami`
newgrp microk8s
microk8s.status --wait-ready
```

Microk8s uses addons to extend its functionality. The required addons for Microk8s to work with OSM are “storage” and “dns”.

```bash
microk8s.enable storage dns
```

You may want to use the metallb addon if your Microk8s is not running in the same machine as OSM

```bash
microk8s.enable metallb
```

Add kubernetes cluster. It needs to be associated to a VIM. You can use an openstack VIM. There is also an option of creating a dummy VIM and assosicating it to it. Check out [link](https://osm.etsi.org/docs/user-guide/latest/05-osm-usage.html#adding-kubernetes-cluster-to-osm) for more information.

```bash
microk8s.config > kubeconfig.yaml

# Optional, for testing: create a dummy VIM to associate k8s to 
osm vim-create --name dummyvim --user u --password p --tenant p --account_type dummy --auth_url http://localhost/dummy

osm k8scluster-add --creds kubeconfig.yaml \
                   --version '1.24' \
                   --vim dummyvim \
                   --description "My K8s cluster" \
                   --k8s-nets '{"net1": "osm-ext"}' \
                   microk8s-cluster
```
## Local development environment using microstack

```bash
sudo snap install microstack --beta --devmode
sudo microstack init --auto --control
```

## Deploy test KNF

```bash
osm repo-add --type helm-chart --description "Bitnami repo" bitnami https://charts.bitnami.com/bitnami
osm repo-add --type helm-chart --description "Cetic repo" cetic https://cetic.github.io/helm-charts
osm repo-add --type helm-chart --description "Elastic repo" elastic https://helm.elastic.co
osm repo-list
osm repo-show bitnami
```

Download and create KNF Helm Chart

```bash
wget https://osm-download.etsi.org/ftp/Packages/examples/openldap_knf.tar.gz
wget https://osm-download.etsi.org/ftp/Packages/examples/openldap_ns.tar.gz
osm nfpkg-create openldap_knf.tar.gz
osm nspkg-create openldap_ns.tar.gz
```

Deploy

```bash
osm ns-create --ns_name ldap --nsd_name openldap_ns --vim_account dummyvim

# Check status
osm ns-op-list ldap
```