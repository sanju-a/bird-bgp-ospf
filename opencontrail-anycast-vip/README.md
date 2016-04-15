OpenContrail anycast vip support for opencontrail API and control plane

config file: anycast_vip.conf

[DEFAULTS]
vip=1.1.1.1
lb_backend=apache-backend


To run, execute as shown below

> python manage_vip.py --vip 192.168.1.17 --lb_backend apache-backend

OR

> python manage_vip.py --conf_file anycast_vip.conf
