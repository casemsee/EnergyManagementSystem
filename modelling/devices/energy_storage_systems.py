"""
Models of energy storage systems
Two types of energy storage systems are supported.
1) Battery energy storage system (BESS)
2) Thermal energy storage system (TESS)
"""

import configuration.configuration_default_ess as default_parameters
BESS =\
    {   #1) Static information
        "ID": default_parameters.BESS["AREA"],
        "CAP": default_parameters.BESS["CAP"],
        "PMAX_DIS": default_parameters.BESS["PMAX_DIS"],
        "PMAX_CH": default_parameters.BESS["PMAX_CH"],
        "EFF_DIS":default_parameters.BESS["EFF_DIS"],
        "EFF_CH":default_parameters.BESS["EFF_CH"],
        "SOC_MAX":default_parameters.BESS["SOC_MAX"],
        "SOC_MIN":default_parameters.BESS["SOC_MIN"],
        "COST_MODEL":default_parameters.BESS["COST_MODEL"],
        "NCOST_DIS":default_parameters.BESS["NCOST_DIS"],
        "COST_DIS":default_parameters.BESS["COST_DIS"],
        "NCOST_CH":default_parameters.BESS["NCOST_CH"],
        "COST_CH":default_parameters.BESS["COST_CH"],
        # 2) Measurement information
        "STATUS": default_parameters.BESS["STATUS"],
        "SOC":default_parameters.BESS["SOC"],
        "PG": default_parameters.BESS["PG"],
        "RG": default_parameters.BESS["RG"],
        # 3) Scheduling information
        "TIME_GENERATED": default_parameters.BESS["TIME_GENERATED"],
        "TIME_APPLIED": default_parameters.BESS["TIME_APPLIED"],
        "TIME_COMMANDED": default_parameters.BESS["TIME_COMMANDED"],
        "COMMAND_PG":default_parameters.BESS["COMMAND_PG"],
        "COMMAND_RG":default_parameters.BESS["COMMAND_RG"],
    }