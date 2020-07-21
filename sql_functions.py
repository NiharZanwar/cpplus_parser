import pymysql
import configparser
from globals import alarm_master, log_dir, config_dir
from datetime import datetime
from requests import post
import json


def log_error(string, time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
    string += "\n\n"
    with open(log_dir + "/error_log.txt", "a+") as f:
        f.write(time + ' : ' + string)


def get_config(path):
    try:
        config = configparser.ConfigParser()
        config.read(path + "/config.conf")
        return config
    except:
        log_error("error while opening config file. check if file is present in directory {}".format(path))
        return 0


def get_sql_details():
    config = get_config(config_dir)
    if config == 0:
        log_error("get_config function returned zero")
        return 0
    else:
        try:
            details = {
                "ip": config["mysql"]["ip"],
                "port": int(config["mysql"]["port"]),
                "username": config["mysql"]["uname"],
                "password": config["mysql"]["password"],
                "db_name": config["mysql"]["db_name"],
                "http": config["send_to"]["path"]
            }
            return details
        except Exception as e:
            log_error("error while parsing config file. check keys - {}".format(e))
            return 0


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
        log_error("error while connecting to database in sql_connection - {}".format(e))
        return 0


def add_device(sql_details, tag, active_status, ip, rcvd_str, create_dt):
    connection = sql_connection(sql_details)
    if connection == 0:
        log_error("error while connecting to database in add_device function ")
        return 0
    else:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO `cpplus_device_dvr`(`tag`, `is_active`, `ip`, `rcvd_str`, `create_dt`, `last_update_dt`)"
                "VALUES ('{}','{}','{}','{}','{}','{}')".format(str(tag), str(active_status), str(ip),
                                                                str(rcvd_str), str(create_dt), str(create_dt)))
            connection.commit()
            connection.close()
            return int(cursor.lastrowid)
        except pymysql.Error as e:
            log_error("error while adding data in add_device function - {}".format(e))
            return 0


def get_device_info(sql_details, tag):
    connection = sql_connection(sql_details)
    if connection == 0:
        log_error("error while connecting to database in get_device_info function ")
        return '', 0
    else:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM `cpplus_device_dvr` WHERE tag='{}'".format((str(tag))))
            response = cursor.fetchall()
            connection.close()
            return response, 1
        except pymysql.Error as e:
            log_error("error while retrieving data in get_device_info - {}".format(e))
            return '', 0


def update_dt(sql_details, tag, date_time):
    connection = sql_connection(sql_details)
    if connection == 0:
        log_error("error while connecting to database in update_dt function ")
        return 0
    else:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE `cpplus_device_dvr` SET `last_update_dt`='{}' WHERE `tag`='{}'".format(str(date_time)
                                                                                                          , str(tag)))
            connection.commit()
            connection.close()
            return 1
        except pymysql.Error as e:
            log_error("error while updating values in update_dt function - {}".format(e))
            return 0


def add_alarm(sql_details, device_id, channel_no, alarm_code, alarm_name, alarm_status, create_dt, panel_code):
    connection = sql_connection(sql_details)
    if connection == 0:
        log_error("error while connecting to database in add_alarm function ")
        return 0
    else:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO `cpplus_alarm_dvr`(`device_id`, `alarm_state`, `channel_no`, `alarm_code`, `create_dt`,"
                " `last_update_dt`,`alarm_name`, `panel_code`)"
                "VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(str(device_id), str(alarm_status),
                                                                          str(channel_no),
                                                                          str(alarm_code), str(create_dt),
                                                                          str(create_dt),
                                                                          str(alarm_name), str(panel_code)))
            connection.commit()
            # print(cursor.lastrowid)
            connection.close()
            return int(cursor.lastrowid)
        except pymysql.Error as e:
            log_error("error while adding data in add_alarm function - {}".format(e))
            return 0


