# The generators set includes the following types of generators:
# 1) AC generators(Generator_AC)
# 2) DC generators(Generator_DC)
# 3) Renewable generators(Generator_RES)
import configuration.configuration_default_generators as default_parameters

Generator_AC = \
	{   #1) Static information
		"ID": default_parameters.default_AC_generator_parameters["AREA"],# Integrated MG
		"PMAX": default_parameters.default_AC_generator_parameters["PMAX"],# Maximal power limitation
		"PMIN": default_parameters.default_AC_generator_parameters["PMIN"],# Minimal power limitation
		"QMAX": default_parameters.default_AC_generator_parameters["QMAX"],# Maximal reactive power limitation
		"QMIN": default_parameters.default_AC_generator_parameters["QMIN"],# Minimal reactive power limitation
		"SMAX": default_parameters.default_AC_generator_parameters["SMAX"],#  factor limitation
		"RAMP_AGC": default_parameters.default_AC_generator_parameters["RAMP_AGC"],# Power factor limitation
		"RAMP_10": default_parameters.default_AC_generator_parameters["RAMP_10"],# Power factor limitation
		"PF_LIMIT": default_parameters.default_AC_generator_parameters["PF_LIMIT"],# Power factor limitation
		"COST_START_UP": default_parameters.default_AC_generator_parameters["COST_START_UP"],
		"COST_SHUT_DOWN": default_parameters.default_AC_generator_parameters["COST_SHUT_DOWN"],
		"COST_MODEL": default_parameters.default_AC_generator_parameters["COST_MODEL"],
		"NCOST": default_parameters.default_AC_generator_parameters["NCOST"],
		"COST": default_parameters.default_AC_generator_parameters["COST"],
		#2) Measurement information
		"STATUS": default_parameters.default_AC_generator_parameters["STATUS"],# Generation status, >0 means avalible, otherwise, unavaliable
		"PG": default_parameters.default_AC_generator_parameters["PG"],
		"QG": default_parameters.default_AC_generator_parameters["QG"],
		"VG": default_parameters.default_AC_generator_parameters["VG"],
		"APF": default_parameters.default_AC_generator_parameters["APF"],  # Droop parameters
		#3) Scheduling information
		"TIME_GENERATED": default_parameters.default_AC_generator_parameters["TIME_GENERATED"],# Model generated time
		"TIME_APPLIED": default_parameters.default_AC_generator_parameters["TIME_APPLIED"],# Valid period
		"TIME_COMMANDED": default_parameters.default_AC_generator_parameters["TIME_COMMANDED"], # Scheduling command generated time
		"COMMAND_START_UP": default_parameters.default_AC_generator_parameters["COMMAND_START_UP"],# Scheduling command generated time
		"COMMAND_VG": default_parameters.default_AC_generator_parameters["COMMAND_SET_POINT_VG"],# Voltage magnitude set point
		"COMMAND_PG": default_parameters.default_AC_generator_parameters["COMMAND_SET_POINT_PG"],# Active power set point
		"COMMAND_QG": default_parameters.default_AC_generator_parameters["COMMAND_SET_POINT_QG"],# Reactive power set point
		"COMMAND_RG": default_parameters.default_AC_generator_parameters["COMMAND_RESERVE"]
	}

Generator_DC = \
	{   # 1） Static information
		"ID": default_parameters.default_DC_generator_parameters["AREA"],
		"PMAX": default_parameters.default_DC_generator_parameters["PMAX"],
		"PMIN": default_parameters.default_DC_generator_parameters["PMIN"],
		"RAMP_AGC": default_parameters.default_DC_generator_parameters["RAMP_AGC"],
		"RAMP_10": default_parameters.default_DC_generator_parameters["RAMP_10"],
		"COST_START_UP": default_parameters.default_DC_generator_parameters["COST_START_UP"],
		"COST_SHUT_DOWN": default_parameters.default_DC_generator_parameters["COST_SHUT_DOWN"],
		"COST_MODEL": default_parameters.default_DC_generator_parameters["COST_MODEL"],
		"NCOST": default_parameters.default_DC_generator_parameters["NCOST"],
		"COST": default_parameters.default_DC_generator_parameters["COST"],
		# 2） Measurement information
		"STATUS": default_parameters.default_DC_generator_parameters["STATUS"],
		"PG": default_parameters.default_DC_generator_parameters["PG"],
		"VG": default_parameters.default_DC_generator_parameters["VG"],
		"APF": default_parameters.default_DC_generator_parameters["APF"],  # The droop parameters
		# 3） Scheduling information
		"TIME_GENERATED": default_parameters.default_DC_generator_parameters["TIME_GENERATED"],
		"TIME_APPLIED": default_parameters.default_DC_generator_parameters["TIME_APPLIED"],
		"TIME_COMMANDED": default_parameters.default_DC_generator_parameters["TIME_COMMANDED"],
		"COMMAND_START_UP": default_parameters.default_DC_generator_parameters["COMMAND_START_UP"],
		"COMMAND_VG": default_parameters.default_DC_generator_parameters["COMMAND_SET_POINT_VG"],
		"COMMAND_PG": default_parameters.default_DC_generator_parameters["COMMAND_SET_POINT_PG"],
		"COMMAND_RG": default_parameters.default_DC_generator_parameters["COMMAND_RESERVE"]
	}

Generator_RES = \
	{   # 1） Static information
		"ID": default_parameters.default_RES_generator_parameters["AREA"],
		"TYPE": default_parameters.default_RES_generator_parameters["TYPE"],  # 1= PV,2=Wind turbine
		"PMAX": default_parameters.default_RES_generator_parameters["PMAX"],
		"PMIN": default_parameters.default_RES_generator_parameters["PMIN"],
		"QMAX": default_parameters.default_RES_generator_parameters["QMAX"],
		"QMIN": default_parameters.default_RES_generator_parameters["QMIN"],
		"SMAX": default_parameters.default_RES_generator_parameters["SMAX"],
		"COST": default_parameters.default_RES_generator_parameters["COST"],
		# 2） Measurement information
		"STATUS": default_parameters.default_RES_generator_parameters["STATUS"],
		"PG": default_parameters.default_RES_generator_parameters["PG"],
		"QG": default_parameters.default_RES_generator_parameters["QG"],
		# 3） Scheduling information
		"TIME_GENERATED": default_parameters.default_RES_generator_parameters["TIME_GENERATED"],
		"TIME_APPLIED": default_parameters.default_RES_generator_parameters["TIME_APPLIED"],
		"TIME_COMMANDED": default_parameters.default_RES_generator_parameters["TIME_COMMANDED"],
		"COMMAND_CURT": default_parameters.default_RES_generator_parameters["COMMAND_CURT"],
		"COMMAND_PG": default_parameters.default_RES_generator_parameters["COMMAND_SET_POINT_PG"],
	}