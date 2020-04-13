
alarm_master = {
    6: {
        "name": "no hdd",
        "channel_specific": False
    },
    2: {
        "name": "motion detect",
        "channel_specific": True
    },
    4: {
        "name": "tampering",
        "channel_specific": True
    },
    3: {
        "name": "video loss",
        "channel_specific": True
    }
}

log_dir = "/data/log/"  # todo: change while making docker
from os import getcwd
config_dir = '/data'  # todo: change while making docker


error_code = {

}