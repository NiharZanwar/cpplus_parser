FROM python:3


RUN apt-get update
RUN	mkdir /app /data
RUN mkdir /data/log
RUN	pip install pymysql configparser

COPY install.sh /app

RUN chmod +x /app/install.sh

ENTRYPOINT ["./app/install.sh"]