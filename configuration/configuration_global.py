"""
Global configuration of energy management system (EMS)
"""

default_operation_mode=\
    {
        "ID": 0,
        "UEMS" : 1, # EMS is a server or a client, 1 = the ems is a server, 0 = the ems is a client
        "LEMS": 2,  # EMS is a server or a client, 1 = the ems is a server, 0 = the ems is a client
        "Grid_connnected" : 1, # MG is connected to the main grid ?
        "Set_point_tracing_opf" : 1, # Operation mode of short term operation， 0 = non set point tracing, >0 is under set-point tracing mode
        "Set_point_tracing_ed": 1,  # Operation mode of middle term operation ;0 = non set point tracing, >0 is under set-point tracing mode
        "Set_point_tracing_uc": 1,  # Operation mode of long term operation; 0 = non set point tracing, >0 is under set-point tracing mode
    }

default_command = \
    {
        "ON": 1,
        "OFF": 0,
        "DEV_AVA": 1,
        "DEV_NON_AVA": 0,
        "TRACING": 1,
        "NON_TRACING": 0,
        "CRITICAL": 1,
        "NON_CRITICAL": 0,
        "PV":1,
        "WP":2,
        "MG": {
            "DC_VOL_MAX": 400.0,
            "DC_VOL_MIN": 360.0,
            "AC_VOL_MAX": 250.0,
            "AC_VOL_MIN": 210.0,
            "AC_FREQ_MAX": 50.5,
            "AC_FREQ_MIN": 49.5,
            "VDC_NORMAL": 380,
            "VAC_NORMAL": 230,
            "FREQ_NOMINAL": 50,
            "DELTA_VDC_MAX_STEP": 0.2,
            "POWER_BALANCE": 1,# The power balancing standard
        }
    }

default_eps = \
    {
        "POWER_BALANCE": 1,
        "Penalty_bic":0.01, # The penalty factor for bi-directional power flow
        "Penalty_uc":0.1,
        "Penalty_ed":0.01,
        "Penalty_opf":0.01,
    }

default_sequence=\
    {
        "UG":0,
        "DG":1,
        "PV":1,
        "WP":2,
        "CRI":0,
        "NON_CRI":1,
    }

default_stochastic=\
    {
        "INJECTION":0.1,
        "DG":0.001,
        "PV":0.0001,
    }