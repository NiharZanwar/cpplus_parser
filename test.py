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
                "ip": config["mysql"]["ip"],
                "port": int(config["mysql"]["port"]),
                "username": config["mysql"]["uname"],
                "password": config["mysql"]["password"],
                "db_name": config["mysql"]["db_name"]
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
                                     port=details["port"],
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
    except pymysql.Error as e:
        print(e)
        return 0


def add_device(sql_details, tag, active_status, ip, rcvd_str, create_dt):
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


def get_device_info(sql_details, tag):
    connection = sql_connection(sql_details)
    if connection == 0:
        print("error while connecting to database")
        return '', 0
    else:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM `device_table` WHERE tag='{}'".format((str(tag))))
            response = cursor.fetchall()
            connection.close()
            return response, 1
        except pymysql.Error as e:
            print("error : {} while fetching device info for tag : {}".format(str(e), tag))
            return '', 0


def update_dt(sql_details, tag, date_time):
    connection = sql_connection(sql_details)
    if connection == 0:
        print("error while connectiong to database")
        return 0
    else:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE `device_table` SET `last_update_dt`='{}' WHERE `tag`='{}'".format(str(date_time)
                                                                                                     , str(tag)))
            connection.commit()
            connection.close()
            return 1
        except pymysql.Error as e:
            print("error : {} while updating datetime for tag : {}".format(str(e), str(tag)))
            return 0


def add_alarm(sql_details, device_id, channel_no, alarm_code, alarm_name, alarm_status, create_dt):
    connection = sql_connection(sql_details)
    if connection == 0:
        print("could not connect to database")
        return 0
    else:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO `alarm_table`(`device_id`, `alarm_state`, `channel_no`, `alarm_code`, `create_dt`,"
                " `last_update_dt`,`alarm_name`)"
                "VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(str(device_id), str(alarm_status), str(channel_no),
                                                                     str(alarm_code), str(create_dt), str(create_dt),
                                                                     str(alarm_name)))
            connection.commit()
            print(cursor.lastrowid)
            connection.close()
            return int(cursor.lastrowid)
        except pymysql.Error as e:
            print("Error while adding new alarm to sql : {}".format(e))
            return 0


#
# from datetime import datetime
# sql_details = get_sql_details()
# result = add_alarm(sql_details, '4', 3, '36', 'video mask', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# print(result)


def get_alarm_info(sql_details, device_id, channel_no, alarm_code):
    connection = sql_connection(sql_details)
    if connection == 0:
        print("error while connecting to database")
        return '', 0
    else:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM `alarm_table` WHERE device_id='{}' AND channel_no='{}'"
                           " AND alarm_code='{}'".format(str(device_id), str(channel_no), str(alarm_code)))
            response = cursor.fetchall()
            connection.close()
            return response, 1
        except pymysql.Error as e:
            print("error : {} while fetching alarm info")
            return '', 0


def add_transaction(sql_details, date_time, device_id, alarm_id, channel_no, alarm_code, alarm_name, alarm_state):
    connection = sql_connection(sql_details)
    if connection == 0:
        print("could not connect to database")
        return 0
    else:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO `txn_table`(`device_id`, `alarm_state`, `channel_no`, `alarm_code`, `alarm_name`,"
                "`date_time`, `alarm_id`)"
                "VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(str(device_id), str(alarm_state), str(channel_no),
                                                                     str(alarm_code), str(alarm_name), str(date_time),
                                                                     str(alarm_id)))
            connection.commit()
            connection.close()
            return 1

        except pymysql.Error as e:
            print("Error while adding new transaction to sql : {}".format(e))
            return 0


# from datetime import datetime
# sql_details = get_sql_details()
# result = add_transaction(sql_details, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 4, 2, 4, 45, 'nihar', 1)
# print(result)