"""
Simulation of real time energy management
The modelling of resource manager is applied here
The real time operation will be triggered every 5 seconds
1) The load profile is generated using the simulated profile
2) The SOC of energy storage system will be updated
3) The status of
"""

from modelling.database.database_format import resource_management, one_minute_history_data,db_short_term
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


def measurement_data(model, session, t0):
    """
    History database query function for real time simulation
    :param history data:
    :param session: operational database session
    :param t0: operational time of real time operation
    :return: updated real time models
    """
    t0 = int(t0 - t0 % default_time["Time_step_rtc"])
    Target_time = int((t0 - default_time["Base_time"]) / default_time["Time_step_opf"])

    if session.query(resource_management).filter(TIME_STAMP=t0).count() == 0:
        blank_row = blank_history_result(t0)
        session.add(blank_row)
        session.commit()

    row = session.query(resource_management).filter_by(TIME_STAMP=t0).first()

    row_source = session_source.query(one_minute_history_data).filter_by(TIME_STAMP=Target_time).first()
    # The disturbance of
    row.AC_PD = int(row_source.AC_PD * model["Load_ac"]["PMAX"] * (1 - default_stochastic["INJECTION"] + 2 * default_stochastic["INJECTION"]*random.random()))
    row.NAC_PD = int(row_source.NAC_PD * model["Load_nac"]["PMAX"] * (1 - default_stochastic["INJECTION"] + 2 * default_stochastic["INJECTION"]*random.random()))
    row.DC_PD = int(row_source.DC_PD * model["Load_dc"]["PMAX"] * (1 - default_stochastic["INJECTION"] + 2 * default_stochastic["INJECTION"]*random.random()))
    row.NDC_PD = int(row_source.NDC_PD * model["Load_ndc"]["PMAX"] * (1 - default_stochastic["INJECTION"] + 2 * default_stochastic["INJECTION"]*random.random()))
    row.PV_PG = int(row_source.PV_PG * model["PV"]["PMAX"]  * (1 - default_stochastic["INJECTION"] + 2 * default_stochastic["INJECTION"]*random.random()))
    row.WP_PG = int(row_source.WP_PG * model["WP"]["PMAX"]  * (1 - default_stochastic["INJECTION"] + 2 * default_stochastic["INJECTION"]*random.random()))

    row.BAT_SOC = model["ESS"]["SOC"]
    # Random generation of generator status
    if random.random() > 0.01:
        row.DG_STATUS = 1
        model["DG"]["STATUS"] = 1
    else:
        row.DG_STATUS = 0
        model["DG"]["STATUS"] = 0

    if random.random() > 0.01:
        row.UG_STATUS = 1
        model["UG"]["STATUS"] = 1
    else:
        row.UG_STATUS = 0
        model["UG"]["STATUS"] = 0

    session.commit()

    model["Load_ac"]["PD"] = int(row_source.AC_PD * model["Load_ac"]["PMAX"])
    model["Load_nac"]["PD"] = int(row_source.NAC_PD * model["Load_ac"]["PMAX"])
    model["Load_dc"]["PD"] = int(row_source.DC_PD * model["Load_ac"]["PMAX"])
    model["Load_ndc"]["PD"] = int(row_source.NDC_PD * model["Load_ac"]["PMAX"])
    model["PV"]["PG"] = int(row_source.PV_PG * model["Load_ac"]["PMAX"])
    model["WP"]["PG"] = int(row_source.WP_PG * model["Load_ac"]["PMAX"])
    model["ESS"]["SOC"] = row.BAT_SOC

    # Further information might be updated.
    # 1) Battery status
    # 2) BIC status

    return model


