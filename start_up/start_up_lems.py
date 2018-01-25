"""
Start up operation procedure for local ems
short, middle and long term operating models are generated for the short, middle and long term operation respectively.
"""

from modelling.devices import generators, loads, energy_storage_systems, convertors  # Information modelling
from configuration.configuration_time_line import default_look_ahead_time_step # Look ahead time
from configuration.configuration_global import default_command
from copy import deepcopy

def start_up():
    # Obtain static information of the local ems
    # Update the local EMS parameters
    microgrid = {"DG": deepcopy(generators.Generator_AC),
                 "UG": deepcopy(generators.Generator_AC),
                 "Load_ac": deepcopy(loads.Load_AC),
                 "Load_nac":deepcopy(loads.Load_AC),
                 "BIC": deepcopy(convertors.BIC),
                 "ESS": deepcopy(energy_storage_systems.BESS),
                 "PV": deepcopy(generators.Generator_RES),
                 "WP": deepcopy(generators.Generator_RES),
                 "Load_dc": deepcopy(loads.Load_DC),
                 "Load_ndc": deepcopy(loads.Load_DC),
                 "PMG": 0,
                 "V_DC": 0}
    # Price information update
    microgrid["UG"]["COST_START_UP"] = 0
    microgrid["PV"]["N"] = microgrid["PV"]["PMAX"]
    microgrid["PV"]["TYPE"] = default_command["PV"]
    microgrid["WP"]["N"] = microgrid["WP"]["PMAX"]
    microgrid["WP"]["TYPE"] = default_command["WP"]

    microgrid["Load_ac"]["FLEX"] = default_command["CRITICAL"]
    microgrid["Load_nac"]["FLEX"] = default_command["NON_CRITICAL"]
    microgrid["Load_dc"]["FLEX"] = default_command["CRITICAL"]
    microgrid["Load_ndc"]["FLEX"] = default_command["NON_CRITICAL"]

    T_short = default_look_ahead_time_step[
        "Look_ahead_time_opf_time_step"]  # The look ahead time step for short term operation
    T_middle = default_look_ahead_time_step[
        "Look_ahead_time_ed_time_step"]  # The look ahead time step for middle term operation
    T_long = default_look_ahead_time_step[
        "Look_ahead_time_uc_time_step"]  # The look ahead time step for long term operation
    # Update information
    local_mg_short = deepcopy(microgrid)
    local_mg_middle = deepcopy(microgrid)
    local_mg_long = deepcopy(microgrid)

    # Generate middle term operation model for local ems, these information should be updated according to the database of resource manager
    local_mg_middle["UG"]["STATUS"] = [local_mg_middle["UG"]["STATUS"]] * T_middle
    local_mg_middle["DG"]["STATUS"] = [local_mg_middle["DG"]["STATUS"]] * T_middle
    local_mg_middle["PV"]["N"] = [local_mg_middle["PV"]["N"]] * T_middle
    local_mg_middle["PV"]["PMAX"] = [local_mg_middle["PV"]["PMAX"]] * T_middle
    local_mg_middle["WP"]["N"] = [local_mg_middle["WP"]["N"]] * T_middle
    local_mg_middle["WP"]["PMAX"] = [local_mg_middle["WP"]["PMAX"]] * T_middle
    local_mg_middle["Load_ac"]["STATUS"] = [local_mg_middle["Load_ac"]["STATUS"]] * T_middle
    local_mg_middle["Load_nac"]["STATUS"] = [local_mg_middle["Load_nac"]["STATUS"]] * T_middle
    local_mg_middle["Load_dc"]["STATUS"] = [local_mg_middle["Load_dc"]["STATUS"]] * T_middle
    local_mg_middle["Load_ndc"]["STATUS"] = [local_mg_middle["Load_ndc"]["STATUS"]] * T_middle
    local_mg_middle["BIC"]["STATUS"] = [local_mg_middle["BIC"]["STATUS"]] * T_middle
    local_mg_middle["ESS"]["STATUS"] = [local_mg_middle["ESS"]["STATUS"]] * T_middle

    # Generate long term operation model for local ems
    local_mg_long["UG"]["STATUS"] = [local_mg_long["UG"]["STATUS"]] * T_long
    local_mg_long["DG"]["STATUS"] = [local_mg_long["DG"]["STATUS"]] * T_long
    local_mg_long["PV"]["N"] = [local_mg_long["PV"]["N"]] * T_long
    local_mg_long["PV"]["PMAX"] = [local_mg_long["PV"]["PMAX"]] * T_long
    local_mg_long["WP"]["N"] = [local_mg_long["WP"]["N"]] * T_long
    local_mg_long["WP"]["PMAX"] = [local_mg_long["WP"]["PMAX"]] * T_long
    local_mg_long["Load_ac"]["STATUS"] = [local_mg_long["Load_ac"]["STATUS"]] * T_long
    local_mg_long["Load_nac"]["STATUS"] = [local_mg_long["Load_nac"]["STATUS"]] * T_long
    local_mg_long["Load_dc"]["STATUS"] = [local_mg_long["Load_dc"]["STATUS"]] * T_long
    local_mg_long["Load_ndc"]["STATUS"] = [local_mg_long["Load_ndc"]["STATUS"]] * T_long
    local_mg_long["BIC"]["STATUS"] = [local_mg_long["BIC"]["STATUS"]] * T_long
    local_mg_long["ESS"]["STATUS"] = [local_mg_long["ESS"]["STATUS"]] * T_long

    return local_mg_short,local_mg_middle,local_mg_long

