import socketserver

def make_log(string):
    string += "\n"
    with open("log.txt", "a") as f:
        f.write(string)


def get_alarm_list(alarm_int):
    return str(bin(alarm_int))[2:].zfill(32)
    

def print_data(channel_int, date_time, alarm_type, domain, channel_string, extra_data, ip, data):
    make_log("-----------------------------")
    print("-----------------------------")
    make_log(data)
    print(data)
    make_log("time : " + date_time)
    print("time : " + date_time)
    make_log("Alarm code : " + str(alarm_type))
    print("Alarm code : " + str(alarm_type))
    make_log("DVR IP : " + ip)
    print("DVR IP : " + ip)
    make_log("channel info : " + channel_string)
    print("channel info : " + channel_string)
    make_log("Domain : " + domain)
    print("Domain : " + domain)
    make_log("Extra data : " + extra_data)
    print("Extra data : " + extra_data)
    make_log("channel int : " + channel_int)
    print("channel int : " + channel_int)


def handle_data(data, dvr_ip):
    alarm_type = data[12]
    extra_data = data[17]
    # print(alarm_type, extra_data)
    str_data = str(data)[1:].replace("'", "")
    str_data1, str_data2 = str_data.split("alarm channel:")
    # print(str_data1)

    alarm_channel, domain, time = str_data2.split("\\r\\n")[:3]
    channel_string = get_alarm_list(int(alarm_channel))
    domain = domain.split(':')[1]
    time = time.replace('Time:', '')
    print_data(alarm_channel, time, str(alarm_type), domain, channel_string, str(extra_data), dvr_ip, str(data))


class MyTCPHandler(socketserver.BaseRequestHandler):


    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024)
        # print("{} wrote:".format(self.client_address[0]))

        handle_data(self.data, self.client_address[0])


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 5001

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
