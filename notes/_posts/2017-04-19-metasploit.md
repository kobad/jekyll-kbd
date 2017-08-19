---
layout: post
title: "Metasploit"
date: 2017-04-19 23:00:00 +0900
toc: true
---

## Metasploit Training
https://www.offensive-security.com/metasploit-unleashed/

Kali LinuxとMetasploitable2を立てておく。

VM同士の通信設定 - https://www.youtube.com/watch?v=e0vpBKRZPGc
要点だけ書くと、VMのネットワーク設定を以下のように設定
```
Kali Linux - NAT, Host Only Adaptor
Metasploitable2 - Host Only Adaptor
```

Kali側からMetasploitable2に対してnmapして以下のようになれば、設定はOK.
```
Starting Nmap 7.40 ( https://nmap.org ) at 2017-07-04 16:58 UTC
Nmap scan report for 192.168.99.100
Host is up (0.00011s latency).
Not shown: 977 closed ports
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
23/tcp   open  telnet
25/tcp   open  smtp
53/tcp   open  domain
80/tcp   open  http
111/tcp  open  rpcbind
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
512/tcp  open  exec
513/tcp  open  login
514/tcp  open  shell
1099/tcp open  rmiregistry
1524/tcp open  ingreslock
2049/tcp open  nfs
2121/tcp open  ccproxy-ftp
3306/tcp open  mysql
5432/tcp open  postgresql
5900/tcp open  vnc
6000/tcp open  X11
6667/tcp open  irc
8009/tcp open  ajp13
8180/tcp open  unknown
MAC Address: 08:00:27:B6:B9:DB (Oracle VirtualBox virtual NIC)

Nmap done: 1 IP address (1 host up) scanned in 0.42 seconds
```
