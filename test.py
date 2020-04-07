
import pymysql
import configparser
import os

def get_config(path):
    try:
        config = configparser.ConfigParser()
        config.read(path + "/config.conf")
        return config
    except:
        print("error while opening config.")
        return 0

def get_sql_details():
    config = get_config(os.getcwd())
    if config == 0:
        return 0
    else:
        try:
            details = {
                "ip":config["mysql"]["ip"],
                "port":int(config["mysql"]["port"]),
                "username":config["mysql"]["uname"],
                "password":config["mysql"]["password"],
                "db_name":config["mysql"]["db_name"]
            }
            return details
        except:
            print("error while parsing config file. please check keys are present")


def sql_connection(details):
    try:
        connection = pymysql.connect(host=details["ip"],
                                     user=details["username"],
                                     password=details["password"],
                                     db=details["db_name"],
                                     port=details["port"])
        return connection
    except pymysql.Error as e:
        print(e)
        return 0

import time

# time_now = time.time()
# details = get_sql_details()
# print(time.time()-time_now)
# sql_connection(details)


def add_device(sql_details ,tag, active_status, ip, rcvd_str, create_dt):

    connection = sql_connection(sql_details)
    if connection == 0:
        print("could not add device to sql")
        return 0
    else:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO `device_table`(`tag`, `is_active`, `ip`, `rcvd_str`, `create_dt`, `last_update_dt`)"
                "VALUES ('{}','{}','{}','{}','{}','{}')".format(str(tag), str(active_status), str(ip),
                                                                str(rcvd_str), str(create_dt), str(create_dt)))
            connection.commit()
            print(cursor.lastrowid)
            connection.close()
            return int(cursor.lastrowid)
        except pymysql.Error as e:
            print("Error while adding device to sql : {}".format(e))
            return 0

from datetime import datetime
time_now = time.time()
sql_details = get_sql_details()
a = add_device(sql_details ,'124', '0', '192.168.1.1', 'abc', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print(time.time()-time_now)
print(a)