def real_time_simulation(model, session, t0, logger):
    """
    Real time simulation for the
    :param model:
    :param session: real time operation database
    :param t0: real time operation time
    :param logger: logger system of real time operation
    :return: updated model and store the result in RTC database
    """
    Target_time = int(t0 - t0 % default_time["Time_step_rtc"])
    row = session(db_short_term).filter(TIME_STAMP = Target_time).first()
    row.UG_PG = model["UG"]["COMMAND_PG"]
    row.UG_QG = model["UG"]["COMMAND_QG"]
    row.DG_PG = model["DG"]["COMMAND_PG"]
    row.DG_QG = model["DG"]["COMMAND_QG"]

    row.BIC_PG = row.AC_PD + row.NAC_PD - model["UG"]["COMMAND_PG"] - model["DG"]["COMMAND_PG"]
    if row.BIC_PG > model["BIC"]["SMAX"] or row.BIC_PG < -model["BIC"]["SMAX"]:
        logger.error("BIC is over current")
    row.BIC_QG = row.AC_QD + row.NAC_QD - model["UG"]["COMMAND_QG"] - model["UG"]["COMMAND_QG"]

    row.BAT_PG = row.DC_PD + row.NDC_PD - model["PMG"] - row.BIC_PG - model["PV"]["PG"] - model["WP"]["PG"]

    if row.BAT_PG > model["ESS"]["PMAX_DIS"] or row.BAT_PG < -model["ESS"]["PMAX_CH"]:
        logger.error("ESS is over current")

    if row.BAT_PG > 0:
        row.BAT_SOC = row.BAT_SOC - row.BAT_PG * default_time["Time_step_rtc"] / model["ESS"]["EFF_DIS"]
    else:
        row.BAT_SOC = row.BAT_SOC - row.BAT_PG * model["ESS"]["EFF_CH"] * default_time["Time_step_rtc"]

    session.commit()


def scheduling_data(model, session, t0):
    """
    Operation database result inquiry
    This function will inquiry the optimal power flow database
    :param session: short_term_scheduling database session
    :return:
    """
    Target_time = int(t0 - t0%default_time["Time_step_rtc"])
    if session.query(db_short_term).filter(TIME_STAMP = Target_time).count() != 0:
        row = session(db_short_term).filter(TIME_STAMP = Target_time).first()
        if row.DG_STATUS>0 and model["DG"]["STATUS"]>0:
            model["DG"]["STATUS"] = 1
            model["DG"]["COMMAND_PG"] = row.DG_PG
            model["DG"]["COMMAND_QG"] = row.DG_QG
        else:
            model["DG"]["STATUS"] = 0
            model["DG"]["COMMAND_PG"] = 0
            model["DG"]["COMMAND_QG"] = 0
        if row.UG_STATUS>0 and  model["UG"]["STATUS"]>0:
            model["UG"]["STATUS"] = 1
            model["UG"]["COMMAND_PG"] = row.UG_PG
            model["UG"]["COMMAND_QG"] = row.UG_QG
        else:
            model["UG"]["STATUS"] = 0
            model["UG"]["COMMAND_PG"] = 0
            model["UG"]["COMMAND_QG"] = 0

        if row.BIC_PG>0:
            model["BIC"]["COMMAND_AC2DC"] = row.BIC_PG
        else:
            model["BIC"]["COMMAND_DC2AC"] = -row.BIC_PG

        model["BIC"]["COMMAND_Q"] = row.BIC_QG
        model["ESS"]["COMMAND_PG"] = row.BAT_PG

        model["PMG"] = row.PMG
        model["V_DC"] = row.V_DC

        if row.PV_CURT > 0:
            model["PV"]["PG"] -= row.PV_CURT

        if row.PV_CURT > 0:
            model["WP"]["PG"] -= row.WP_CURT

        if row.AC_SHED >0 :
            model["Load_ac"]["PD"] = 0
        if row.NAC_SHED > 0:
            model["Load_nac"]["PD"] = 0
        if row.DC_SHED >0:
            model["Load_dc"]["PD"] = 0
        if row.NDC_SHED >0:
            model["Load_ndc"]["PD"] = 0

    return model

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
