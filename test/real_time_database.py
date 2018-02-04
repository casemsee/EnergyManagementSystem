"""
The test of real time information
"""
from configuration.configuration_database import rtc_local
from database_management.database_functions import db_session
import time
from modelling.database.database_format import RMDBData
from datetime import datetime


def run(*args):
    """
    real time information query function
    :param args:
    :return:
    """
    session = args[0]
    Target_time = args[1]

    row = session.query(RMDBData).filter_by(datetime1=Target_time).first()
    exitence = 0
    if row != None:
        DC_PD = row.LOAD_DC_CT_POW
        NDC_PD = row.LOAD_DC_NCT_POW

        AC_PD = row.LOAD_AC3P_CT_ACTPOW
        AC_QD = row.LOAD_AC3P_CT_REACTPOW

        NAC_PD = row.LOAD_AC3P_NCT_ACTPOW
        NAC_QD = row.LOAD_AC3P_NCT_REACTPOW
        if row.PV0_1_POW != None:
            PV_PG = row.PV0_1_POW
        else:
            PV_PG = 0
        if row.PV0_2_POW != None:
            PV_PG += row.PV0_2_POW
        if row.PV0_3_POW != None:
            PV_PG += row.PV0_3_POW

        if row.PV1_1_POW != None:
            PV_PG += row.PV1_1_POW
        if row.PV1_2_POW != None:
            PV_PG += row.PV1_2_POW
        if row.PV1_3_POW != None:
            PV_PG += row.PV1_3_POW

        WP_PG = row.WT_POW
        exitence = 0
    else:
        DC_PD = 0
        NDC_PD = 0

        AC_PD = 0
        AC_QD = 0

        NAC_PD = 0
        NAC_QD = 0

        PV_PG = 0
        WP_PG = 0
        exitence = 1
    return AC_PD, AC_QD, NAC_PD, NAC_QD, DC_PD, NDC_PD, PV_PG, WP_PG, exitence


if __name__ == "__main__":
    Session = db_session(rtc_local)
    session = Session()
    t = '2018-02-01 12:53:43'
    test_time = time.mktime(time.strptime(t, "%Y-%m-%d %H:%M:%S"))
    target_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(test_time))
    (AC_PD, AC_QD, NAC_PD, NAC_QD, DC_PD, NDC_PD, PV_PG, WP_PG, exitence) = run(session, target_time)
    print(exitence)
