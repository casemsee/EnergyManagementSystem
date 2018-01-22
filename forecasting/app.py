"""
Forecasting thread for energy management system. There are three threads in the forecasting,
1) short term forecasting
2) middle term forecasting
3) long term forecasting
"""

from forecasting.short_term_forecasting import short_term_forecasting_pv_history, short_term_forecasting_wp_history, \
    short_term_forecasting_load_ac_history, short_term_forecasting_load_dc_history, short_term_forecasting_load_nac_history, \
    short_term_forecasting_load_ndc_history
from forecasting.mid_term_forecasting import middle_term_forecasting_pv_history, middle_term_forecasting_wp_history, \
    middle_term_forecasting_load_ac_history, middle_term_forecasting_load_dc_history, middle_term_forecasting_load_nac_history, \
    middle_term_forecasting_load_ndc_history
from forecasting.long_term_forecasting import long_term_forecasting_pv_history, long_term_forecasting_wp_history, \
    long_term_forecasting_load_ac_history, long_term_forecasting_load_dc_history, long_term_forecasting_load_nac_history, \
    long_term_forecasting_load_ndc_history
from configuration.configuration_time_line import default_look_ahead_time_step
import threading
from utils import Logger
from copy import deepcopy

class ShortTermForecastingThread(threading.Thread):
    """
    Short-term forecasting thread for the short-term operation process
    """
    def __init__(self, session, Target_time, microgrid):
        threading.Thread.__init__(self)
        self.session = session
        self.Target_time = Target_time
        self.microgrid = microgrid
        self.logger = Logger("Short_term_forecasting")
    def run(self):
        self.microgrid = short_term_forecasting(self.session, self.Target_time, self.microgrid, self.logger)

class MiddleTermForecastingThread(threading.Thread):
    """
    Middle-term forecasting thread for the middle-term operation process
    """
    def __init__(self, session, Target_time, microgrid):
        threading.Thread.__init__(self)
        self.session = session
        self.Target_time = Target_time
        self.microgrid = microgrid
        self.logger = Logger("Mid_term_forecasting")
        self.T = default_look_ahead_time_step["Look_ahead_time_ed_time_step"]
    def run(self):
        self.models = mid_term_forecasting(self.session, self.Target_time, self.microgrid, self.logger, self.T)

class LongTermForecastingThread(threading.Thread):
    """
    Long-term forecasting thread for the long-term operation process
    """
    def __init__(self, session, Target_time, microgrid):
        threading.Thread.__init__(self)
        self.session = session
        self.Target_time = Target_time
        self.microgrid = microgrid
        self.logger = Logger("Long_term_forecasting")
        self.T = default_look_ahead_time_step["Look_ahead_time_uc_time_step"]

    def run(self):
        self.microgrid = long_term_forecasting(self.session, self.Target_time, self.microgrid,self.logger, self.T)

