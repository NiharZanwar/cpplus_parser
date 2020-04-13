from sql_functions import *


from datetime import datetime
# import time
#
sql_details1 = get_sql_details()
# time_now = time.time()
result = process_data2(sql_details1, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 6, 123456,
                        '00000000000000000000000000001101', '192.168.1.11', 'uyuy')
# print(time.time() - time_now)
print(result)
# process_data2(sql_details, time, alarm_code, tag, channel_string, dvr_ip, data):