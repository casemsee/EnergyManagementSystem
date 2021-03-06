# Default parameters of convertors
import configuration.configuration_time_line as timeline

BIC = \
	{
		"AREA": 1,
		"STATUS": 1,
		"SMAX": 500,
		"EFF_AC2DC": 0.95,
		"EFF_DC2AC": 0.95,
		"P_AC2DC":0,
		"P_DC2AC":0,
		"Q_AC":0,
		"TIME_GENERATED": timeline.default_time["Base_time"],
		"TIME_APPLIED": [timeline.default_time["Base_time"], timeline.default_time["Base_time"]+timeline.default_time["Look_ahead_time_opf"]],
		"TIME_COMMANDED": timeline.default_time["Base_time"],
		"COMMAND_AC2DC": 0,
		"COMMAND_DC2AC": 0,
		"COMMAND_Q": 0,
	}
