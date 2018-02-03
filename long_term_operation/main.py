"""
Jointed energy and reserves are optimized to reduce the operation cost and risk.
@author: Zhao Tianyang
@data: 24 September 2017
"""

import threading
import time
from configuration.configuration_time_line import default_time,default_look_ahead_time_step
from information_management.app import MultiplePeriodsInformationUpdateThread, MultiplePeriodsInformationFormulationThread
from information_management.app import InformationSendReceive
from long_term_operation.long_tertm_forecasting import ForecastingThread
from utils import Logger
from copy import deepcopy
from long_term_operation.input_check import InputCheck
from long_term_operation.output_check import OutputCheck
from long_term_operation.long2middle import Long2Middle
from modelling.database.database_format import db_middle_term
from database_management.database_management import database_storage_operation

logger_uems = Logger("Long_term_dispatch_UEMS")
logger_lems = Logger("Long_term_dispatch_LEMS")

def long_term_operation_uems(*args):
    # Short term forecasting for the middle term operation in universal energy management system.
    from long_term_operation.problem_formulation import ProblemFormulation
    from long_term_operation.problem_solving import SolvingThread
    from configuration.configuration_time_line import default_dead_line_time
    # Short term operation
    # General procedure for middle-term operation
    # 1)Information collection
    # 1.1)local EMS forecasting
    # 1.2)Information exchange
    universal_models = deepcopy(args[0])
    local_models = deepcopy(args[1])
    socket_upload = args[2]
    socket_download = args[3]
    info = args[4]
    session = args[5]

    Target_time = time.time()
    Target_time = round((Target_time - Target_time % default_time["Time_step_uc"] + default_time["Time_step_uc"]))

    # Update the universal parameter by using the database engine
    # Two threads are created to obtain the information simultaneously.
    thread_forecasting = ForecastingThread(session, Target_time, universal_models)
    thread_info_ex = MultiplePeriodsInformationUpdateThread(local_models,info,socket_upload)

    thread_forecasting.start()
    thread_info_ex.start()

    thread_forecasting.join()
    thread_info_ex.join()

    universal_models = thread_forecasting.models
    local_models = thread_info_ex.microgrid

    local_models = InputCheck.model_local_check(local_models)
    universal_models = InputCheck.model_universal_check(universal_models)
    # Solve the optimal power flow problem
    # Two threads will be created, one for feasible problem, the other for infeasible problem
    # universal_models["ESS"]["SOC"]=universal_models["ESS"]["SOC_MIN"], the test shows that, the input check is necessary.

    mathematical_model = ProblemFormulation.problem_formulation_universal(local_models, universal_models,
                                                                               "Feasible")
    mathematical_model_recovery = ProblemFormulation.problem_formulation_universal(local_models, universal_models,
                                                                                        "Infeasible")
    # Solve the problem
    res = SolvingThread(mathematical_model)
    res_recovery = SolvingThread(mathematical_model_recovery)
    res.daemon = True
    res_recovery.daemon = True

    res.start()
    res_recovery.start()

    res.join(default_dead_line_time["Gate_closure_uc"])
    res_recovery.join(default_dead_line_time["Gate_closure_uc"])

    if res.value["success"] == True:
        (local_models, universal_models) = result_update(res.value, local_models, universal_models, "Feasible")
    else:
        (local_models, universal_models) = result_update(res_recovery.value, local_models, universal_models,"Infeasible")

    local_models = OutputCheck.output_local_check(local_models)
    universal_models = OutputCheck.output_local_check(universal_models)

    # Return command to the local ems
    local_models["COMMAND_TYPE"] = 0
    dynamic_model = MultiplePeriodsInformationFormulationThread(local_models, info, Target_time,"UC")
    dynamic_model.TIME_STAMP_COMMAND = round(time.time())

    information_send_thread = threading.Thread(target=InformationSendReceive(socket_upload,dynamic_model),
                                                args=(socket_upload, dynamic_model, 2))

    database_operation_uems = threading.Thread(target=database_storage_operation.database_record,
                                                    args=(session, universal_models, Target_time, "UC"))

    Long2Middle.run(Target_time, session, universal_models)
    logger_uems.info("The command for UEMS is {}".format(universal_models["PMG"]))
    information_send_thread.start()
    database_operation_uems.start()

    information_send_thread.join()
    database_operation_uems.join()

