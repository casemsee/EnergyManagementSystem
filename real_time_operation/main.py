"""
Simulation of real time energy management
The modelling of resource manager is applied here
The real time operation will be triggered every 5 seconds
1) The load profile is generated using the simulated profile
2) The SOC of energy storage system will be updated
3) The status of
"""

from modelling.database.database_format import resource_management, one_minute_history_data,db_short_term,db_real_time
import random
from configuration.configuration_database import history_data
from sqlalchemy import create_engine, and_  # Import database
from sqlalchemy.orm import sessionmaker
from configuration.configuration_time_line import default_time
from configuration.configuration_global import default_stochastic
db_str = 'mysql+pymysql://' + history_data["user_name"] + ':' + history_data["password"] + '@' + history_data[
    "ip_address"] + '/' + history_data["db_name"]

engine = create_engine(db_str, echo=False)
Session = sessionmaker(bind=engine)
session_source = Session()


def measurement_data(microgrid, session, t0):
    """
    History database query function for real time simulation
    :param history data:
    :param session: operational database session
    :param t0: operational time of real time operation
    :return: updated real time models
    """
    t0 = int(t0 - t0 % default_time["Time_step_rtc"])
    Target_time = int((t0 - default_time["Base_time"]) / default_time["Time_step_opf"])

    if session.query(resource_management).filter(resource_management.TIME_STAMP==t0).count() == 0:
        blank_row = blank_history_result(t0)
        session.add(blank_row)
        session.commit()

    row = session.query(resource_management).filter_by(TIME_STAMP=t0).first()

    row_source = session_source.query(one_minute_history_data).filter_by(TIME_STAMP=Target_time).first()# By using the default data to test the system
    # The disturbance of
    row.AC_PD = int(row_source.AC_PD * microgrid["Load_ac"]["PMAX"] * (1 - default_stochastic["INJECTION"] + 2 * default_stochastic["INJECTION"]*random.random()))
    row.NAC_PD = int(row_source.NAC_PD * microgrid["Load_nac"]["PMAX"] * (1 - default_stochastic["INJECTION"] + 2 * default_stochastic["INJECTION"]*random.random()))
    row.DC_PD = int(row_source.DC_PD * microgrid["Load_dc"]["PMAX"] * (1 - default_stochastic["INJECTION"] + 2 * default_stochastic["INJECTION"]*random.random()))
    row.NDC_PD = int(row_source.NDC_PD * microgrid["Load_ndc"]["PMAX"] * (1 - default_stochastic["INJECTION"] + 2 * default_stochastic["INJECTION"]*random.random()))
    row.PV_PG = int(row_source.PV_PG * microgrid["PV"]["PMAX"]  * (1 - default_stochastic["INJECTION"] + 2 * default_stochastic["INJECTION"]*random.random()))
    row.WP_PG = int(row_source.WP_PG * microgrid["WP"]["PMAX"]  * (1 - default_stochastic["INJECTION"] + 2 * default_stochastic["INJECTION"]*random.random()))

    # update SOC according to the operation data or the previous data
    # if the operation data exits

    if session.query(db_real_time).filter(db_real_time.TIME_STAMP == t0 - default_time["Time_step_rtc"]).count() != 0:
        row_target = session.query(db_real_time).filter_by( TIME_STAMP = t0 - default_time["Time_step_rtc"]).first()
        row.BAT_SOC = row_target.BAT_SOC
    else:
        row.BAT_SOC = microgrid["ESS"]["SOC"]
    # Random generation of generator status
    if random.random() > 0.01:
        row.DG_STATUS = 1
        microgrid["DG"]["STATUS"] = 1
    else:
        row.DG_STATUS = 0
        microgrid["DG"]["STATUS"] = 0

    if random.random() > 0.01:
        row.UG_STATUS = 1
        microgrid["UG"]["STATUS"] = 1
    else:
        row.UG_STATUS = 0
        microgrid["UG"]["STATUS"] = 0

    session.commit()

    microgrid["Load_ac"]["PD"] = int(row_source.AC_PD * microgrid["Load_ac"]["PMAX"])
    microgrid["Load_nac"]["PD"] = int(row_source.NAC_PD * microgrid["Load_ac"]["PMAX"])
    microgrid["Load_dc"]["PD"] = int(row_source.DC_PD * microgrid["Load_ac"]["PMAX"])
    microgrid["Load_ndc"]["PD"] = int(row_source.NDC_PD * microgrid["Load_ac"]["PMAX"])
    microgrid["PV"]["PG"] = int(row_source.PV_PG * microgrid["Load_ac"]["PMAX"])
    microgrid["WP"]["PG"] = int(row_source.WP_PG * microgrid["Load_ac"]["PMAX"])
    microgrid["ESS"]["SOC"] = row.BAT_SOC

    # Further information might be updated.
    # 1) Battery status
    # 2) BIC status

    return microgrid


