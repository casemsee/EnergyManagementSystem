"""
Information formulation and extraction for the energy management system
/date: 20 Dec 2017
/version: 1.1
Update: Using setattr and getattr to avoid input error
"""

from configuration.configuration_global import default_operation_mode
from configuration.configuration_global import default_sequence
from modelling.data.ext2int import updated_attributes_static_ac_generator, updated_attributes_static_ess, \
	updated_attributes_static_res_generator, updated_attributes_static_ac_load, updated_attributes_static_dc_load, \
	updated_attributes_static_bic

from modelling.data.ext2int import updated_attributes_ac_generator_single_period, \
	updated_attributes_ac_load_single_period, updated_attributes_bic_single_period, \
	updated_attributes_dc_load_single_period, updated_attributes_ess_single_period, \
	updated_attributes_res_generator_single_period

from copy import deepcopy


def static_information_formulation(microgrid, static_model):
	"""
	Information formulation of local energy management system models
	:param args: microgrid, information model
	:return: formulated microgrid model
	getattrib function is adopted.
	"""
	import time
	info = static_model.microgrid()
	dg_info = static_model.microgrid.DgType()  # The utility grid is modelled as a generation as well.
	ug_info = static_model.microgrid.DgType()  # The utility grid is modelled as a generation as well.
	ess_info = static_model.microgrid.EssType()
	pv_info = static_model.microgrid.PvType()
	wp_info = static_model.microgrid.WpType()
	load_ac_info = static_model.microgrid.Load_AC_Type()
	load_nac_info = static_model.microgrid.Load_AC_Type()
	load_dc_info = static_model.microgrid.Load_DC_Type()
	load_ndc_info = static_model.microgrid.Load_DC_Type()
	bic_info = static_model.microgrid.Convertor_Type()
	# Update the static information
	info.AREA = default_operation_mode["ID"] + 1  # The area information
	info.TIME_STAMP = round(time.time())  # The information generation time

	# The utility grid part
	for i in updated_attributes_static_ac_generator:
		if i in microgrid["UG"]:
			try:
				setattr(ug_info, i, microgrid["UG"][i])
			except:  # The list format
				temp = getattr(ug_info, i)
				temp.extend(microgrid["UG"][i])

	# The diesel generation part
	for i in updated_attributes_static_ac_generator:
		if i in microgrid["DG"]:
			try:
				setattr(dg_info, i, microgrid["DG"][i])
			except:  # The list format
				temp = getattr(dg_info, i)
				temp.extend(microgrid["DG"][i])

	# Add result back to the information set.
	info.dg.extend([ug_info, dg_info])

	# The energy storage system part
	for i in updated_attributes_static_ess:
		if i in microgrid["ESS"]:
			try:
				setattr(ess_info, i, microgrid["ESS"][i])
			except:  # The list format
				temp = getattr(ess_info, i)
				temp.extend(microgrid["ESS"][i])

	info.ess.extend([ess_info])
	# The pv group
	for i in updated_attributes_static_res_generator:
		if i in microgrid["PV"]:
			try:
				setattr(pv_info, i, microgrid["PV"][i])
			except:  # The list format
				temp = getattr(pv_info, i)
				temp.extend(microgrid["PV"][i])

	info.pv.extend([pv_info])
	# The wp group
	for i in updated_attributes_static_res_generator:
		if i in microgrid["WP"]:
			try:
				setattr(wp_info, i, microgrid["WP"][i])
			except:  # The list format
				temp = getattr(wp_info, i)
				temp.extend(microgrid["WP"][i])

	info.wp.extend([wp_info])

	# The load part
	# AC critical load
	for i in updated_attributes_static_ac_load:
		if i in microgrid["Load_ac"]:
			try:
				setattr(load_ac_info, i, microgrid["Load_ac"][i])
			except:  # The list format
				temp = getattr(load_ac_info, i)
				temp.extend(microgrid["Load_ac"][i])
	# AC non-critical load
	for i in updated_attributes_static_ac_load:
		if i in microgrid["Load_nac"]:
			try:
				setattr(load_nac_info, i, microgrid["Load_nac"][i])
			except:  # The list format
				temp = getattr(load_nac_info, i)
				temp.extend(microgrid["Load_nac"][i])
	info.load_ac.extend([load_ac_info, load_nac_info])

	# DC critial load
	for i in updated_attributes_static_dc_load:
		if i in microgrid["Load_dc"]:
			try:
				setattr(load_dc_info, i, microgrid["Load_dc"][i])
			except:  # The list format
				temp = getattr(load_dc_info, i)
				temp.extend(microgrid["Load_dc"][i])
	# DC non-critical load
	for i in updated_attributes_static_dc_load:
		if i in microgrid["Load_ndc"]:
			try:
				setattr(load_ndc_info, i, microgrid["Load_ndc"][i])
			except:  # The list format
				temp = getattr(load_ndc_info, i)
				temp.extend(microgrid["Load_ndc"][i])

	info.load_dc.extend([load_dc_info, load_ndc_info])

	# BIC information
	for i in updated_attributes_static_bic:
		if i in microgrid["BIC"]:
			try:
				setattr(bic_info, i, microgrid["BIC"][i])
			except:  # The list format
				temp = getattr(bic_info, i)
				temp.extend(microgrid["BIC"][i])

	info.bic.extend([bic_info])

	return info  # The information structure.


