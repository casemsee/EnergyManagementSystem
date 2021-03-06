# Loads modelling in universal energy management system
# Generally, there are two types of loads in the UEMS
import configuration.configuration_default_load as default_parameters

Load_AC = \
	{   # 1) Static information
		"ID": default_parameters.default_Load_AC["AREA"],
		"PMAX": default_parameters.default_Load_AC["PDMAX"],
		"PMIN": default_parameters.default_Load_AC["PDMIN"],
		"FLEX": default_parameters.default_Load_AC["FLEX"],  # 0, load is undispatchable;1, load is dispatchable
		"MODEL": default_parameters.default_Load_AC["MODEL"],
		# 0, load is discrete dispatchable;1, load is contineously dispatchable
		"COST_MODEL": default_parameters.default_Load_AC["COST_MODEL"],
		"NCOST": default_parameters.default_Load_AC["NCOST"],
		"COST": default_parameters.default_Load_AC["COST"],
		# 2) Measurement information
		"STATUS": default_parameters.default_Load_AC["STATUS"],
		# The generation status, >0 means avalible, otherwise, unavaliable
		"PD": default_parameters.default_Load_AC["PD"],
		"QD": default_parameters.default_Load_AC["QD"],
		"PF": default_parameters.default_Load_AC["PF"],
		"APF": default_parameters.default_Load_AC["APF"],
		# 3) Scheduling information
		"TIME_GENERATED": default_parameters.default_Load_AC["TIME_GENERATED"],
		"TIME_APPLIED": default_parameters.default_Load_AC["TIME_APPLIED"],
		"TIME_COMMANDED": default_parameters.default_Load_AC["TIME_COMMANDED"],
		"COMMAND_PD": default_parameters.default_Load_AC["COMMAND_SHED"],
		"COMMAND_RD": default_parameters.default_Load_AC["COMMAND_RESERVE"],
	}

Load_DC = \
	{   # 1) Static information
		"ID": default_parameters.default_Load_DC["AREA"],
		"PMAX": default_parameters.default_Load_DC["PDMAX"],
		"PMIN": default_parameters.default_Load_DC["PDMIN"],
		"FLEX": default_parameters.default_Load_DC["FLEX"],  # 0, load is undispatchable;1, load is dispatchable
		"MODEL": default_parameters.default_Load_DC["MODEL"],# 0, load is discrete dispatchable;1, load is contineously dispatchable
		"COST_MODEL": default_parameters.default_Load_DC["COST_MODEL"],
		"NCOST": default_parameters.default_Load_DC["NCOST"],
		"COST": default_parameters.default_Load_DC["COST"],
		# 2) Measurement information
		"STATUS": default_parameters.default_Load_DC["STATUS"],
		# The generation status, >0 means avalible, otherwise, unavaliable
		"PD": default_parameters.default_Load_DC["PD"],
		"APF": default_parameters.default_Load_DC["APF"],
		# 3) Scheduling information
		"TIME_GENERATED": default_parameters.default_Load_DC["TIME_GENERATED"],
		"TIME_APPLIED": default_parameters.default_Load_DC["TIME_APPLIED"],
		"TIME_COMMANDED": default_parameters.default_Load_DC["TIME_COMMANDED"],
		"COMMAND_PD": default_parameters.default_Load_DC["COMMAND_SHED"],
		"COMMAND_RD": default_parameters.default_Load_DC["COMMAND_RESERVE"],
	}