def short_term_forecasting(*args):
    """
    Short-term forecasting function, the following functions will be implemented.
    1) PV forecasting
    2) WP forecasting
    3) Critical AC load
    4) Non-critical AC load
    5) Critical DC load
    6) Non-critical DC load
    @date: 22/Jan/2018
    @author: Tianyang Zhao
    :param args: database session, scheduling time and information modelling of microgrid
    :return: information model of microgrid
    """
    session = args[0]
    Target_time = args[1]
    microgrid = deepcopy(args[2])

    logger = args[3]

    if microgrid["PV"]["STATUS"] > 0:
        pv_profile = short_term_forecasting_pv_history(session, Target_time)
        microgrid["PV"]["PG"] = round(microgrid["PV"]["PMAX"] * pv_profile)
    else:
        logger.warning("No PV is connected, set to default value 0!")
        microgrid["PV"]["PG"] = 0

    if microgrid["WP"]["STATUS"] > 0:
        pv_profile = short_term_forecasting_wp_history(session, Target_time)
        microgrid["WP"]["PG"] = round(microgrid["WP"]["PMAX"] * pv_profile)
    else:
        logger.warning("No WP is connected, set to default value 0!")
        microgrid["WP"]["PG"] = 0

    if microgrid["Load_ac"]["STATUS"] > 0:
        load_ac = short_term_forecasting_load_ac_history(session, Target_time)
        microgrid["Load_ac"]["PD"] = round(load_ac * microgrid["Load_ac"]["PMAX"])
    else:
        logger.warning("No critical AC load is connected, set to default value 0!")
        microgrid["Load_ac"]["PD"] = 0

    if microgrid["Load_nac"]["STATUS"] > 0:
        if microgrid["Load_nac"]["STATUS"] > 0:
            load_nac = short_term_forecasting_load_nac_history(session, Target_time)
            microgrid["Load_nac"]["PD"] = round(load_nac * microgrid["Load_nac"]["PMAX"])
        else:
            logger.warning("No non-critical AC load is connected, set to default value 0!")
            microgrid["Load_nac"]["PD"] = 0

    if microgrid["Load_dc"]["STATUS"] > 0:
        load_dc = short_term_forecasting_load_dc_history(session, Target_time)
        microgrid["Load_dc"]["PD"] = round(load_dc * microgrid["Load_dc"]["PMAX"])
    else:
        logger.warning("No critical DC load is connected, set to default value 0!")
        microgrid["Load_dc"]["PD"] = 0

    if microgrid["Load_ndc"]["STATUS"] > 0:
        load_ndc = short_term_forecasting_load_ndc_history(session, Target_time)
        microgrid["Load_ndc"]["PD"] = round(load_ndc * microgrid["Load_ndc"]["PMAX"])
    else:
        logger.warning("No non-critical DC load is connected, set to default value 0!")
        microgrid["Load_ndc"]["PD"] = 0

    return microgrid



def mid_term_forecasting(*args):
    """
    Middle-term forecasting function, the following functions will be implemented.
    1) PV forecasting
    2) WP forecasting
    3) Critical AC load
    4) Non-critical AC load
    5) Critical DC load
    6) Non-critical DC load
    @date: 22/Jan/2018
    @author: Tianyang Zhao
    :param args: database session, scheduling time and information modelling of microgrid, look ahead time step
    :return: information model of microgrid
    """
    session = args[0]
    Target_time = args[1]
    microgrid = deepcopy(args[2])
    T = args[3]

    microgrid["PV"]["PG"] = []
    microgrid["WP"]["PG"] = []
    microgrid["Load_ac"]["PD"] = []
    microgrid["Load_nac"]["PD"] = []
    microgrid["Load_dc"]["PD"] = []
    microgrid["Load_ndc"]["PD"] = []

    pv_profile = middle_term_forecasting_pv_history(session, Target_time)
    wp_profile = middle_term_forecasting_wp_history(session, Target_time)
    load_ac = middle_term_forecasting_load_ac_history(session, Target_time)
    load_nac = middle_term_forecasting_load_nac_history(session, Target_time)
    load_dc = middle_term_forecasting_load_dc_history(session, Target_time)
    load_ndc = middle_term_forecasting_load_ndc_history(session, Target_time)

    for i in range(T):
        # Update the forecasting result of PV
        if microgrid["PV"]["NPV"][i] > 0:
            microgrid["PV"]["PG"].append(round(microgrid["PV"]["PMAX"][i] * pv_profile[i]))
        else:
            microgrid["PV"]["PG"].append(0)

        if microgrid["WP"]["NWP"][i] > 0:
            microgrid["WP"]["PG"].append(round(microgrid["WP"]["PMAX"][i] * wp_profile[i]))
        else:
            microgrid["WP"]["PG"].append(0)

        if microgrid["Load_ac"]["STATUS"][i] > 0:
            microgrid["Load_ac"]["PD"].append(round(load_ac[i] * microgrid["Load_ac"]["PMAX"]))
        else:
            microgrid["Load_ac"]["PD"].append(0)

        if microgrid["Load_nac"]["STATUS"][i] > 0:
            microgrid["Load_nac"]["PD"].append(round(load_nac[i] * microgrid["Load_nac"]["PMAX"]))
        else:
            microgrid["Load_nac"]["PD"].append(0)

        if microgrid["Load_dc"]["STATUS"][i] > 0:
            microgrid["Load_dc"]["PD"].append(round(load_dc[i] * microgrid["Load_dc"]["PMAX"]))
        else:
            microgrid["Load_dc"]["PD"].append(0)

        if microgrid["Load_ndc"]["STATUS"][i] > 0:
            microgrid["Load_ndc"]["PD"].append(round(load_ndc[i] * microgrid["Load_ndc"]["PMAX"]))
        else:
            microgrid["Load_ndc"]["PD"].append(0)

    return microgrid

