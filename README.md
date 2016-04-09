# bird-bgp-ospf

Bird internet routing daemon distributed under GNU General Public License is a fully functional routing engine that is deployed on linux 
and FreeBSD systems. For more details please go to http://bird.network.cz/

This project is to have valid tested configuration for Anycast VIP advertisments for opencontrail using either OSPF or BGP. 

It will have configuration of bird for OSPF and BGP and also include OSPF and BGP configurations for Junos QFX top of rack switch. 

# Ansible for bird configuration

Ansible is used for installing and configuring the servers with bird. Currently it supports debian systems. Support for redhat / centos will be added later.

Steps for running playbook:

1-> Update the inventory file with the servers that need to have bird installed
    
    Ex: 
        [birds]
        10.10.10.10
        20.20.20.20

2-> Update the bird_network_proto, vip and networks in group_vars/birds. The networks are the networks that you want the static route to be configured by bird on the servers and update the routing tables. 

3-> Run the setup.sh script

    Ex:
       `INVENTORY=/home/users/bird-admin/bird-hosts /home/users/bird-admin/setup.sh`
        or
        > pwd
        /home/users/bird-admin
        > export INVENTORY=/home/users/bird-admin/bird-hosts
        > ./setup.sh

The result of the above steps will be servers configured with bird OSPF.

# Sample configs 

Same config files for OSPF and BGP can be found here https://github.com/sanabby/bird-bgp-ospf/tree/master/sample-bird-configs
