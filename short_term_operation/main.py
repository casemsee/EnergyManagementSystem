import threading
import time
from configuration.configuration_time_line import default_time
from information_management.app import Single_period_information_update_thread
from information_management.app import information_send_receive
from information_management.information_send_receive import information_send
from information_management.informulation_formulation_update import single_period_information_formulation
from forecasting.app import ShortTermForecastingThread
from configuration.configuration_time_line import default_dead_line_time
from short_term_operation.set_ponits_tracing import set_points_tracing_opf
from configuration.configuration_time_line import default_look_ahead_time_step
from copy import deepcopy

from short_term_operation.input_check import InputCheckShorterm
from short_term_operation.output_check import output_local_check
from database_management.database_management import database_storage_operation
from information_management.informulation_formulation_update import single_period_information_update
from configuration.configuration_global import default_operation_mode
from modelling.database.database_format import resource_management

def short_term_operation_uems(universal_mg, local_mg, socket_upload, socket_download, info, session, logger):
    """
    Short term operation for universal energy management system
    :param universal_mg: universal ems model
    :param local_mg:local ems model
    :param socket_upload: online socket
    :param socket_download: backup socket
    :param info: information model
    :param session: database session
    :param logger: logger system
    :return: nothing to return
    """
    from short_term_operation.problem_formulation import problem_formulation
    from short_term_operation.problem_formulation_set_ponits_tracing import problem_formulation_set_points_tracing
    from short_term_operation.problem_solving import Solving_Thread
    # Short term operation
    # General procedure for short-term operation
    # 1)Information collection
    # 1.1)local EMS forecasting
    # 1.2)Information exchange
    Target_time = time.time()
    Target_time = round((Target_time - Target_time % default_time["Time_step_opf"] + default_time["Time_step_opf"]))

    # Update the universal parameter by using the database engine
    # Two threads are created to obtain the information simultaneously.
    thread_forecasting = ShortTermForecastingThread(session, Target_time, universal_mg)
    thread_info_ex = Single_period_information_update_thread(local_mg, info, socket_upload, default_look_ahead_time_step["Look_ahead_time_opf_time_step"])

    thread_forecasting.start()
    thread_info_ex.start()

    thread_forecasting.join()
    thread_info_ex.join()

    universal_mg = thread_forecasting.microgrid
    local_mg = thread_info_ex.microgrid
    universal_mg = set_points_tracing_opf(Target_time, session,universal_mg)  # There are some bugs in this function
    # Solve the optimal power flow problem
    local_mg = InputCheckShorterm.model_local_check(local_mg)
    universal_mg = InputCheckShorterm.model_universal_check(universal_mg)

    # Two threads will be created, one for feasible problem, the other for infeasible problem
    if local_mg["COMMAND_TYPE"] == 1 and universal_mg["COMMAND_TYPE"] == 1:
        logger.info("OPF is under set-points tracing mode!")
        mathematical_model = problem_formulation_set_points_tracing.problem_formulation_universal(local_mg,universal_mg,"Feasible")
        mathematical_model_recovery = problem_formulation_set_points_tracing.problem_formulation_universal(local_mg,universal_mg,"Infeasible")
    else:
        logger.info("OPF is under idle mode!")
        mathematical_model = problem_formulation.problem_formulation_universal(local_mg, universal_mg,"Feasible")
        mathematical_model_recovery = problem_formulation.problem_formulation_universal(local_mg, universal_mg,"Infeasible")
        local_mg["COMMAND_TYPE"] = 0
        universal_mg["COMMAND_TYPE"] = 0

    # Solving procedure
    res = Solving_Thread(mathematical_model)
    res_recovery = Solving_Thread(mathematical_model_recovery)
    res.daemon = True
    res_recovery.daemon = True

    res.start()
    res_recovery.start()

    res.join(default_dead_line_time["Gate_closure_opf"])
    res_recovery.join(default_dead_line_time["Gate_closure_opf"])

    if res.value["success"] is True:
        (local_mg, universal_mg) = result_update(res.value, local_mg, universal_mg, "Feasible",mathematical_model)
    else:
        (local_mg, universal_mg) = result_update(res_recovery.value, local_mg, universal_mg, "Infeasible",mathematical_model_recovery)
    # The output check the result
    local_mg = output_local_check(local_mg)
    universal_mg = output_local_check(universal_mg)

    # Return command to the local ems
    dynamic_model = single_period_information_formulation(local_mg, info, Target_time)
    dynamic_model.COMMAND_TIME_STAMP = round(time.time())
    # Update the cost function

    information_send_thread = threading.Thread(target=information_send,args=(socket_upload, dynamic_model, 2))
    database_operation__uems = threading.Thread(target=database_storage_operation.database_record,args=(session, universal_mg, Target_time, "OPF"))

    logger.info("The command for UEMS is {}".format(universal_mg["PMG"]))
    information_send_thread.start()
    database_operation__uems.start()

    information_send_thread.join()
    database_operation__uems.join()