def static_information_update(microgrid, info, logger):
	"""
	Information update of local energy management system models
	:param args: microgrid, information model, logger
	:return: updated microgrid model
	getattrib function is adopted.
	"""
	microgrid = deepcopy(microgrid)
	microgrid["AREA"] = info.AREA
	microgrid["TIME_STAMP"] = info.TIME_STAMP
	# Update the utility grid group
	for i in updated_attributes_static_ac_generator:
		if i in microgrid["UG"]:  # Update the attribute value of given attributes list
			temp = getattr(info.dg[default_sequence["UG"]], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["UG"][i] = temp
			else:
				try:
					microgrid["UG"][i] = temp._values
				except:
					logger.warning("The protocol buffer model of UG has been changed!")

	for i in updated_attributes_static_ac_generator:
		if i in microgrid["DG"]:  # Update the attribute value of given attributes list
			temp = getattr(info.dg[default_sequence["DG"]], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["DG"][i] = temp
			else:
				try:
					microgrid["DG"][i] = temp._values
				except:
					logger.warning("The protocol buffer model of DG has been changed!")
	# Update the energy storage system group
	for i in updated_attributes_static_ess:
		if i in microgrid["ESS"]:  # Update the attribute value of given attributes list
			temp = getattr(info.ess[0], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["ESS"][i] = temp
			else:
				try:
					microgrid["ESS"][i] = temp._values
				except:
					logger.warning("The protocol buffer model of ESS has been changed!")

	# Update the photovoltaic generator grid group
	for i in updated_attributes_static_res_generator:
		if i in microgrid["PV"]:  # Update the attribute value of given attributes list
			temp = getattr(info.pv[0], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["PV"][i] = temp
			else:
				try:
					microgrid["PV"][i] = temp._values
				except:
					logger.warning("The protocol buffer model of PV has been changed!")

	for i in updated_attributes_static_res_generator:
		if i in microgrid["WP"]:  # Update the attribute value of given attributes list
			temp = getattr(info.wp[0], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["WP"][i] = temp
			else:
				try:
					microgrid["WP"][i] = temp._values
				except:
					logger.warning("The protocol buffer model of WP has been changed!")

	# Update the critical AC load group
	for i in updated_attributes_static_ac_load:
		if i in microgrid["Load_ac"]:  # Update the attribute value of given attributes list
			temp = getattr(info.load_ac[default_sequence["CRI"]], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["Load_ac"][i] = temp
			else:
				try:
					microgrid["Load_ac"][i] = temp._values
				except:
					logger.warning("The protocol buffer model of Load_ac has been changed!")

	# Update the non-critical AC load group
	for i in updated_attributes_static_ac_load:
		if i in microgrid["Load_nac"]:  # Update the attribute value of given attributes list
			temp = getattr(info.load_ac[default_sequence["NON_CRI"]], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["Load_nac"][i] = temp
			else:
				try:
					microgrid["Load_nac"][i] = temp._values
				except:
					logger.warning("The protocol buffer model of Load_nac has been changed!")

	# Update the critical DC load group
	for i in updated_attributes_static_dc_load:
		if i in microgrid["Load_dc"]:  # Update the attribute value of given attributes list
			temp = getattr(info.load_dc[default_sequence["CRI"]], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["Load_dc"][i] = temp
			else:
				try:
					microgrid["Load_dc"][i] = temp._values
				except:
					logger.warning("The protocol buffer model of Load_dc has been changed!")

	# Update the non-critical DC load group
	for i in updated_attributes_static_dc_load:
		if i in microgrid["Load_nac"]:  # Update the attribute value of given attributes list
			temp = getattr(info.load_dc[default_sequence["NON_CRI"]], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["Load_nac"][i] = temp
			else:
				try:
					microgrid["Load_nac"][i] = temp._values
				except:
					logger.warning("The protocol buffer model of Load_nac has been changed!")

	# Update the bi-directional convertor group
	for i in updated_attributes_static_bic:
		if i in microgrid["BIC"]:  # Update the attribute value of given attributes list
			temp = getattr(info.bic[0], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["BIC"][i] = temp
			else:
				try:
					microgrid["BIC"][i] = temp._values
				except:
					logger.warning("The protocol buffer model of BIC has been changed!")
	# Return result
	return microgrid


def single_period_information_formulation(microgrid, info, Target_time):
	"""
	single period information model formulation
	:param microgrid: The target ems model
	:param info: The information format
	:param Target_time: Valid time of the ems model
	:return:
	"""
	# 1) Initial dynamic model
	dynamic_info = info
	#################################The information structure
	ug_info = info.DgType()
	dg_info = info.DgType()
	ess_info = info.EssType()
	pv_info = info.PvType()
	wp_info = info.WpType()
	load_ac_info = info.Load_AC_Type()
	load_dc_info = info.Load_DC_Type()
	load_nac_info = info.Load_AC_Type()
	load_ndc_info = info.Load_DC_Type()
	bic_info = info.Convertor_Type()

	# Obtain information from the external systems
	dynamic_info.AREA = microgrid["AREA"]
	dynamic_info.TIME_STAMP = microgrid["TIME_STAMP"]
	# The utility grid part
	for i in updated_attributes_ac_generator_single_period:
		if i in microgrid["UG"]:
			try:
				setattr(ug_info, i, microgrid["UG"][i])
			except:  # The list format
				temp = getattr(ug_info, i)
				temp.extend(microgrid["UG"][i])

	# The diesel generation part
	for i in updated_attributes_ac_generator_single_period:
		if i in microgrid["DG"]:
			try:
				setattr(dg_info, i, microgrid["DG"][i])
			except:  # The list format
				temp = getattr(dg_info, i)
				temp.extend(microgrid["DG"][i])

	# Add result back to the information set.
	dynamic_info.dg.extend([ug_info, dg_info])

	# The energy storage system part
	for i in updated_attributes_ess_single_period:
		if i in microgrid["ESS"]:
			try:
				setattr(ess_info, i, microgrid["ESS"][i])
			except:  # The list format
				temp = getattr(ess_info, i)
				temp.extend(microgrid["ESS"][i])

	dynamic_info.ess.extend([ess_info])
	# The pv group
	for i in updated_attributes_res_generator_single_period:
		if i in microgrid["PV"]:
			try:
				setattr(pv_info, i, microgrid["PV"][i])
			except:  # The list format
				temp = getattr(pv_info, i)
				temp.extend(microgrid["PV"][i])

	dynamic_info.pv.extend([pv_info])
	# The wp group
	for i in updated_attributes_res_generator_single_period:
		if i in microgrid["WP"]:
			try:
				setattr(wp_info, i, microgrid["WP"][i])
			except:  # The list format
				temp = getattr(wp_info, i)
				temp.extend(microgrid["WP"][i])

	dynamic_info.wp.extend([wp_info])

	# The load part
	# AC critical load
	for i in updated_attributes_ac_load_single_period:
		if i in microgrid["Load_ac"]:
			try:
				setattr(load_ac_info, i, microgrid["Load_ac"][i])
			except:  # The list format
				temp = getattr(load_ac_info, i)
				temp.extend(microgrid["Load_ac"][i])
	# AC non-critical load
	for i in updated_attributes_ac_load_single_period:
		if i in microgrid["Load_nac"]:
			try:
				setattr(load_nac_info, i, microgrid["Load_nac"][i])
			except:  # The list format
				temp = getattr(load_nac_info, i)
				temp.extend(microgrid["Load_nac"][i])
	dynamic_info.load_ac.extend([load_ac_info, load_nac_info])

	# DC critial load
	for i in updated_attributes_dc_load_single_period:
		if i in microgrid["Load_dc"]:
			try:
				setattr(load_dc_info, i, microgrid["Load_dc"][i])
			except:  # The list format
				temp = getattr(load_dc_info, i)
				temp.extend(microgrid["Load_dc"][i])
	# DC non-critical load
	for i in updated_attributes_dc_load_single_period:
		if i in microgrid["Load_ndc"]:
			try:
				setattr(load_ndc_info, i, microgrid["Load_ndc"][i])
			except:  # The list format
				temp = getattr(load_ndc_info, i)
				temp.extend(microgrid["Load_ndc"][i])

	dynamic_info.load_dc.extend([load_dc_info, load_ndc_info])

	# BIC information
	for i in updated_attributes_bic_single_period:
		if i in microgrid["BIC"]:
			try:
				setattr(bic_info, i, microgrid["BIC"][i])
			except:  # The list format
				temp = getattr(bic_info, i)
				temp.extend(microgrid["BIC"][i])

	info.bic.extend([bic_info])

	dynamic_info.PMG = microgrid["PMG"]
	dynamic_info.V_DC = microgrid["V_DC"]

	dynamic_info.COMMAND_TYPE = microgrid["COMMAND_TYPE"]
	dynamic_info.COMMAND_TIME_STAMP = Target_time
	dynamic_info.COST = microgrid["COST"]

	return dynamic_info


def single_period_information_update(microgrid, info):
	"""
	single period information model update
	:param microgrid: Target model
	:param info: The received information
	:return:
	"""

	# The utility grid part
	microgrid = deepcopy(microgrid)
	microgrid["AREA"] = info.AREA
	microgrid["TIME_STAMP"] = info.COMMAND_TIME_STAMP
	microgrid["COST"] = info.COST
	microgrid["V_DC"]= info.V_DC
	# Update the utility grid group
	for i in updated_attributes_ac_generator_single_period:
		if i in microgrid["UG"]:  # Update the attribute value of given attributes list
			temp = getattr(info.dg[default_sequence["UG"]], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["UG"][i] = temp
			else:
				microgrid["UG"][i] = temp._values

	for i in updated_attributes_ac_generator_single_period:
		if i in microgrid["DG"]:  # Update the attribute value of given attributes list
			temp = getattr(info.dg[default_sequence["DG"]], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["DG"][i] = temp
			else:
				microgrid["DG"][i] = temp._values
	# Update the energy storage system group
	for i in updated_attributes_ess_single_period:
		if i in microgrid["ESS"]:  # Update the attribute value of given attributes list
			temp = getattr(info.ess[0], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["ESS"][i] = temp
			else:
				microgrid["ESS"][i] = temp._values

	# Update the photovoltaic generator grid group
	for i in updated_attributes_res_generator_single_period:
		if i in microgrid["PV"]:  # Update the attribute value of given attributes list
			temp = getattr(info.pv[0], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["PV"][i] = temp
			else:
				microgrid["PV"][i] = temp._values

	for i in updated_attributes_res_generator_single_period:
		if i in microgrid["WP"]:  # Update the attribute value of given attributes list
			temp = getattr(info.wp[0], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["WP"][i] = temp
			else:
				microgrid["WP"][i] = temp._values


	# Update the critical AC load group
	for i in updated_attributes_ac_load_single_period:
		if i in microgrid["Load_ac"]:  # Update the attribute value of given attributes list
			temp = getattr(info.load_ac[default_sequence["CRI"]], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["Load_ac"][i] = temp
			else:
				microgrid["Load_ac"][i] = temp._values

	# Update the non-critical AC load group
	for i in updated_attributes_ac_load_single_period:
		if i in microgrid["Load_nac"]:  # Update the attribute value of given attributes list
			temp = getattr(info.load_ac[default_sequence["NON_CRI"]], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["Load_nac"][i] = temp
			else:
				microgrid["Load_nac"][i] = temp._values

	# Update the critical DC load group
	for i in updated_attributes_dc_load_single_period:
		if i in microgrid["Load_dc"]:  # Update the attribute value of given attributes list
			temp = getattr(info.load_dc[default_sequence["CRI"]], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["Load_dc"][i] = temp
			else:
				microgrid["Load_dc"][i] = temp._values

	# Update the non-critical DC load group
	for i in updated_attributes_dc_load_single_period:
		if i in microgrid["Load_nac"]:  # Update the attribute value of given attributes list
			temp = getattr(info.load_dc[default_sequence["NON_CRI"]], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["Load_nac"][i] = temp
			else:
				microgrid["Load_nac"][i] = temp._values

	# Update the bi-directional convertor group
	for i in updated_attributes_static_bic:
		if i in microgrid["BIC"]:  # Update the attribute value of given attributes list
			temp = getattr(info.bic[0], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["BIC"][i] = temp
			else:
				microgrid["BIC"][i] = temp._values

	microgrid["COMMAND_TYPE"] = info.COMMAND_TYPE

	return microgrid

def multiple_periods_information_formulation(*args):
	# Dynamic information formulation
	microgrid = args[0]
	info = args[1]
	Target_time = args[2]
	# 1) Initial dynamic model
	dynamic_info = info  # The input should be a empty data structure
	###########The information structure
	ug_info = info.DgType()
	dg_info = info.DgType()
	ess_info = info.EssType()
	pv_info = info.PvType()
	wp_info = info.WpType()
	load_ac_info = info.Load_AC_Type()
	load_dc_info = info.Load_DC_Type()
	load_nac_info = info.Load_AC_Type()
	load_ndc_info = info.Load_DC_Type()
	bic_info = info.Convertor_Type()

	# Obtain information from the external systems
	dynamic_info.AREA = microgrid["AREA"]
	dynamic_info.TIME_STAMP = Target_time
	# The utility grid part
	for i in updated_attributes_ac_generator_single_period:
		if i in microgrid["UG"]:
			try:
				setattr(ug_info, i, microgrid["UG"][i])
			except:  # The list format
				temp = getattr(ug_info, i)
				temp.extend(microgrid["UG"][i])

	# The diesel generation part
	for i in updated_attributes_ac_generator_single_period:
		if i in microgrid["DG"]:
			try:
				setattr(dg_info, i, microgrid["DG"][i])
			except:  # The list format
				temp = getattr(dg_info, i)
				temp.extend(microgrid["DG"][i])

	# Add result back to the information set.
	dynamic_info.dg.extend([ug_info, dg_info])

	# The energy storage system part
	for i in updated_attributes_ess_single_period:
		if i in microgrid["ESS"]:
			try:
				setattr(ess_info, i, microgrid["ESS"][i])
			except:  # The list format
				temp = getattr(ess_info, i)
				temp.extend(microgrid["ESS"][i])

	dynamic_info.ess.extend([ess_info])
	# The pv group
	for i in updated_attributes_res_generator_single_period:
		if i in microgrid["PV"]:
			try:
				setattr(pv_info, i, microgrid["PV"][i])
			except:  # The list format
				temp = getattr(pv_info, i)
				temp.extend(microgrid["PV"][i])

	dynamic_info.pv.extend([pv_info])
	# The wp group
	for i in updated_attributes_res_generator_single_period:
		if i in microgrid["WP"]:
			try:
				setattr(wp_info, i, microgrid["WP"][i])
			except:  # The list format
				temp = getattr(wp_info, i)
				temp.extend(microgrid["WP"][i])

	dynamic_info.wp.extend([wp_info])

	# The load part
	# AC critical load
	for i in updated_attributes_ac_load_single_period:
		if i in microgrid["Load_ac"]:
			try:
				setattr(load_ac_info, i, microgrid["Load_ac"][i])
			except:  # The list format
				temp = getattr(load_ac_info, i)
				temp.extend(microgrid["Load_ac"][i])
	# AC non-critical load
	for i in updated_attributes_ac_load_single_period:
		if i in microgrid["Load_nac"]:
			try:
				setattr(load_nac_info, i, microgrid["Load_nac"][i])
			except:  # The list format
				temp = getattr(load_nac_info, i)
				temp.extend(microgrid["Load_nac"][i])
	dynamic_info.load_ac.extend([load_ac_info, load_nac_info])

	# DC critial load
	for i in updated_attributes_dc_load_single_period:
		if i in microgrid["Load_dc"]:
			try:
				setattr(load_dc_info, i, microgrid["Load_dc"][i])
			except:  # The list format
				temp = getattr(load_dc_info, i)
				temp.extend(microgrid["Load_dc"][i])
	# DC non-critical load
	for i in updated_attributes_dc_load_single_period:
		if i in microgrid["Load_ndc"]:
			try:
				setattr(load_ndc_info, i, microgrid["Load_ndc"][i])
			except:  # The list format
				temp = getattr(load_ndc_info, i)
				temp.extend(microgrid["Load_ndc"][i])

	dynamic_info.load_dc.extend([load_dc_info, load_ndc_info])

	# BIC information
	for i in updated_attributes_bic_single_period:
		if i in microgrid["BIC"]:
			try:
				setattr(bic_info, i, microgrid["BIC"][i])
			except:  # The list format
				temp = getattr(bic_info, i)
				temp.extend(microgrid["BIC"][i])

	info.bic.extend([bic_info])

	dynamic_info.PMG.extend(microgrid["PMG"])
	dynamic_info.V_DC.extend(microgrid["V_DC"])
	dynamic_info.COST.extend(microgrid["COST"])
	dynamic_info.COMMAND_TYPE = microgrid["COMMAND_TYPE"]
	dynamic_info.COMMAND_TIME_STAMP = Target_time

	return dynamic_info


def multiple_periods_information_update(*args):
	microgrid = deepcopy(args[0])
	info = args[1]
	# The utility grid part
	microgrid = deepcopy(microgrid)
	microgrid["AREA"] = info.AREA
	microgrid["TIME_STAMP"] = info.COMMAND_TIME_STAMP
	microgrid["COST"] = info.COST._values
	microgrid["V_DC"] = info.V_DC._values
	microgrid["COMMAND_TYPE"] = info.COMMAND_TYPE
	microgrid["PMG"] = info.PMG._values

	# Update the utility grid group
	for i in updated_attributes_ac_generator_single_period:
		if i in microgrid["UG"]:  # Update the attribute value of given attributes list
			temp = getattr(info.dg[default_sequence["UG"]], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["UG"][i] = temp
			else:
				microgrid["UG"][i] = temp._values

	for i in updated_attributes_ac_generator_single_period:
		if i in microgrid["DG"]:  # Update the attribute value of given attributes list
			temp = getattr(info.dg[default_sequence["DG"]], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["DG"][i] = temp
			else:
				microgrid["DG"][i] = temp._values
	# Update the energy storage system group
	for i in updated_attributes_ess_single_period:
		if i in microgrid["ESS"]:  # Update the attribute value of given attributes list
			temp = getattr(info.ess[0], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["ESS"][i] = temp
			else:
				microgrid["ESS"][i] = temp._values

	# Update the photovoltaic generator grid group
	for i in updated_attributes_res_generator_single_period:
		if i in microgrid["PV"]:  # Update the attribute value of given attributes list
			temp = getattr(info.pv[0], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["PV"][i] = temp
			else:
				microgrid["PV"][i] = temp._values

	for i in updated_attributes_res_generator_single_period:
		if i in microgrid["WP"]:  # Update the attribute value of given attributes list
			temp = getattr(info.wp[0], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["WP"][i] = temp
			else:
				microgrid["WP"][i] = temp._values


	# Update the critical AC load group
	for i in updated_attributes_ac_load_single_period:
		if i in microgrid["Load_ac"]:  # Update the attribute value of given attributes list
			temp = getattr(info.load_ac[default_sequence["CRI"]], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["Load_ac"][i] = temp
			else:
				microgrid["Load_ac"][i] = temp._values

	# Update the non-critical AC load group
	for i in updated_attributes_ac_load_single_period:
		if i in microgrid["Load_nac"]:  # Update the attribute value of given attributes list
			temp = getattr(info.load_ac[default_sequence["NON_CRI"]], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["Load_nac"][i] = temp
			else:
				microgrid["Load_nac"][i] = temp._values

	# Update the critical DC load group
	for i in updated_attributes_dc_load_single_period:
		if i in microgrid["Load_dc"]:  # Update the attribute value of given attributes list
			temp = getattr(info.load_dc[default_sequence["CRI"]], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["Load_dc"][i] = temp
			else:
				microgrid["Load_dc"][i] = temp._values

	# Update the non-critical DC load group
	for i in updated_attributes_dc_load_single_period:
		if i in microgrid["Load_nac"]:  # Update the attribute value of given attributes list
			temp = getattr(info.load_dc[default_sequence["NON_CRI"]], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["Load_nac"][i] = temp
			else:
				microgrid["Load_nac"][i] = temp._values

	# Update the bi-directional convertor group
	for i in updated_attributes_static_bic:
		if i in microgrid["BIC"]:  # Update the attribute value of given attributes list
			temp = getattr(info.bic[0], i, 0)
			if type(temp) is float or type(temp) is int:
				microgrid["BIC"][i] = temp
			else:
				microgrid["BIC"][i] = temp._values


	return microgrid
