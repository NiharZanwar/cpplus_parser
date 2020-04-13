#!/bin/bash
cd /app
git clone https://github.com/NiharZanwar/cpplus_parser.git
cd cpplus_parser
echo "clone complete"
cd /app/cpplus_parser
python parser.py &
ps -aef
cd /data/log;
python -m http.server 8008
