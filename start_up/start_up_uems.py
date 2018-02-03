from copy import deepcopy
from modelling.devices import transmission_lines
from configuration.configuration_time_line import default_look_ahead_time_step

def start_up(microgrid, microgrid_middle, microgrid_long):
	"""
	Start up of universal energy management system, which is depended on the start up of local energy management system.
	:param microgrid: short-term information model
	:param microgrid_middle: middle-term information model
	:param microgrid_long: long-term information model
	:return:
	"""
	microgrid = deepcopy(microgrid)

	microgrid["LINE"] = deepcopy(transmission_lines.Line)

	T_middle = default_look_ahead_time_step[
		"Look_ahead_time_ed_time_step"]  # The look ahead time step for middle term operation
	T_long = default_look_ahead_time_step[
		"Look_ahead_time_uc_time_step"]  # The look ahead time step for long term operation

	microgrid_middle = deepcopy(microgrid_middle)
	microgrid_middle["LINE"] = deepcopy(transmission_lines.Line)
	microgrid_middle["LINE"] = [microgrid_middle["LINE"]["STATUS"]] * T_middle

	microgrid_long = deepcopy(microgrid_long)
	microgrid_long["LINE"] = deepcopy(transmission_lines.Line)
	microgrid_long["LINE"] = [microgrid_long["LINE"]["STATUS"]] * T_long

	return microgrid,microgrid_middle,microgrid_long