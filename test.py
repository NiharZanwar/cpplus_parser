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
            # print(cursor.lastrowid)
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
            # print(cursor.lastrowid)
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


def update_alarm(sql_details, device_id, alarm_code, alarm_status, channel_no, data_time):
    connection = sql_connection(sql_details)
    if connection == 0:
        print("error while connectiong to database")
        return 0
    else:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE `alarm_table` SET `alarm_state`='{}' , `last_update_dt`='{}' WHERE `device_id`='{}' AND"
                "`alarm_code`='{}' AND `channel_no`='{}'".format(str(alarm_status), str(data_time), str(device_id)
                                                                 , str(alarm_code), str(channel_no)))
            connection.commit()
            connection.close()
            return 1
        except pymysql.Error as e:
            print("error : {} while updating datetime for tag".format(str(e)))
            return 0


alarm_master = {
    4: {
        "name": "video mask",
        "channel_specific": True
    },
    5: {
        "name":"video tamper",
        "channel_specific": True
    },
    6: {
        "name":"invalid_login",
        "channel_specific": False
    }
}


def process_data(sql_details, alarm_channel, time, alarm_code, tag, channel_string, extra_data, dvr_ip, data):

    device_info, success = get_device_info(sql_details, tag)
    if success == 0:
        return 200
    if len(device_info) == 0:
        device_id = add_device(sql_details, tag, 0, dvr_ip, data, time)
        if device_id == 0:
            return 201
    else:
        if device_info['is_active'] == 0:
            if update_dt(sql_details, tag, time) == 0:
                return 202
            else:
                return 100
        else:
            alarm_info, success = get_alarm_info(sql_details, device_info["device_id"], 1, alarm_code)
            if success == 0:
                return 203
            if len(alarm_info) == 0:

                for alarm in alarm_master:

                    if not alarm_master[alarm]["channel_specific"]:
                        add_alarm(sql_details, device_info["device_id"], 0, alarm, alarm_master[alarm]["name"],0,time)
                    else:
                        for i in range(1, device_info["channel_no"]+1):
                            add_alarm(sql_details, device_info["device_id"], i, alarm, alarm_master[alarm]["name"], 0, time)

                for i in range(31, 31 - device_info['channel_no'], -1):
                    if update_alarm(sql_details, device_info['device_id'], alarm_code, channel_string[i], 32 - i,
                                    time) == 0:

                        return 0

                return 0
            else:
                if device_info['channel_no'] is None:
                    return 0
                else:
                    if not alarm_master[alarm_code]["channel_specific"]:
                        if update_alarm(sql_details, device_info['device_id'], alarm_code, 1, 0, time) == 0:
                            return 0
                    for i in range(31, 31 - device_info['channel_no'], -1):
                        if update_alarm(sql_details, device_info['device_id'], alarm_code, channel_string[i], 32-i, time) == 0:
                            return 0


def process_data2(sql_details, alarm_channel, time, alarm_code, tag, channel_string, extra_data, dvr_ip, data):
    channel_string = channel_string[::-1]
    device_info, success = get_device_info(sql_details, tag)

    if success == 0:
        return 200

    if len(device_info) == 0:
        if add_device(sql_details, tag, 0, dvr_ip, data, time) == 0:
            return 201
        else:
            return 100

    if int(alarm_code) not in alarm_master:
        if update_dt(sql_details, tag, time) == 0:
            return 202
        return 209

    else:
        device_info = device_info[0]
        if device_info['is_active'] == 0:
            if update_dt(sql_details, tag, time) == 0:
                return 202
            else:
                return 101

        elif device_info['is_active'] == 1 and device_info['channel_no'] is not None:
            alarm_info, success = get_alarm_info(sql_details, device_info["device_id"], 1, alarm_code)
            if success == 0:
                return 203

            if len(alarm_info) == 0:
                for alarm in alarm_master:

                    if not alarm_master[alarm]["channel_specific"]:
                        alarm_id = add_alarm(sql_details, device_info["device_id"], 0, alarm,
                                             alarm_master[alarm]["name"], 0, time)
                        if alarm_id is not 0 and int(alarm_code) == alarm:

                            update_alarm(sql_details, device_info['device_id'], alarm, 0, 0, time)
                            add_transaction(sql_details, time, device_info['device_id'], alarm_id, 0, alarm_code,
                                            alarm_master[alarm]["name"], 0)

                        elif alarm_id == 0:
                            return 204

                    else:
                        for i in range(1, device_info["channel_no"] + 1):
                            alarm_id = add_alarm(sql_details, device_info["device_id"], i, alarm,
                                                 alarm_master[alarm]["name"], 0, time)

                            if alarm_id is not 0 and int(alarm_code) == alarm:
                                if update_alarm(sql_details, device_info['device_id'], alarm, channel_string[i-1], i, time) == 0:
                                    return 301
                                add_transaction(sql_details, time, device_info['device_id'], alarm_id, i, alarm_code,
                                                alarm_master[alarm]["name"], channel_string[i-1])

                            elif alarm_id == 0:
                                return 205

            else:

                for i in range(1, device_info['channel_no']+1):
                    alarm_info, success = get_alarm_info(sql_details, device_info['device_id'], i, alarm_code)
                    if success == 0:
                        return 206
                    alarm_info = alarm_info[0]
                    if alarm_master[int(alarm_code)]["channel_specific"]:
                        if alarm_info['alarm_state'] != int(channel_string[i-1]):
                            if update_alarm(sql_details, device_info['device_id'], alarm_code, channel_string[i-1], i,
                                            time) == 0:
                                return 207
                            if add_transaction(sql_details, time, device_info['device_id'], alarm_info['alarm_id'], i,
                                               alarm_code,
                                               alarm_master[alarm_code]["name"], channel_string[i-1]) == 0:
                                return 208

                    else:
                        if update_alarm(sql_details, device_info['device_id'], alarm_code, 0, 0,
                                        time) == 0:
                            return 207
                        if add_transaction(sql_details, time, device_info['device_id'], alarm_info['alarm_id'], 0,
                                           alarm_code,
                                           alarm_master[alarm_code]["name"], 0) == 0:
                            return 208
    return 500




from datetime import datetime
import time
sql_details1 = get_sql_details()
time_now = time.time()
result = process_data2(sql_details1,0,datetime.now().strftime("%Y-%m-%d %H:%M:%S"),5,12345,'00000100000000000000000000011111','11','192.168.1.11','uyuy')
print(time.time()-time_now)
print(result)



