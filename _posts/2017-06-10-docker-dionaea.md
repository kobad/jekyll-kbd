---
layout: post
title: Docker for Dionaea
date: 2017-06-10 14:47:31
categories: security
---
低対話型ハニーポットであるDionaeaを構築するDockerfileを作成しました。(https://github.com/kobad/docker-dionaea)

手順とかをまとめておく。

## Dionaea 構築

image: Ubuntu16.04

ほぼ[ココ](https://gist.github.com/ytn86/7bc4130aca64ce77d1d6)通りですが、変更点を書く。

Python, Cython等のバージョンを最新にする。

* LibEv - http://dist.schmorp.de/libev/Attic/
* LibPcap - http://www.tcpdump.org/release/
* Python - http://www.python.org/ftp/python/
* Cython - https://pypi.python.org/pypi?%3Aaction=search&term=cython&submit=search
* OpenSSL - https://github.com/openssl/openssl/

Dionaeaインストール時の

`find ./ -type f | xargs sed -i "s/-Werror//g"`だと、ビルドでこけるので、

`find ./ -type f -print0 | xargs -0 sed -i "s/-Werror//g"`に変更。

## Dionaea 設定

### ログ制御 - 最低限のログ出力にする (/opt/dionaea/etc/dionaea/dionaea.conf)
```
logging = {
	default = {
		// file not starting with / is taken relative to LOCALESTATEDIR (e.g. /opt/dionaea/var)
		file = "log/dionaea.log"
		levels = "all, -debug"
		domains = "*"
    }

	errors = {
		// file not starting with / is taken relative to LOCALESTATEDIR (e.g. /opt/dionaea/var)
		file = "log/dionaea-errors.log"
		levels = "error"
		domains = "*"
	}
}
```

### Nmap 検知回避
デフォルトだとNmapに検知されるので、それをある程度防ぐ。

#### ftp.py - welcome massage を変更する (/opt/dionaea/lib/dionaea/python/dionaea/ftp.py)
```
def handle_established(self):
  self.processors()
  self.reply(WELCOME_MSG, "Start the ftp service")
```

#### mssql.py - TokenType を変更(0x01) (/opt/dionaea/lib/dionaea/python/dionaea/mssql/mssql.py)
```
if PacketType == TDS_TYPES_PRE_LOGIN:
			r = TDS_Prelogin_Response()
			#FIXME: any better way to initialise this?
			r.VersionToken.TokenType = 0x01
			r.VersionToken.Offset = 26
			r.VersionToken.Len = 6
			r.EncryptionToken.TokenType = 0x01
			r.EncryptionToken.Offset = 32
			r.EncryptionToken.Len = 1
			r.InstanceToken.TokenType = 0x02
			r.InstanceToken.Offset = 33
			r.InstanceToken.Len = 1
			r.ThreadIDToken.TokenType = 0x03
			r.ThreadIDToken.Offset = 34
			r.ThreadIDToken.Len = 0
			r.MARSToken.TokenType = 0x04
			r.MARSToken.Offset = 34
			r.MARSToken.Len = 1
```

#### index.html - indexページを作成 (/opt/dionaea/var/dionaea/wwwroot/)
任意のhtmlを置いておく。

## Dockerfile

一連の流れを記入し、dionaea用のユーザに登録して終わり。

* Build - `$ docker build -t dionaea .`
* Run -
```
$ docker run -u dionaea -it -p 21:21 -p 42:42 -p 69:69/udp -p 80:80 -p 135:135 -p 443:443 -p 445:445 -p 1433:1433 -p 1723:1723 -p 1883:1883 -p 1900:1900/udp -p 3306:3306 -p 5060:5060 -p 5060:5060/udp -p 5061:5061 -p 11211:11211 dionaea
```
* Start - `container$ /opt/dionaea/bin/dionaea -D`
* Detach - `Ctrl-p, Ctrl-q`

結果
```

Starting Nmap 7.40 ( https://nmap.org ) at 2017-06-07 15:49 JST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00023s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 987 closed ports
PORT      STATE SERVICE
21/tcp    open  ftp
42/tcp    open  nameserver
80/tcp    open  http
135/tcp   open  msrpc
443/tcp   open  https
445/tcp   open  microsoft-ds
1433/tcp  open  ms-sql-s
1723/tcp  open  pptp
3306/tcp  open  mysql
5060/tcp  open  sip
5061/tcp  open  sip-tls
49152/tcp open  unknown
49153/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 9.25 secondss
```
----
以下、完成したDockerfile
```
FROM ubuntu:16.04

# Libraries
RUN apt-get update
RUN set -x && \
  apt-get -y install \
  wget \
  curl \
  libudns-dev \
  libglib2.0-dev \
  libssl-dev \
  libcurl4-openssl-dev \
  libreadline-dev \
  libsqlite3-dev \
  python-dev \
  libtool \
  automake \
  autoconf \
  build-essential \
  subversion \
  git-core \
  flex \
  bison \
  pkg-config \
  libnl-3-dev \
  libnl-genl-3-dev \
  libnl-nf-3-dev \
  libnl-route-3-dev \
  sqlite3

# Clone Dionaea
RUN cd /opt/ && git clone https://github.com/rep/dionaea.git dionaea

# Install Liblcfg
RUN set -x && \
  cd /usr/local/src && \
  git clone https://github.com/pb-/liblcfg.git liblcfg && \
  cd liblcfg/code && \
  autoreconf -vi && \
  ./configure -prefix=/opt/dionaea && \
  make install

# Install Libemu
RUN set -x && \
  cd /usr/local/src && \
  git clone https://github.com/cperdana/libemu.git libemu && \
  cd libemu && \
  autoreconf -vi && \
  find ./ -type f | xargs sed -i "s/-Werror//g" && \
  ./configure -prefix=/opt/dionaea && \
  make && \
  make install

# Install LibEv
RUN set -x && \
  cd /usr/local/src &&  \
  wget http://dist.schmorp.de/libev/Attic/libev-4.20.tar.gz && \
  tar xzf libev-4.20.tar.gz && \
  cd libev-4.20 && \
  ./configure -prefix=/opt/dionaea && \
  make install

# Install Libpcap
RUN set -x && \
  cd /usr/local/src && \
  wget http://www.tcpdump.org/release/libpcap-1.8.1.tar.gz && \
  tar xzf libpcap-1.8.1.tar.gz && \
  cd libpcap-1.8.1 && \
  ./configure -prefix=/opt/dionaea && \
  make install

# Install Python
RUN set -x && \
  cd /usr/local/src && \
  wget http://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz && \
  tar xzf Python-3.6.1.tgz && \
  cd Python-3.6.1 && \
  ./configure --enable-shared -prefix=/opt/dionaea --with-computed-gotos -enable-ipv6 LDFLAGS="-Wl,-rpath=/opt/dionaea/lib -L/usr/lib/x86_64-linux-gnu/" && \
  make && \
  make install

# Install Cython
RUN set -x && \
  cd /usr/local/src && \
  wget https://pypi.python.org/packages/c6/fe/97319581905de40f1be7015a0ea1bd336a756f6249914b148a17eefa75dc/Cython-0.24.1.tar.gz && \
  tar xzf Cython-0.24.1.tar.gz && \
  cd Cython-0.24.1 && \
  /opt/dionaea/bin/python3 setup.py install

# Install Openssl
RUN set -x && \
  cd /usr/local/src && \
  wget https://github.com/openssl/openssl/archive/OpenSSL_1_0_1p.tar.gz && \
  tar xzf OpenSSL_1_0_1p.tar.gz && \
  cd openssl-OpenSSL_1_0_1p && \
  ./Configure shared --prefix=/opt/dionaea linux-x86_64 && \
  make && \
  make install

# Install Dionaea
RUN set -x && \
  cd /opt/dionaea && \
  autoreconf -vi && \
  find ./ -type f -print0 | xargs -0 sed -i "s/-Werror//g" && \
  rm -rf /opt/dionaea/modules/python/util/gnuplotsql && \
  ./configure --with-lcfg-include=/opt/dionaea/include/ \
      --with-lcfg-lib=/opt/dionaea/lib/ \
      --with-python=/opt/dionaea/bin/python3.6 \
      --with-cython-dir=/opt/dionaea/bin \
      --with-udns-include=/opt/dionaea/include/ \
      --with-udns-lib=/opt/dionaea/lib/ \
      --with-emu-include=/opt/dionaea/include/ \
      --with-emu-lib=/opt/dionaea/lib/ \
      --with-gc-include=/usr/include/gc \
      --with-ev-include=/opt/dionaea/include \
      --with-ev-lib=/opt/dionaea/lib \
      --with-nl-include=/opt/dionaea/include \
      --with-nl-lib=/opt/dionaea/lib/ \
      --with-curl-config=/usr/bin/ \
      --with-pcap-include=/opt/dionaea/include \
      --with-pcap-lib=/opt/dionaea/lib/ \
      --with-ssl-include=/opt/dionaea/include/ \
      --with-ssl-lib=/opt/dionaea/lib/ && \
  make && \
  make install

# Setup Dionaea
ADD config /opt/dionaea/etc/dionaea/config
RUN /bin/bash /opt/dionaea/etc/dionaea/config/setup.sh

# Add User
RUN groupadd --gid 1000 dionaea && \
  useradd -m --uid 1000 --gid 1000 dionaea && \
  chown -R dionaea:dionaea /opt/dionaea/var


```
