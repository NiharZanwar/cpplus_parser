# Alarm Algorithm

Check for incoming alarm, if domain name is -

* is present as a tag value, check the `active_status` if it is 
  * 1 - then get device ID and and no of channels info and check if in `alarm_table` there is a entry with `device_id` , `channel_no=1`, if
    * yes - change status of alarm detected
    * no - create all entries in `alarm_table`, then change status of alarm detected and add entry to `txn_table`.
  * 0 - do nothing, and update last_updated_time
* not present, then create a entry in `device_table` with `active_status=0` and `channel_no=NULL`

# Functions required

```pyt
add_device(tag, active_status, ip, rcvd_str, create_dt)
get_device_info(tag)
update_dt(tag, date_time)

add_alarm(device_id, channel_no, alarm_code, alarm_name, alarm_status, create_dt)
get_alarm_info(device_id, channel_no, alarm_code)
add_transaction(date_time, device_id, alarm_id, channel_no, alarm_code, alarm_name, alarm_state, add_info)
```

