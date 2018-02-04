"""
Configuration file of local databases and network databases
Five databases which are required for the energy management system
1) energy_trading_plan, for the energy trading with other MGs
2) scheduling_plan, for the scheduling data of local energy resources
3) forecasting_result, for the forecasting results of each operation process
4) resource_manager, to store the measurement information
5) weather_station, to store the history data of weather station
6) history_data, to store the history operation data
"""

energy_trading_plan = \
    {
        "user_name": 'uems',
        "password": '2',
        "ip_address": 'localhost',
        "db_name": 'microgrid_db'
    }

scheduling_plan = \
    {
        "user_name": 'uems',
        "password": '2',
        "ip_address": 'localhost',
        "db_name": 'microgrid_db'
    }

forecasting_result = \
    {
        "user_name": 'lems',
        "password": '3',
        "ip_address": 'localhost',
        "db_name": 'load_profile'
    }

history_data = \
    {
        "user_name": 'lems',
        "password": '3',
        "ip_address": 'localhost',
        "db_name": 'history_data'
    }

weather_station = \
    {
        "user_name": 'lems',
        "password": '3',
        "ip_address": 'localhost',
        "db_name": 'weather_station'
    }

resource_manager = \
    {
        "user_name": 'lems',
        "password": '3',
        "ip_address": 'localhost',
        "db_name": 'microgrid_db'
    }

scheduling_plan_local = \
    {
        "user_name": 'root',
        "password": '1',
        "ip_address": 'localhost',
        "db_name": 'microgrid_db_local'
    }
# The resource manager
rtc_local = \
    {
        "user_name": 'root',
        "password": '1',
        "ip_address": 'localhost',
        "db_name": 'Module2'
    }
