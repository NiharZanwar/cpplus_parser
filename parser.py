import socketserver

from sql_functions import *
from globals import log_dir, error_code, config_dir
from datetime import datetime
from time import sleep


def make_log(string):
    string += "\n"
    with open(log_dir + "log.txt", "a") as f:
        f.write(string)


def get_alarm_list(alarm_int):
    return str(bin(alarm_int))[2:].zfill(32)
    

def print_data(channel_int, date_time, alarm_type, domain, channel_string, extra_data, ip, data, sql_result):
    log_string = "----------------------\n"

    log_string += "time : " + date_time + '\n'
    log_string += "Alarm code : " + str(alarm_type) + '\n'
    log_string += "DVR IP : " + ip + '\n'
    log_string += "channel info : " + channel_string + '\n'
    log_string += "Domain : " + domain + '\n'
    log_string += "Extra data : " + extra_data + '\n'
    log_string += "channel int : " + channel_int + '\n'
    log_string += "result : " + str(sql_result) + '\n'


def handle_data(data, dvr_ip):
    alarm_type = data[12]
    extra_data = data[17]
    str_data = str(data)[1:].replace("'", "")
    str_data1, str_data2 = str_data.split("alarm channel:")

    alarm_channel, domain, time = str_data2.split("\\r\\n")[:3]
    channel_string = get_alarm_list(int(alarm_channel))
    domain = domain.split(':')[1]
    time = time.replace('Time:', '')
    sql_details = get_sql_details()

    config = get_config(config_dir)
    if config['mode']['consider_ip_as_tag'] == 1:
        domain = str(dvr_ip)

    result = process_data2(sql_details, time, int(alarm_type), domain, channel_string,
                           dvr_ip, str_data)
    print(result)
    print_data(alarm_channel, time, str(alarm_type), domain, channel_string, str(extra_data), dvr_ip, str(data), result)


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024)
        handle_data(self.data, self.client_address[0])
        print(self.client_address[0])
        print(self.data)


if __name__ == "__main__":

    while True:
        sql_details = get_sql_details()
        if sql_details == 0:
            log_error("could not find sql details file while initializing. check if config file exists in {}"
                      .format(config_dir))
            print("config file not present or some error with config file")
        else:
            connection = sql_connection(sql_details)
            if connection == 0:

                log_error("could not make connection to database while initializing server")
                print("could not make connection to database while initializing server")
            else:
                make_log("initializing success")
                print("initializing success")
                break
        sleep(5)

    HOST, PORT = "0.0.0.0", 5001

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