def real_time_simulation(microgrid, session, t0, logger):
    """
    Real time simulation for the
    :param model:
    :param session: real time operation database
    :param t0: real time operation time
    :param logger: logger system of real time operation
    :return: updated model and store the result in RTC database
    """
    Target_time = int(t0 - t0 % default_time["Time_step_rtc"])

    if session.query(db_real_time).filter(db_real_time.TIME_STAMP==Target_time).count() == 0:
        blank_row = blank_real_time_result(Target_time)
        session.add(blank_row)
        session.commit()
    row = session.query(db_real_time).filter(db_real_time.TIME_STAMP == Target_time).first()
    # record the measurement information
    row.AC_PD = microgrid["Load_ac"]["PD"]
    row.NAC_PD = microgrid["Load_nac"]["PD"]
    row.DC_PD = microgrid["Load_dc"]["PD"]
    row.NDC_PD = microgrid["Load_ndc"]["PD"]
    row.PV_PG = microgrid["PV"]["PG"]
    row.WP_PG = microgrid["WP"]["PG"]
    # record the scheduling plan
    row.UG_PG = microgrid["UG"]["COMMAND_PG"]
    row.UG_QG = microgrid["UG"]["COMMAND_QG"]
    row.DG_PG = microgrid["DG"]["COMMAND_PG"]
    row.DG_QG = microgrid["DG"]["COMMAND_QG"]
    row.PMG = microgrid["PMG"]
    row.BIC_PG = row.AC_PD + row.NAC_PD - row.UG_PG - row.DG_PG

    if row.BIC_PG > microgrid["BIC"]["SMAX"] or row.BIC_PG < -microgrid["BIC"]["SMAX"]:
        logger.error("BIC is over current")
    row.BIC_QG = row.AC_QD + row.NAC_QD - row.UG_QG - row.DG_QG

    row.BAT_PG = row.DC_PD + row.NDC_PD - row.PMG + row.BIC_PG - row.PV_PG - row.WP_PG

    if row.BAT_PG > microgrid["ESS"]["PMAX_DIS"] or row.BAT_PG < - microgrid["ESS"]["PMAX_CH"]:
        logger.error("ESS is over current")

    if row.BAT_PG > 0:
        row.BAT_SOC = microgrid["ESS"]["SOC"] - row.BAT_PG * default_time["Time_step_rtc"] / microgrid["ESS"]["EFF_DIS"]/microgrid["ESS"]["CAP"]/3600
    else:
        row.BAT_SOC = microgrid["ESS"]["SOC"] - row.BAT_PG * microgrid["ESS"]["EFF_CH"] * default_time["Time_step_rtc"]/microgrid["ESS"]["CAP"]/3600

    session.commit()