def long_term_operation_lems(*args):
    # Short term operation for local ems
    # The following operation sequence
    # 1) Information collection
    # 2) Short-term forecasting
    # 3) Information upload and database store
    # 4) Download command and database operation
    local_models = deepcopy(args[0])  # Local energy management system models
    socket_upload = args[1]  # Upload information channel
    socket_download = args[2]  # Download information channel
    info = args[3]  # Information structure
    session = args[4]  # local database

    Target_time = time.time()
    Target_time = round((Target_time - Target_time % default_time["Time_step_uc"] + default_time["Time_step_uc"]))

    # Step 1: Short-term forecasting
    thread_forecasting = ForecastingThread(session, Target_time, local_models)  # The forecasting thread
    thread_forecasting.start()
    thread_forecasting.join()

    local_models = thread_forecasting.models
    # Update the dynamic model
    local_models["COMMAND_TYPE"] = 0
    dynamic_model = MultiplePeriodsInformationUpdateThread(local_models, Target_time,"UC")
    # Information send
    logger_lems.info("Sending request from {}".format(dynamic_model.AREA) + " to the serve")
    logger_lems.info("The local time is {}".format(dynamic_model.TIME_STAMP))
    information_send_receive = InformationSendReceive(socket_upload, dynamic_model)
    information_send_receive.send()

    # Step2: Backup operation, which indicates the universal ems is down
    # Receive information from uems
    dynamic_model = information_send_receive.receive()
    # print("The universal time is", dynamic_model.TIME_STAMP_COMMAND)
    logger_lems.info("The command from UEMS is {}".format(dynamic_model.PMG))
    # Store the data into the database

    multiple_periods_information_update_thread = MultiplePeriodsInformationUpdateThread(local_models, dynamic_model)
    multiple_periods_information_update_thread.start()
    multiple_periods_information_update_thread.join()
    local_models = multiple_periods_information_update_thread.microgrid
    Long2Middle.run(Target_time, session, local_models)

    database_operation_lems = threading.Thread(target=database_storage_operation.database_record,args=(session, local_models, Target_time, "UC"))

    database_operation_lems.start()
    database_operation_lems.join()


def long_term_operation(microgrid,session,session_history,logger):
    """
    Long-term operation for standalone ems
    :param local_mg:Long-term energy management system models
    :param session:local database
    :param logger:
    :return: nothing
    The following operation sequence
    1) Long-term forecasting
    2) Status update
    3) Input check
    4) Problem formulation
    5) Problem solving
    6) Output check
    7) Database operation
    """
    from long_term_operation.problem_formulation import ProblemFormulation
    from long_term_operation.problem_solving import SolvingThread
    from configuration.configuration_time_line import default_dead_line_time
    # from long_term_operation.problem_solving import solving_procedure
    microgrid = deepcopy(microgrid)  # Local energy management system models

    Target_time = time.time()
    Target_time = round((Target_time - Target_time % default_time["Time_step_uc"] + default_time["Time_step_uc"]))

    # Step 1: Short-term forecasting
    thread_forecasting = ForecastingThread(session, session_history, Target_time, microgrid)  # The forecasting thread
    thread_forecasting.start()
    thread_forecasting.join()
    microgrid = thread_forecasting.models
    # Step 2: Status update
    # microgrid = status_update(microgrid, session, Target_time)
    # Step 4: Input check
    microgrid = InputCheck.model_local_check(microgrid)
    # Step 5: Problem formulation
    mathematical_model = ProblemFormulation.problem_formulation_local(microgrid)
    mathematical_model_recovery = ProblemFormulation.problem_formulation_local_recovery(microgrid)
    # Step 6: Problem solving
    # res = solving_procedure(mathematical_model)
    res = SolvingThread(mathematical_model)
    res_recovery = SolvingThread(mathematical_model_recovery)
    res.daemon = True
    res_recovery.daemon = True

    res.start()
    res_recovery.start()

    res.join(default_dead_line_time["Gate_closure_uc"])
    res_recovery.join(default_dead_line_time["Gate_closure_uc"])

    if res.value["success"] == True:
        microgrid = result_update_local(res.value, microgrid, "Feasible",mathematical_model)
    else:
        microgrid = result_update_local(res_recovery.value, microgrid,"Infeasible",mathematical_model_recovery)

    # Step 7: Output check
    microgrid = OutputCheck.output_local_check(microgrid)

    # Step 8: Database operation
    Long2Middle.run(Target_time, session, microgrid)
    database_storage_operation.database_record(session, microgrid, Target_time, "UC")

