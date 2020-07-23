FROM python:3


RUN apt-get update
RUN	mkdir /app /config /logs
RUN	pip install pymysql configparser cryptography requests

COPY install.sh /app

RUN chmod +x /app/install.sh

ENTRYPOINT ["./app/install.sh"]