def short_term_operation_lems(local_mg,socket_upload,socket_download,info,session,logger):
    """
    Short term operation for local ems
    The following operation sequence
    1) Information collection
    2) Short-term forecasting
    3) Information upload and database store
    4) Download command and database operation
    :param local_mg:Local energy management system models
    :param socket_upload:Upload information channel
    :param socket_download:Download information channel
    :param info:Information structure
    :param session:local database
    :param logger:
    :return:
    """
    local_mg = deepcopy(local_mg)

    Target_time = time.time()
    Target_time = round((Target_time - Target_time % default_time["Time_step_opf"] + default_time["Time_step_opf"]))

    local_mg["AREA"] = default_operation_mode["ID"]+1
    local_mg["TIME_STAMP"] = Target_time
    local_mg["COST"] = 0
    # Step 1: Short-term forecasting
    thread_forecasting = ShortTermForecastingThread(session, Target_time, local_mg)  # The forecasting thread
    thread_forecasting.start()
    thread_forecasting.join()

    local_mg = thread_forecasting.microgrid

    # Update the dynamic model
    local_mg = InputCheckShorterm.model_local_check(local_mg) # Check the data format of local ems
    local_mg = set_points_tracing_opf(Target_time,session,local_mg) # Update the

    dynamic_model = single_period_information_formulation(local_mg, info, Target_time)

    # Information send
    logger.info("Sending request from {}".format(dynamic_model.AREA) + " to the serve")
    logger.info("The local time is {}".format(dynamic_model.TIME_STAMP))
    info_management_local = information_send_receive(socket_upload,dynamic_model)
    info_management_local.send()


    # Step2: Backup operation, which indicates the universal ems is down
    dynamic_model = info_management_local.receive()# Receive information from uems
    logger.info("The command from UEMS is {}".format(dynamic_model.PMG))

    local_mg = single_period_information_update(local_mg, dynamic_model)# Store the data into the database
    database_storage_operation.database_record(session, local_mg, Target_time, "OPF")


