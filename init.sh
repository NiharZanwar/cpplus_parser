#!/bin/bash
mkdir sql-data python-data

sudo docker network create -d bridge alarm-network

sudo docker run -d --restart always -p 33067:3306 --name alarm-mysql -v `pwd`/sql-data:/var/lib/mysql \
-v `pwd`/mysql-scripts:/docker-entrypoint-initdb.d/ \
-e MYSQL_ROOT_PASSWORD=toor -e MYSQL_DATABASE=dvr --network alarm-network mysql

sudo docker build -t alarm-server .

sudo docker run -d --restart always -p 5050:5001 --name alarm-server-container -v `pwd`/python-data:/data \
--network alarm-network alarm-server

sudo cp config.conf python-data/config.conf