def scheduling_data(microgrid, session, t0):
    """
    Operation database result inquiry
    This function will inquiry the optimal power flow database
    :param session: short_term_scheduling database session
    :return:
    """
    Target_time = int(t0 - t0%default_time["Time_step_rtc"])
    if session.query(db_short_term).filter(db_short_term.TIME_STAMP == Target_time).count() != 0: # If the scheduling plan exists!
        row = session(db_short_term).filter(TIME_STAMP = Target_time).first()
        if row.DG_STATUS>0 and microgrid["DG"]["STATUS"]>0:
            microgrid["DG"]["STATUS"] = 1
            microgrid["DG"]["COMMAND_PG"] = row.DG_PG
            microgrid["DG"]["COMMAND_QG"] = row.DG_QG
        else:
            microgrid["DG"]["STATUS"] = 0
            microgrid["DG"]["COMMAND_PG"] = 0
            microgrid["DG"]["COMMAND_QG"] = 0
        if row.UG_STATUS>0 and  microgrid["UG"]["STATUS"]>0:
            microgrid["UG"]["STATUS"] = 1
            microgrid["UG"]["COMMAND_PG"] = row.UG_PG
            microgrid["UG"]["COMMAND_QG"] = row.UG_QG
        else:
            microgrid["UG"]["STATUS"] = 0
            microgrid["UG"]["COMMAND_PG"] = 0
            microgrid["UG"]["COMMAND_QG"] = 0

        if row.BIC_PG>0:
            microgrid["BIC"]["COMMAND_AC2DC"] = row.BIC_PG
        else:
            microgrid["BIC"]["COMMAND_DC2AC"] = -row.BIC_PG

        microgrid["BIC"]["COMMAND_Q"] = row.BIC_QG
        microgrid["ESS"]["COMMAND_PG"] = row.BAT_PG

        microgrid["PMG"] = row.PMG
        microgrid["V_DC"] = row.V_DC

        if row.PV_CURT > 0:
            microgrid["PV"]["PG"] -= row.PV_CURT

        if row.PV_CURT > 0:
            microgrid["WP"]["PG"] -= row.WP_CURT

        if row.AC_SHED >0 :
            microgrid["Load_ac"]["PD"] = 0
        if row.NAC_SHED > 0:
            microgrid["Load_nac"]["PD"] = 0
        if row.DC_SHED >0:
            microgrid["Load_dc"]["PD"] = 0
        if row.NDC_SHED >0:
            microgrid["Load_ndc"]["PD"] = 0

    return microgrid

def database_management(session, t0):
    # Manage the resource manager database and real-time-operation database
    session.query(db_real_time).filter(default_time.TIME_STAMP < t0 - 3600).delete()
    session.query(resource_management).filter(resource_management.TIME_STAMP < t0 - 3600).delete()
    session.commit()

def blank_history_result(Target_time):
    """
    Default resource management database
    :param Target_time:
    :return: all zeros
    """
    default_result = resource_management \
        (
            TIME_STAMP=Target_time,
            AC_PD=0,
            AC_QD=0,
            NAC_PD=0,
            NAC_QD=0,
            DC_PD=0,
            NDC_PD=0,
            # Renewable energy group.
            PV_PG=0,
            WP_PG=0,
            # DG group
            DG_STATUS=0,
            DG_PG=0,
            DG_QG=0,
            # UG group
            UG_STATUS=0,
            UG_PG=0,
            UG_QG=0,
            # BIC group
            BIC_PG=0,
            BIC_QG=0,
            # Battery group
            BAT_PG=0,
            BAT_SOC=0,
            # Coordination group
            PMG=0,
            V_DC=0
        )

    return default_result

def blank_real_time_result(Target_time):
    """
    Default resource management database
    :param Target_time:
    :return: all zeros
    """
    default_result = db_real_time \
        (
            TIME_STAMP=Target_time,
            AC_PD=0,
            AC_QD=0,
            NAC_PD=0,
            NAC_QD=0,
            DC_PD=0,
            NDC_PD=0,
            # Renewable energy group.
            PV_PG=0,
            WP_PG=0,
            # DG group
            DG_STATUS=0,
            DG_PG=0,
            DG_QG=0,
            # UG group
            UG_STATUS=0,
            UG_PG=0,
            UG_QG=0,
            # BIC group
            BIC_PG=0,
            BIC_QG=0,
            # Battery group
            BAT_PG=0,
            BAT_SOC=0,
            # Coordination group
            PMG=0,
            V_DC=0,
            # Operational cost
            COST=0,
        )

    return default_result