def get_alarm_info(sql_details, device_id, channel_no, alarm_code):
    connection = sql_connection(sql_details)
    if connection == 0:
        log_error("error while connecting to database in get_alarm_info function ")
        return '', 0
    else:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM `cpplus_alarm_dvr` WHERE device_id='{}' AND channel_no='{}'"
                           " AND alarm_code='{}'".format(str(device_id), str(channel_no), str(alarm_code)))
            response = cursor.fetchall()
            connection.close()
            return response, 1
        except pymysql.Error as e:
            log_error("error while retrieving data in get_alarm_info - {}".format(e))
            return '', 0


def add_transaction(sql_details, date_time, device_id, alarm_id, channel_no, alarm_code, alarm_name, alarm_state,
                    alarm_sent):
    connection = sql_connection(sql_details)
    if connection == 0:
        log_error("error while connecting to database in add_transaction function ")
        return 0
    else:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO `cpplus_txn_dvr`(`device_id`, `alarm_state`, `channel_no`, `alarm_code`, `alarm_name`,"
                "`date_time`, `alarm_id`, `alarm_sent`)"
                "VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(str(device_id), str(alarm_state),
                                                                          str(channel_no),
                                                                          str(alarm_code), str(alarm_name),
                                                                          str(date_time),
                                                                          str(alarm_id), str(alarm_sent)))
            connection.commit()
            connection.close()
            return 1

        except pymysql.Error as e:
            log_error("error while adding transaction in add_transaction".format(e))
            return 0


def update_alarm(sql_details, device_id, alarm_code, alarm_status, channel_no, data_time):
    connection = sql_connection(sql_details)
    if connection == 0:
        log_error("error while connecting to database in update_alarm function ")
        return 0
    else:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE `cpplus_alarm_dvr` SET `alarm_state`='{}' , `last_update_dt`='{}' WHERE `device_id`='{}' AND"
                "`alarm_code`='{}' AND `channel_no`='{}'".format(str(alarm_status), str(data_time), str(device_id)
                                                                 , str(alarm_code), str(channel_no)))
            connection.commit()
            connection.close()
            return 1
        except pymysql.Error as e:
            log_error("error while updating alarm in update_alarm function - {}".format(e))
            return 0


def print_json(http_details, tag, time, eventcode, channel, alarm_state):
    response = {
        "HE": {
            "ID": tag,
        },
        "TX": []
    }
    TX = {
            "DT": str(time),
            "EN": "",
            "CMNT": ""
        }

    if alarm_master[eventcode]['channel_specific']:

        if int(alarm_state) == 1:
            event = alarm_master[eventcode]["error_code"] + '000'
            TX["EN"] = event
            TX["CMNT"] = "Channel " + str(channel)
            response["TX"].append(TX)
        else:
            event = alarm_master[eventcode]["ok_code"] + '000'
            TX["EN"] = event
            TX["CMNT"] = "Channel " + str(channel)
            response["TX"].append(TX)
    else:
        event = alarm_master[eventcode]["eventcode"]
        TX["EN"] = event
        TX["CMNT"] = "Channel " + str(channel)
        response["TX"].append(TX)
    try:
        http_response = post(http_details["http"], json=response)
        if http_response.status_code == 200:
            resp_json = json.loads(http_response.text)
            if resp_json["Status"] == 'Fail':
                log_error("Status return fail - {}".format(json.dumps(resp_json)))
                return 0
            if resp_json["Status"] == 'Success':
                return 1
        return 0
    except Exception as error:
        log_error("Exception while posting data - {}".format(error))
        return 0


