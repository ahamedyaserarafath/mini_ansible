# Mini Ansible - Python - Fabric
- [Introduction](#Introduction)
- [Pre-requisites](#pre-requisites)
- [Installation and configuration](#Installation-and-configuration)

# Introduction
Tired of installing ansible and writing configuration which you don't know, but you know the command to install means you are in right place, I have a made mini ansible just clone and add ur command on conf it works like a charm.

- [Pre-requisites](#pre-requisites)
Just python typically every linux os has default python package installed so just clone and try it out.

- [Installation and configuration](#Installation-and-configuration)
Clone the project locally to your linux machine, it support execution of commands as well as sending a file from local.
This project both IP and DNS as well it can be either password or key.

Make configuration changes by edit the mini_ansible.conf file.
Please find the reference below.
```
# [UniqueName]
# ip = IP/DNS
# username = ubuntu
# password = test@123
# or
# key = /tmp/test.pem
# cmd = apt-get install python
# or
# local_path = file.txt
# remote_path = /tmp/.
```
Below example for your reference.
```
...
[ssh_host_1]
ip = 10.10.10.10
username = ubuntu
private_key = /tmp/tmp.pem
command = ls
...
...
[ssh_host_2]
ip = 10.10.10.11
username = ubuntu
password = test
....
```
You can any number of host, one things which I'm still working on is parallel execution as of now it support one by one execution.

Finally the run the below command to start the execution.
```
python mini_ansible.py
```

Check the logs folder for your reference.



