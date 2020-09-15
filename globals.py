
alarm_master = {
    6: {
        "eventcode":"CHF001",
        "name": "no hdd",
        "channel_specific": False
    },
    # 2: {
    #     "eventcode": "CHF001",
    #     "name": "motion detect",
    #     "channel_specific": True
    # },
    4: {
       "error_code":"CCB",
       "ok_code":"CCO",
       "name": "tampering/mask",
        "channel_specific": True
    },
    3: {
        "error_code":"CNV",
        "ok_code":"CNO",
        "name": "video loss",
        "channel_specific": True
    }
}

log_dir = "/logs"
config_dir = '/config'