def process_data2(sql_details, time, alarm_code, tag, channel_string, dvr_ip, data):
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
        return 203

    else:
        device_info = device_info[0]
        if device_info['is_active'] == 0:
            if update_dt(sql_details, tag, time) == 0:
                return 204
            else:
                return 101

        elif device_info['is_active'] == 1 and device_info['channel_no'] is not None:

            if alarm_master[int(alarm_code)]["channel_specific"]:
                check_value = 1
            else:
                check_value = 0

            alarm_info, success = get_alarm_info(sql_details, device_info["device_id"], check_value, alarm_code)
            if success == 0:
                return 205

            if len(alarm_info) == 0:
                for alarm in alarm_master:

                    if not alarm_master[alarm]["channel_specific"]:
                        alarm_id = add_alarm(sql_details, device_info["device_id"], 0, alarm,
                                             alarm_master[alarm]["name"], 0, time, tag)
                        if alarm_id is not 0 and int(alarm_code) == alarm:

                            if update_alarm(sql_details, device_info['device_id'], alarm, 0, 0, time) == 0:
                                return 206

                            if print_json(sql_details,tag, time, alarm_code, 0, 1) == 0:
                                if add_transaction(sql_details, time, device_info['device_id'], alarm_id, 0, alarm_code,
                                                   alarm_master[alarm]["name"], 0, 0) == 0:
                                    return 207

                            else:
                                if add_transaction(sql_details, time, device_info['device_id'], alarm_id, 0, alarm_code,
                                                   alarm_master[alarm]["name"], 0, 1) == 0:
                                    return 207

                        elif alarm_id == 0:
                            return 208

                    else:
                        for i in range(1, device_info["channel_no"] + 1):
                            alarm_id = add_alarm(sql_details, device_info["device_id"], i, alarm,
                                                 alarm_master[alarm]["name"], 0, time, tag)

                            if alarm_id is not 0 and int(alarm_code) == alarm:
                                if update_alarm(sql_details, device_info['device_id'], alarm, channel_string[i - 1], i,
                                                time) == 0:
                                    return 209
                                if print_json(sql_details, tag, time, alarm_code, i, channel_string[i - 1]) == 0:
                                    if add_transaction(sql_details, time, device_info['device_id'], alarm_id, i,
                                                       alarm_code,
                                                       alarm_master[alarm]["name"], channel_string[i - 1], 0) == 0:
                                        return 210

                                else:
                                    if add_transaction(sql_details, time, device_info['device_id'], alarm_id, i,
                                                       alarm_code,
                                                       alarm_master[alarm]["name"], channel_string[i - 1], 1) == 0:
                                        return 210

                            elif alarm_id == 0:
                                return 211

            else:

                for i in range(1, device_info['channel_no'] + 1):

                    if alarm_master[int(alarm_code)]["channel_specific"]:

                        alarm_info, success = get_alarm_info(sql_details, device_info['device_id'], i, alarm_code)
                        if success == 0:
                            return 212
                        alarm_info = alarm_info[0]

                        if alarm_info['alarm_state'] != int(channel_string[i - 1]):
                            if update_alarm(sql_details, device_info['device_id'], alarm_code, channel_string[i - 1], i,
                                            time) == 0:
                                return 213

                            if print_json(sql_details, tag, time, alarm_code, i, channel_string[i - 1]) == 0:
                                if add_transaction(sql_details, time, device_info['device_id'], alarm_info['alarm_id'],
                                                   i,
                                                   alarm_code,
                                                   alarm_master[alarm_code]["name"], channel_string[i - 1], 0) == 0:
                                    return 214

                            else:
                                if add_transaction(sql_details, time, device_info['device_id'], alarm_info['alarm_id'],
                                                   i,
                                                   alarm_code,
                                                   alarm_master[alarm_code]["name"], channel_string[i - 1], 1) == 0:
                                    return 214

                    else:

                        alarm_info, success = get_alarm_info(sql_details, device_info['device_id'], 0, alarm_code)
                        if success == 0:
                            return 215
                        alarm_info = alarm_info[0]

                        if update_alarm(sql_details, device_info['device_id'], alarm_code, 0, 0,
                                        time) == 0:
                            # TODO:finalize what to do for non channel specific alarms, whether to give alarm state 1
                            return 216
                        if print_json(sql_details, tag, time, alarm_code, 0, 1) == 0:
                            if add_transaction(sql_details, time, device_info['device_id'], alarm_info['alarm_id'], 0,
                                               alarm_code,
                                               alarm_master[alarm_code]["name"], 0, 0) == 0:
                                return 217

                        else:
                            if add_transaction(sql_details, time, device_info['device_id'], alarm_info['alarm_id'], 0,
                                               alarm_code,
                                               alarm_master[alarm_code]["name"], 0, 1) == 0:
                                return 217
                        break
    return 500
