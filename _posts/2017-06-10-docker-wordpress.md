---
layout: post
title: Docker For WordPress
date: 2017-06-10 16:32:22
categories: security
---
WordPressの脆弱性を検証するための環境(空のWordPress環境)をDockerで簡単に構築できるので紹介します。

[https://github.com/kobad/docker-wordpress](https://github.com/kobad/docker-wordpress)

Dockerでは公式にWordPressの環境構築してくれるのがあるので、それを使って環境を作成します。[https://docs.docker.com/compose/wordpress/](https://docs.docker.com/compose/wordpress/)

以下のような docker-compose.yml を作成します。
```
version: '3'

services:
   db:
     image: mysql:5.7
     volumes:
       - db_data:/var/lib/mysql
     restart: always
     environment:
       MYSQL_ROOT_PASSWORD: somewordpress
       MYSQL_DATABASE: wordpress
       MYSQL_USER: wordpress
       MYSQL_PASSWORD: wordpress

   wordpress:
     depends_on:
       - db
     image: wordpress:4.7.0
     ports:
       - "8000:80"
     restart: always
     environment:
       WORDPRESS_DB_HOST: db:3306
       WORDPRESS_DB_USER: wordpress
       WORDPRESS_DB_PASSWORD: wordpress
volumes:
    db_data:
```

image: wordpress: に構築したいバージョンを指定します。

次に、docker-compose.ymlを作成したディレクトリで、

`$ docker-compose up -d `

を実行すれば終わりです。

```
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                  NAMES
61e2b4daaca2        wordpress:4.7.0     "docker-entrypoint..."   6 seconds ago       Up 4 seconds        0.0.0.0:8000->80/tcp   wordpress_wordpress_1
d2723f64133e        mysql:5.7           "docker-entrypoint..."   7 seconds ago       Up 5 seconds        3306/tcp               wordpress_db_1
```

http:localhost:8000 にて、動いているので初期設定をすれば完成です。

初期化したい場合は、
1. `$ docker-compose down --volumes `
2. `$ docker-compose up -d `

で1から作成されます。
