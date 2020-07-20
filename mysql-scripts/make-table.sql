
create table cpplus_device_dvr
(
    device_id      int auto_increment
        primary key,
    ip             varchar(45)   null,
    mac            varchar(45)   null,
    serial_no      varchar(60)   null,
    model_no       varchar(45)   null,
    tag            varchar(45)   not null,
    parse_type     varchar(45)   null,
    server_port    int           null,
    rcvd_str       varchar(1024) null,
    channel_no     int           null,
    last_update_dt datetime      null,
    create_dt      datetime      null,
    is_active      tinyint       null,
    constraint tag_UNIQUE
        unique (tag)
);

create table cpplus_alarm_dvr
(
    alarm_id       int auto_increment
        primary key,
    device_id      int         not null,
    channel_no     int         null,
    alarm_code     varchar(45) null,
    alarm_name     varchar(45) null,
    alarm_state    int         null,
    add_info       varchar(45) null,
    create_dt      datetime    null,
    last_update_dt datetime    null,
    constraint device_id
        foreign key (device_id) references cpplus_device_dvr (device_id)
);

create index device_id_idx
    on cpplus_alarm_dvr (device_id);

create table cpplus_txn_dvr
(
    date_time   datetime    not null,
    device_id   int         not null,
    alarm_id    int         not null,
    channel_no  int         not null,
    alarm_code  varchar(45) not null,
    alarm_name  varchar(45) null,
    alarm_state int         null,
    add_info    varchar(45) null
);



GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';

FLUSH PRIVILEGES;