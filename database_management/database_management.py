# Database query and record funtion for universal energy management system
import time
from modelling.database.database_format import db_short_term, db_middle_term, db_long_term

class database_storage_operation():
    # Database operation in universal energy management system
    def default_long_term_operation_data(*args): # All zeros insert
        Target_time = args[0]
        default_result = db_long_term \
            (TIME_STAMP=Target_time,
             AC_PD=0,
             NAC_PD=0,
             DC_PD=0,
             NDC_PD=0,
             PV_PG=0,
             WP_PG=0,
             PRICE=0,
             DG_STATUS=0,
             DG_PG=0,
             UG_STATUS=0,
             UG_PG=0,
             BIC_PG=0,
             BAT_PG=0,
             BAT_SOC=0,
             PMG=0,
             V_DC=0,
             PV_CURT=0,
             WP_CURT=0,
             AC_SHED=0,
             NAC_SHED=0,
             DC_SHED=0,
             NDC_SHED=0,
             COST=0,)
        return default_result

    def default_middle_term_operation_data(*args):
        Target_time = args[0]
        default_result = db_middle_term \
            (TIME_STAMP=Target_time,
             AC_PD=0,
             NAC_PD=0,
             DC_PD=0,
             NDC_PD=0,
             PV_PG=0,
             WP_PG=0,
             PRICE=0,
             DG_STATUS=0,
             DG_PG=0,
             UG_STATUS=0,
             UG_PG=0,
             BIC_PG=0,
             BAT_PG=0,
             BAT_SOC=0,
             PMG=0,
             V_DC=0,
             PV_CURT=0,
             WP_CURT=0,
             AC_SHED=0,
             NAC_SHED=0,
             DC_SHED=0,
             NDC_SHED=0,
             COST=0)
        return default_result

    def default_short_term_operation_data(*args):
        Target_time = args[0]
        default_result = db_short_term \
            (TIME_STAMP=Target_time,
             AC_PD=0,
             AC_QD=0,
             NAC_PD=0,
             NAC_QD=0,
             DC_PD=0,
             NDC_PD=0,
             PV_PG=0,
             WP_PG=0,
             DG_STATUS=0,
             DG_PG=0,
             DG_QG=0,
             UG_STATUS=0,
             UG_PG=0,
             UG_QG=0,
             BIC_PG=0,
             BIC_QG=0,
             BAT_PG=0,
             BAT_SOC=0,
             PMG=0,
             V_DC=0,
             PV_CURT=0,
             WP_CURT=0,
             AC_SHED=0,
             NAC_SHED=0,
             DC_SHED=0,
             NDC_SHED=0,
             COST=0)
        return default_result



    def database_query(input, session):
        # The input information check for the databases
        print(time.time())

    def database_record(*args):
        # The result storage operation for obtained result
        session = args[0]
        model = args[1]
        Target_time = args[2]
        ## control model of UC, ED or OPF
        function = args[3]

        database_target = {"UC": db_long_term,
                           "ED": db_middle_term,
                           "OPF": db_short_term}

        if session.query(database_target[function]).filter(database_target[function].TIME_STAMP == Target_time).count() == 0:
            if function == "OPF":
                blank_row = database_storage_operation.default_short_term_operation_data(Target_time)
                session.add(blank_row)
                session.commit()

        if function == "OPF":
            row = session.query(database_target[function]).filter(database_target[function].TIME_STAMP == Target_time).first()
            row.AC_PD = model["Load_ac"]["PD"]
            row.AC_QD = model["Load_ac"]["QD"]
            row.NAC_PD = model["Load_nac"]["PD"]
            row.NAC_QD = model["Load_nac"]["QD"]
            row.DC_PD = model["Load_dc"]["PD"]
            row.NDC_PD = model["Load_ndc"]["PD"]
            row.PV_PG = model["PV"]["PG"]
            row.WP_PG = model["WP"]["PG"]
            row.DG_STATUS = model["DG"]["GEN_STATUS"]
            row.DG_PG = model["DG"]["COMMAND_PG"]
            row.DG_QG = model["DG"]["COMMAND_QG"]
            row.UG_STATUS = model["UG"]["GEN_STATUS"]
            row.UG_PG = model["UG"]["COMMAND_PG"]
            row.UG_QG = model["UG"]["COMMAND_QG"]
            row.BIC_PG = model["BIC"]["COMMAND_AC2DC"] - model["BIC"]["COMMAND_DC2AC"]
            row.BIC_QG = model["BIC"]["COMMAND_Q"]
            row.BAT_PG = model["ESS"]["COMMAND_PG"]
            row.BAT_SOC = model["ESS"]["SOC"]
            row.PMG = model["PMG"]
            row.V_DC = model["V_DC"]
            row.PV_CURT = model["PV"]["COMMAND_CURT"]
            row.WP_CURT = model["WP"]["COMMAND_CURT"]
            row.AC_SHED = model["Load_ac"]["COMMAND_SHED"]
            row.NAC_SHED = model["Load_nac"]["COMMAND_SHED"]
            row.DC_SHED = model["Load_dc"]["COMMAND_SHED"]
            row.NDC_SHED = model["Load_ndc"]["COMMAND_SHED"]
            row.COST = model["COST"]
            session.commit()
        elif function == "ED":
            from configuration.configuration_time_line import default_look_ahead_time_step
            from configuration.configuration_time_line import default_time
            T = default_look_ahead_time_step["Look_ahead_time_ed_time_step"]
            delta_T = default_time["Time_step_ed"]

            for i in range(T):
                if session.query(database_target[function]).filter(database_target[function].TIME_STAMP == Target_time + i * delta_T).count() == 0:
                    blank_row = database_storage_operation.default_middle_term_operation_data(Target_time + i * delta_T)

                    blank_row.AC_PD = model["Load_ac"]["PD"][i]
                    blank_row.NAC_PD = model["Load_nac"]["PD"][i]
                    blank_row.DC_PD = model["Load_dc"]["PD"][i]
                    blank_row.NDC_PD = model["Load_ndc"]["PD"][i]
                    blank_row.PV_PG = model["PV"]["PG"][i]
                    blank_row.WP_PG = model["WP"]["PG"][i]
                    blank_row.DG_STATUS = model["DG"]["GEN_STATUS"][i]
                    blank_row.DG_PG = model["DG"]["COMMAND_PG"][i]
                    blank_row.UG_STATUS = model["UG"]["GEN_STATUS"][i]
                    blank_row.UG_PG = model["UG"]["COMMAND_PG"][i]
                    blank_row.BIC_PG = model["BIC"]["COMMAND_AC2DC"][i] - model["BIC"]["COMMAND_DC2AC"][i]
                    blank_row.BAT_PG = model["ESS"]["COMMAND_PG"][i]
                    blank_row.BAT_SOC = model["ESS"]["SOC"][i]
                    blank_row.PMG = model["PMG"][i]
                    blank_row.PV_CURT = model["PV"]["COMMAND_CURT"][i]
                    blank_row.WP_CURT = model["WP"]["COMMAND_CURT"][i]
                    blank_row.AC_SHED = model["Load_ac"]["COMMAND_SHED"][i]
                    blank_row.NAC_SHED = model["Load_nac"]["COMMAND_SHED"][i]
                    blank_row.DC_SHED = model["Load_dc"]["COMMAND_SHED"][i]
                    blank_row.NDC_SHED = model["Load_ndc"]["COMMAND_SHED"][i]
                    blank_row.COST = model["COST"][i]
                    session.add(blank_row)
                    session.commit()
                else:
                    row = session.query(database_target[function]).filter(database_target[function].TIME_STAMP == Target_time + i * delta_T).first()

                    row.AC_PD = model["Load_ac"]["PD"][i]
                    row.NAC_PD = model["Load_nac"]["PD"][i]
                    row.DC_PD = model["Load_dc"]["PD"][i]
                    row.NDC_PD = model["Load_ndc"]["PD"][i]
                    row.PV_PG = model["PV"]["PG"][i]
                    row.WP_PG = model["WP"]["PG"][i]
                    row.DG_STATUS = model["DG"]["GEN_STATUS"][i]
                    row.DG_PG = model["DG"]["COMMAND_PG"][i]
                    row.UG_STATUS = model["UG"]["GEN_STATUS"][i]
                    row.UG_PG = model["UG"]["COMMAND_PG"][i]
                    row.BIC_PG = model["BIC"]["COMMAND_AC2DC"][i] - model["BIC"]["COMMAND_DC2AC"][i]
                    row.BAT_PG = model["ESS"]["COMMAND_PG"][i]
                    row.BAT_SOC = model["ESS"]["SOC"][i]
                    row.PMG = model["PMG"][i]
                    row.PV_CURT = model["PV"]["COMMAND_CURT"][i]
                    row.WP_CURT = model["WP"]["COMMAND_CURT"][i]
                    row.AC_SHED = model["Load_ac"]["COMMAND_SHED"][i]
                    row.UAC_SHED = model["Load_uac"]["COMMAND_SHED"][i]
                    row.DC_SHED = model["Load_dc"]["COMMAND_SHED"][i]
                    row.UDC_SHED = model["Load_udc"]["COMMAND_SHED"][i]
                    row.COST = model["COST"][i]
                    session.commit()
        else:
            from configuration.configuration_time_line import default_look_ahead_time_step
            from configuration.configuration_time_line import default_time

            T = default_look_ahead_time_step["Look_ahead_time_uc_time_step"]
            delta_T = default_time["Time_step_uc"]

            for i in range(T):
                if session.query(database_target[function]).filter(database_target[function].TIME_STAMP == Target_time + i * delta_T).count() == 0:

                    blank_row = database_storage_operation.default_long_term_operation_data(Target_time + i * delta_T)

                    blank_row.AC_PD = model["Load_ac"]["PD"][i]
                    blank_row.NAC_PD = model["Load_nac"]["PD"][i]
                    blank_row.DC_PD = model["Load_dc"]["PD"][i]
                    blank_row.NDC_PD = model["Load_ndc"]["PD"][i]
                    blank_row.PV_PG = model["PV"]["PG"][i]
                    blank_row.WP_PG = model["WP"]["PG"][i]
                    blank_row.DG_STATUS = model["DG"]["COMMAND_START_UP"][i]
                    blank_row.DG_PG = model["DG"]["COMMAND_PG"][i]
                    blank_row.UG_STATUS = model["UG"]["COMMAND_START_UP"][i]
                    blank_row.UG_PG = model["UG"]["COMMAND_PG"][i]
                    blank_row.BIC_PG = model["BIC"]["COMMAND_AC2DC"][i] - model["BIC"]["COMMAND_DC2AC"][i]
                    blank_row.BAT_PG = model["ESS"]["COMMAND_PG"][i]
                    blank_row.BAT_SOC = model["ESS"]["SOC"][i]
                    blank_row.PMG = model["PMG"][i]
                    blank_row.PV_CURT = model["PV"]["COMMAND_CURT"][i]
                    blank_row.WP_CURT = model["WP"]["COMMAND_CURT"][i]
                    blank_row.AC_SHED = model["Load_ac"]["COMMAND_SHED"][i]
                    blank_row.UAC_SHED = model["Load_uac"]["COMMAND_SHED"][i]
                    blank_row.DC_SHED = model["Load_dc"]["COMMAND_SHED"][i]
                    blank_row.UDC_SHED = model["Load_udc"]["COMMAND_SHED"][i]
                    blank_row.COST = model["COST"][i]
                    session.add(blank_row)
                    session.commit()
                else:
                    row = session.query(database_target[function]).filter(database_target[function].TIME_STAMP == Target_time + i * delta_T).first()

                    row.AC_PD = model["Load_ac"]["PD"][i]
                    row.NAC_PD = model["Load_nac"]["PD"][i]
                    row.DC_PD = model["Load_dc"]["PD"][i]
                    row.NDC_PD = model["Load_ndc"]["PD"][i]
                    row.PV_PG = model["PV"]["PG"][i]
                    row.WP_PG = model["WP"]["PG"][i]
                    row.DG_STATUS = model["DG"]["COMMAND_START_UP"][i]
                    row.DG_PG = model["DG"]["COMMAND_PG"][i]
                    row.UG_STATUS = model["UG"]["COMMAND_START_UP"][i]
                    row.UG_PG = model["UG"]["COMMAND_PG"][i]
                    row.BIC_PG = model["BIC"]["COMMAND_AC2DC"][i] - model["BIC"]["COMMAND_DC2AC"][i]
                    row.BAT_PG = model["ESS"]["COMMAND_PG"][i]
                    row.BAT_SOC = model["ESS"]["SOC"][i]
                    row.PMG = model["PMG"][i]
                    row.PV_CURT = model["PV"]["COMMAND_CURT"][i]
                    row.WP_CURT = model["WP"]["COMMAND_CURT"][i]
                    row.AC_SHED = model["Load_ac"]["COMMAND_SHED"][i]
                    row.NAC_SHED = model["Load_nac"]["COMMAND_SHED"][i]
                    row.DC_SHED = model["Load_dc"]["COMMAND_SHED"][i]
                    row.NDC_SHED = model["Load_ndc"]["COMMAND_SHED"][i]
                    row.COST = model["COST"][i]
                    session.commit()