def short_term_operation(local_mg,session,logger):
    """
    Short term operation for isolated microgrid
    The following operation sequence
    1) Short-term forecasting
    2) Information upload and database store
    3) Download command and database operation
    :param local_mg:Local energy management system models
    :param session:local database
    :param logger:
    :return:
    """
    from short_term_operation.problem_formulation import problem_formulation
    from short_term_operation.problem_formulation_set_ponits_tracing import problem_formulation_set_points_tracing
    from short_term_operation.problem_solving import Solving_Thread

    local_mg = deepcopy(local_mg)

    Target_time = time.time()
    Target_time = round((Target_time - Target_time % default_time["Time_step_opf"] + default_time["Time_step_opf"]))

    local_mg["AREA"] = default_operation_mode["ID"] + 1
    local_mg["TIME_STAMP"] = Target_time
    local_mg["COST"] = 0
    # Step 1: Short-term forecasting
    thread_forecasting = ShortTermForecastingThread(session, Target_time, local_mg)  # The forecasting thread
    thread_forecasting.start()
    thread_forecasting.join()
    local_mg = thread_forecasting.microgrid

    # Update the dynamic model
    local_mg = InputCheckShorterm.model_local_check(local_mg) # Check the data format of local ems
    local_mg = set_points_tracing_opf(Target_time,session,local_mg) # Update the operation mode of local ems

    if local_mg["COMMAND_TYPE"] == 1:
        logger.info("OPF is under set-points tracing mode!")
        mathematical_model = problem_formulation_set_points_tracing.problem_formulation_local(local_mg)
        mathematical_model_recovery = problem_formulation_set_points_tracing.problem_formulation_local_recovery(local_mg)
    else:
        logger.info("OPF is under idle mode!")
        mathematical_model = problem_formulation.problem_formulation_local(local_mg)
        mathematical_model_recovery = problem_formulation.problem_formulation_local_recovery(local_mg)
        local_mg["COMMAND_TYPE"] = 0

    # Step2: Backup operation, which indicates the universal ems is down
    # Solving procedure
    res = Solving_Thread(mathematical_model)
    res_recovery = Solving_Thread(mathematical_model_recovery)
    res.daemon = True
    res_recovery.daemon = True

    res.start()
    res_recovery.start()

    res.join(default_dead_line_time["Gate_closure_opf"])
    res_recovery.join(default_dead_line_time["Gate_closure_opf"])
    if res.value["success"] is True:
        local_mg = result_update_local(res.value, local_mg, "Feasible", mathematical_model)
    else:
        local_mg = result_update_local(res_recovery.value, local_mg, "Infeasible",mathematical_model_recovery)

        local_mg = output_local_check(local_mg)
    #Check the output of optimal power flow
    local_mg = output_local_check(local_mg)
    database_storage_operation.database_record(session, local_mg, Target_time, "OPF")

def result_update(res, local_model, universal_model, type, mathematical_model):
    """
    Result update for universal energy management system
    :param res:
    :param local_model:
    :param universal_model:
    :param type:
    :param mathematical_model:
    :return:
    """
    if type == "Feasible":
        if local_model["COMMAND_TYPE"] is 0:
            from modelling.data.idx_format import NX
        else:
            from modelling.data.idx_opf_set_points_tracing import NX
    else:
        if local_model["COMMAND_TYPE"] is 0:
            from modelling.data.idx_format_recovery import NX
        else:
            from modelling.data.idx_opf_set_points_tracing_recovery import NX

    x_local = res["x"][0:NX]
    x_universal = res["x"][NX:2 * NX]
    c_local = mathematical_model["c"][0:NX]
    c_universal = mathematical_model["c"][0:NX]

    local_model = update(x_local, local_model, type)
    universal_model = update(x_universal, universal_model, type)

    local_model["COST"] = float(sum([c*d for c,d in zip(c_local,x_local)])) # Update the
    universal_model["COST"] = float(sum([c * d for c, d in zip(c_universal, x_universal)]))

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

    x_local = res["x"]
    c_local = mathematical_model["c"]

    local_model = update(x_local, local_model, type)
    local_model["COST"] = float(sum([c*d for c,d in zip(c_local,x_local)])) # Update the

    return local_model