def result_update(*args):
    ## Result update for local ems and universal ems models
    res = args[0]
    local_model = args[1]
    universal_model = args[2]
    type = args[3]
    T = default_look_ahead_time_step["Look_ahead_time_uc_time_step"]

    if type == "Feasible":
        from modelling.data.idx_uc_format import NX
    else:
        from modelling.data.idx_uc_recovery_format import NX

    nx = T * NX
    x_local = res["x"][0:nx]
    x_universal = res["x"][nx:2*nx]

    local_model = update(x_local, local_model, type)
    universal_model = update(x_universal, universal_model, type)

    return local_model, universal_model

def result_update_local(*args):
    """
    Result update with obtained solution and
    :param args: the obtained solutions,
    :return: updated solutions of information models
    """
    res = args[0]
    local_model = args[1]
    type = args[2]
    mathematical_model = args[3]

    T = default_look_ahead_time_step["Look_ahead_time_uc_time_step"]

    x_local = res["x"]
    c_local = mathematical_model["c"]

    local_model = update(x_local, local_model, type)

    local_model["COST"] = [0]*T

    if type == "Feasible":
        from modelling.data.idx_uc_format import NX
    else:
        from modelling.data.idx_uc_recovery_format import NX

    for i in range(T):
        local_model["COST"][i] = float(sum([c*d for c,d in zip(c_local[i*NX:(i+1)*NX],x_local[i*NX:(i+1)*NX])]))*default_time["Time_step_ed"]/3600 # Update the

    return local_model

