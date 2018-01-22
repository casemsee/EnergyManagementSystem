"""
Start up operation procedure for local ems
short, middle and long term operating models are generated for the short, middle and long term operation respectively.
"""

from modelling.devices import generators, loads, energy_storage_systems, convertors  # Import modellings
from configuration.configuration_time_line import default_look_ahead_time_step# The look ahead time is adopted to
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

    microgrid["PV"]["N"] = microgrid["PV"]["PMAX"]
    microgrid["PV"]["TYPE"] = default_command["PV"]
    microgrid["WP"]["N"] = microgrid["WP"]["PMAX"]
    microgrid["WP"]["TYPE"] = default_command["WP"]

    microgrid["Load_ac"]["FLEX"] = default_command["CRITICAL"]
    microgrid["Load_nac"]["FLEX"] = default_command["NON_CRITICAL"]
    microgrid["Load_dc"]["FLEX"] = default_command["CRITICAL"]
    microgrid["Load_ndc"]["FLEX"] = default_command["NON_CRITICAL"]


    return microgrid