def update(*args):
    x = args[0]
    microgrid = args[1]
    model_type = args[2]

    if model_type == "Feasible":
        if microgrid["COMMAND_TYPE"] is 0:
            from modelling.data.idx_format import PG, QG, RG, PUG, QUG, RUG, PBIC_AC2DC, PBIC_DC2AC, QBIC, PESS_C, \
                PESS_DC, RESS, PMG
        else:
            from modelling.data.idx_opf_set_points_tracing import PG, QG, RG, PUG, QUG, RUG, PBIC_AC2DC, PBIC_DC2AC, QBIC, PESS_C, \
                PESS_DC, RESS, PMG

        microgrid["DG"]["COMMAND_PG"] = int(x[PG])
        microgrid["DG"]["COMMAND_QG"] = int(x[QG])
        microgrid["DG"]["COMMAND_RG"] = int(x[RG])

        microgrid["UG"]["COMMAND_PG"] = int(x[PUG])
        microgrid["UG"]["COMMAND_QG"] = int(x[QUG])
        microgrid["UG"]["COMMAND_RG"] = int(x[RUG])

        microgrid["BIC"]["COMMAND_AC2DC"] = int(x[PBIC_AC2DC])
        microgrid["BIC"]["COMMAND_DC2AC"] = int(x[PBIC_DC2AC])

        microgrid["BIC"]["COMMAND_Q"] = int(x[QBIC])

        microgrid["ESS"]["COMMAND_PG"] = int(x[PESS_DC]) - int(x[PESS_C])
        microgrid["ESS"]["COMMAND_RG"] = int(x[RESS])

        microgrid["PMG"] = int(x[PMG])
        microgrid["success"] = True

    else:
        if microgrid["COMMAND_TYPE"] is 0:
            from modelling.data.idx_format_recovery import PG, QG, RG, PUG, QUG, RUG, PBIC_AC2DC, PBIC_DC2AC, QBIC, \
                PESS_C, PESS_DC, RESS, PMG, PPV, PWP, PL_AC, PL_UAC, PL_DC, PL_UDC
        else:
            from modelling.data.idx_opf_set_points_tracing_recovery import PG, QG, RG, PUG, QUG, RUG, PBIC_AC2DC, PBIC_DC2AC, \
                QBIC,PESS_C, PESS_DC, RESS, PMG, PPV, PWP, PL_AC, PL_UAC, PL_DC, PL_UDC
            microgrid["DG"]["COMMAND_PG"] = int(x[PG])
        microgrid["DG"]["COMMAND_QG"] = int(x[QG])
        microgrid["DG"]["COMMAND_RG"] = int(x[RG])

        microgrid["UG"]["COMMAND_PG"] = int(x[PUG])
        microgrid["UG"]["COMMAND_QG"] = int(x[QUG])
        microgrid["UG"]["COMMAND_RG"] = int(x[RUG])

        microgrid["BIC"]["COMMAND_AC2DC"] = int(x[PBIC_AC2DC])
        microgrid["BIC"]["COMMAND_DC2AC"] = int(x[PBIC_DC2AC])
        microgrid["BIC"]["COMMAND_Q"] = int(x[QBIC])

        microgrid["ESS"]["COMMAND_PG"] = int(x[PESS_DC]) - int(x[PESS_C])
        microgrid["ESS"]["COMMAND_RG"] = int(x[RESS])

        microgrid["PMG"] = int(x[PMG])

        microgrid["PV"]["COMMAND_CURT"] = int(microgrid["PV"]["PG"]- x[PPV])
        microgrid["WP"]["COMMAND_CURT"] = int(microgrid["WP"]["PG"] - x[PWP])
        microgrid["Load_ac"]["COMMAND_SHED"] = int(microgrid["Load_ac"]["PD"] - x[PL_AC])
        microgrid["Load_nac"]["COMMAND_SHED"] = int(microgrid["Load_nac"]["PD"] - x[PL_UAC])
        microgrid["Load_dc"]["COMMAND_SHED"] = int(microgrid["Load_dc"]["PD"] - x[PL_DC])
        microgrid["Load_ndc"]["COMMAND_SHED"] = int(microgrid["Load_ndc"]["PD"] - x[PL_UDC])

        microgrid["success"] = False

    return microgrid


def status_update(microgrid,session,Target_time):
    """
    Update Battery SOC, generation status, load status, bic status etc
    :param microgrid: information model of
    :param session: inquery the real time operation database
    :param Target_time: scheduling time of short time operation
    :return: microgrid model
    1) check the database of resource manager, if not exist, 2); if exist, update the soc, available information, go to 3)
    2) check the short term operation database, if not exist, go to 3); if exist, update the soc and available information.
    3) update the scheduling information from middle term operation database, if not exist, do nothing, if exist, update the status of gen,load,bic,battery
    Note: This function serves as the closed loop between the scheduling and information.
    """

    row = session.query(resource_management).filter_by(resource_management.TIME_STAMP <= Target_time).fisrt()
    microgrid["ESS"]["SOC"] = row.BAT_SOC
    microgrid["DG"]["STATUS"] = row.DG_STATUS
    microgrid["UG"]["STATUS"] = row.UG_STATUS

    return microgrid