def long_term_forecasting(*args):
    """
    Long-term forecasting function, the following functions will be implemented.
    1) PV forecasting
    2) WP forecasting
    3) Critical AC load
    4) Non-critical AC load
    5) Critical DC load
    6) Non-critical DC load
    @date: 22/Jan/2018
    @author: Tianyang Zhao
    :param args: database session, scheduling time and information modelling of microgrid, look ahead time step
    :return: information model of microgrid
    """

    session = args[0]
    Target_time = args[1]
    microgrid = deepcopy(args[2])
    T = args[3]

    microgrid["PV"]["PG"] = []
    microgrid["WP"]["PG"] = []
    microgrid["Load_ac"]["PD"] = []
    microgrid["Load_uac"]["PD"] = []
    microgrid["Load_dc"]["PD"] = []
    microgrid["Load_udc"]["PD"] = []
    pv_profile = long_term_forecasting_pv_history(session, Target_time)
    wp_profile = long_term_forecasting_wp_history(session, Target_time)
    load_ac = long_term_forecasting_load_ac_history(session, Target_time)
    load_nac = long_term_forecasting_load_nac_history(session, Target_time)
    load_dc = long_term_forecasting_load_dc_history(session, Target_time)
    load_ndc = long_term_forecasting_load_ndc_history(session, Target_time)

    for i in range(T):
        # Update the forecasting result of PV
        if microgrid["PV"]["NPV"][i] > 0:
            microgrid["PV"]["PG"].append(round(microgrid["PV"]["PMAX"][i] * pv_profile[i]))
        else:
            microgrid["PV"]["PG"].append(0)

        if microgrid["WP"]["NWP"][i] > 0:
            microgrid["WP"]["PG"].append(round(microgrid["WP"]["PMAX"][i] * wp_profile[i]))
        else:
            microgrid["WP"]["PG"].append(0)

        if microgrid["Load_ac"]["STATUS"][i] > 0:
            microgrid["Load_ac"]["PD"].append(round(load_ac[i] * microgrid["Load_ac"]["PMAX"]))
        else:
            microgrid["Load_ac"]["PD"].append(0)

        if microgrid["Load_nac"]["STATUS"][i] > 0:
            microgrid["Load_nac"]["PD"].append(round(load_nac[i] * microgrid["Load_nac"]["PMAX"]))
        else:
            microgrid["Load_nac"]["PD"].append(0)

        if microgrid["Load_dc"]["STATUS"][i] > 0:
            microgrid["Load_dc"]["PD"].append(round(load_dc[i] * microgrid["Load_dc"]["PMAX"]))
        else:
            microgrid["Load_dc"]["PD"].append(0)

        if microgrid["Load_ndc"]["STATUS"][i] > 0:
            microgrid["Load_ndc"]["PD"].append(round(load_ndc[i] * microgrid["Load_ndc"]["PMAX"]))
        else:
            microgrid["Load_ndc"]["PD"].append(0)

    return microgrid