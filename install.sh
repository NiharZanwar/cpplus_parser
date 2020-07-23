#!/bin/bash
mkdir /data
cd /app
git clone https://github.com/NiharZanwar/cpplus_parser.git
cd cpplus_parser
git checkout docker-version
cd /app/cpplus_parser
python parser.py &
ps -aef
cd /data/log;
python -m http.server 8008