def update(*args):
    x = args[0]
    model = args[1]
    type = args[2]
    T = default_look_ahead_time_step["Look_ahead_time_uc_time_step"]

    if type == "Feasible":
        from modelling.data.idx_uc_format import IG, PG, RG, IUG, PUG, RUG, PBIC_AC2DC, PBIC_DC2AC, PESS_C, PESS_DC, RESS,EESS,\
            PMG, NX
        model["DG"]["COMMAND_START_UP"] = [0] * T
        model["DG"]["COMMAND_PG"] = [0] * T
        model["DG"]["COMMAND_RG"] = [0] * T

        model["UG"]["COMMAND_START_UP"] = [0] * T
        model["UG"]["COMMAND_PG"] = [0] * T
        model["UG"]["COMMAND_RG"] = [0] * T

        model["BIC"]["COMMAND_AC2DC"] = [0] * T
        model["BIC"]["COMMAND_DC2AC"] = [0] * T

        model["ESS"]["COMMAND_PG"] = [0] * T
        model["ESS"]["COMMAND_RG"] = [0] * T
        model["ESS"]["SOC"] = [0]*T

        model["PV"]["COMMAND_CURT"] = [0] * T
        model["WP"]["COMMAND_CURT"] = [0] * T

        model["PMG"] = [0] * T

        model["Load_ac"]["COMMAND_SHED"] = [0] * T
        model["Load_nac"]["COMMAND_SHED"] = [0] * T
        model["Load_dc"]["COMMAND_SHED"] = [0] * T
        model["Load_ndc"]["COMMAND_SHED"] = [0] * T

        for i in range(T):
            model["DG"]["COMMAND_START_UP"][i] = int(x[i * NX + IG])
            model["DG"]["COMMAND_PG"][i] = int(x[i * NX + PG])
            model["DG"]["COMMAND_RG"][i] = int(x[i * NX + RG])

            model["UG"]["COMMAND_START_UP"][i] = int(x[i * NX + IUG])
            model["UG"]["COMMAND_PG"][i] = int(x[i * NX + PUG])
            model["UG"]["COMMAND_RG"][i] = int(x[i * NX + RUG])

            model["BIC"]["COMMAND_AC2DC"][i] = int(x[i * NX + PBIC_AC2DC])
            model["BIC"]["COMMAND_DC2AC"][i] = int(x[i * NX + PBIC_DC2AC])

            model["ESS"]["COMMAND_PG"][i] = int(x[i * NX + PESS_DC] - x[i * NX + PESS_C])
            model["ESS"]["COMMAND_RG"][i] = int(x[i * NX + RESS])
            model["ESS"]["SOC"][i] = x[i*NX+EESS]/model["ESS"]["CAP"]

            model["PMG"][i] = int(x[i * NX + PMG])

        model["success"] = True
    else:
        from modelling.data.idx_uc_recovery_format import IG, PG, RG, IUG, PUG, RUG, IBIC, PBIC_AC2DC, PBIC_DC2AC, PESS_C,EESS, \
            PESS_DC, RESS, PMG, IPV, IWP, IL_AC, IL_NAC, IL_DC, IL_NDC, NX

        model["DG"]["COMMAND_START_UP"] = [0] * T
        model["DG"]["COMMAND_PG"] = [0] * T
        model["DG"]["COMMAND_RG"] = [0] * T

        model["UG"]["COMMAND_START_UP"] = [0] * T
        model["UG"]["COMMAND_PG"] = [0] * T
        model["UG"]["COMMAND_RG"] = [0] * T

        model["BIC"]["COMMAND_AC2DC"] = [0] * T
        model["BIC"]["COMMAND_DC2AC"] = [0] * T

        model["ESS"]["COMMAND_PG"] = [0] * T
        model["ESS"]["COMMAND_RG"] = [0] * T
        model["ESS"]["SOC"] = [0] * T

        model["PV"]["COMMAND_CURT"] = [0] * T
        model["WP"]["COMMAND_CURT"] = [0] * T

        model["PMG"] = [0] * T

        model["Load_ac"]["COMMAND_SHED"] = [0] * T
        model["Load_nac"]["COMMAND_SHED"] = [0] * T
        model["Load_dc"]["COMMAND_SHED"] = [0] * T
        model["Load_ndc"]["COMMAND_SHED"] = [0] * T

        for i in range(T):
            # Update the solutions
            model["DG"]["COMMAND_START_UP"][i] = int(x[i * NX + IG])
            model["DG"]["COMMAND_PG"][i] = int(x[i * NX + PG])
            model["DG"]["COMMAND_RG"][i] = int(x[i * NX + RG])

            model["UG"]["COMMAND_START_UP"][i] = int(x[i * NX + IUG])
            model["UG"]["COMMAND_PG"][i] = int(x[i * NX + PUG])
            model["UG"]["COMMAND_RG"][i] = int(x[i * NX + RUG])

            model["BIC"]["COMMAND_AC2DC"][i] = int(x[i * NX + PBIC_AC2DC])
            model["BIC"]["COMMAND_DC2AC"][i] = int(x[i * NX + PBIC_DC2AC])

            model["ESS"]["COMMAND_PG"][i] = int(x[i * NX + PESS_DC] - x[i * NX + PESS_C])
            model["ESS"]["COMMAND_RG"][i] = int(x[i * NX + RESS])
            model["ESS"]["SOC"][i] = x[i * NX + EESS]/model["ESS"]["CAP"]

            model["PMG"][i] = int(x[i * NX + PMG])

            model["PV"]["COMMAND_CURT"][i] = model["PV"]["PG"][i]-int(x[i * NX + IPV])
            model["WP"]["COMMAND_CURT"][i] = model["WP"]["PG"][i]-int(x[i * NX + IWP])

            model["Load_ac"]["COMMAND_SHED"][i] = model["Load_ac"]["PD"][i]-int(x[i * NX + IL_AC])
            model["Load_nac"]["COMMAND_SHED"][i] = model["Load_nac"]["PD"][i]-int(x[i * NX + IL_NAC])
            model["Load_dc"]["COMMAND_SHED"][i] = model["Load_dc"]["PD"][i]-int(x[i * NX + IL_DC])
            model["Load_ndc"]["COMMAND_SHED"][i] = model["Load_ndc"]["PD"][i]-int(x[i * NX + IL_NDC])

        model["success"] = False
    return model

def status_update(microgrid,session,Target_time):
    """
    Update Battery SOC, generation status, load status, bic status etc, according to the scheduling of middle term operation
    :param microgrid: information model
    :param session: inquery the middle_term operation database
    :param Target_time: scheduling time of middle time operation
    :return: microgrid model
    1) check the database of resource manager, if not exist, 2); if exist, update the soc, available information, go to 3)
    2) check the short term operation database, if not exist, go to 3); if exist, update the soc and available information.
    3) update the scheduling information from middle term operation database, if not exist, do nothing, if exist, update the status of gen,load,bic,battery
    Note: This function serves as the closed loop between the scheduling and information.
    """

    if session.query(db_middle_term).filter(db_middle_term.TIME_STAMP == Target_time).count()!=0:
        row = session.query(db_middle_term).filter(db_middle_term.TIME_STAMP == Target_time).first()
        microgrid["ESS"]["SOC"] = row.BAT_SOC
        microgrid["DG"]["STATUS"] = [row.DG_STATUS]*default_look_ahead_time_step["Look_ahead_time_uc_time_step"]
        microgrid["UG"]["STATUS"] = [row.UG_STATUS]*default_look_ahead_time_step["Look_ahead_time_uc_time_step"]

    return microgrid