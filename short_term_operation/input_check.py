# The input information check function for the optimal power flow
# Two types of information will be checked, shown as follows.
# 1) universal model, which contains the connection and topology information within the microgrid parks
# 2) local model, which contains the local sources information

# The following rules are used
# 1) Online status of generators
# 2) Capacity

# Important notice:
# The input check is the oriented from 1） the start-up of the local ems and universal ems
# 2） modelling of each equipment

from copy import deepcopy
from configuration.configuration_time_line import default_look_ahead_time_step
from utils import Logger

logger = Logger("Short_term_dispatch_input_check")
from configuration import configuration_default_generators, configuration_default_load, configuration_convertors, \
    configuration_default_lines


class InputCheckShortTerm():
    def model_local_check(*args):
        model = deepcopy(args[0])  # The input model
        T_short = default_look_ahead_time_step[
            "Look_ahead_time_opf_time_step"]  # The look ahead time step for short term operation
        # 1) The input check of utility grid
        if type(model["UG"]["STATUS"]) is not int and type(model["UG"]["STATUS"]) is not float and type(
                model["UG"]["STATUS"]) is not bool:
            logger.error("The type of utility grid status is incorrect!")
            logger.info("The status of utility grid has been reset to online!")
            model["UG"]["STATUS"] = 1

        if type(model["UG"]["PMAX"]) is not float and type(model["UG"]["PMAX"]) is not int:
            logger.error("The data format of utility grid capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of utility grid")
                model["UG"]["PMAX"] = model["UG"]["PMAX"][0]
            except:
                logger.info(
                    "The correction of utility grid capacity failed! Restore it to default value in configuration file!")
                model["UG"]["PMAX"] = configuration_default_generators.default_AC_generator_parameters["PMAX"]
        if type(model["UG"]["PMIN"]) is not float and type(model["UG"]["PMIN"]) is not int:
            logger.error("The data format of utility grid capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of utility grid")
                model["UG"]["PMIN"] = model["UG"]["PMIN"][0]
            except:
                logger.info(
                    "The correction of utility grid capacity failed! Restore it to default value in configuration file!")
                model["UG"]["PMIN"] = configuration_default_generators.default_AC_generator_parameters["PMIN"]
        if model["UG"]["PMIN"] > model["UG"]["PMAX"]:
            logger.error("The maximal capacity of UG is smaller than the minimal capacity!")
            logger.info("Correct the capacity to its lower boundary!")
            model["UG"]["PMIN"] = model["UG"]["PMAX"]
        if model["UG"]["QMIN"] > model["UG"]["QMAX"]:
            logger.error("The maximal reactive power capacity of UG is smaller than the minimal capacity!")
            logger.info("Correct the reactive power capacity to its lower boundary!")
            model["UG"]["QMIN"] = model["UG"]["QMAX"]

        # 2) The input check of diesel generator
        if type(model["DG"]["STATUS"]) is not int and type(model["DG"]["STATUS"]) is not float and type(
                model["DG"]["STATUS"]) is not bool:
            logger.error("The size of diesel generator status is incorrect!")
            logger.info("The status of diesel generator has been reset to online!")
            model["DG"]["STATUS"] = 1

        if type(model["DG"]["PMAX"]) is not float and type(model["DG"]["PMAX"]) is not int:
            logger.error("The data format of diesel generator capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of diesel generator")
                model["DG"]["PMAX"] = model["DG"]["PMAX"][0]
            except:
                logger.info(
                    "The correction of diesel generator capacity failed! Restore it to default value in configuration file!")
                model["DG"]["PMAX"] = configuration_default_generators.default_AC_generator_parameters["PMAX"]
        if type(model["DG"]["PMIN"]) is not float and type(model["DG"]["PMIN"]) is not int:
            logger.error("The data format of diesel generator capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of diesel generator")
                model["DG"]["PMIN"] = model["DG"]["PMIN"][0]
            except:
                logger.info(
                    "The correction of diesel generator capacity failed! Restore it to default value in configuration file!")
                model["DG"]["PMIN"] = configuration_default_generators.default_AC_generator_parameters["PMIN"]
        if model["DG"]["PMIN"] > model["DG"]["PMAX"]:
            logger.error("The maximal capacity of UG is smaller than the minimal capacity!")
            model["DG"]["PMIN"] = model["DG"]["PMAX"]
        if model["DG"]["QMIN"] > model["DG"]["QMAX"]:
            logger.error("The maximal reactive power capacity of UG is smaller than the minimal capacity!")
            model["DG"]["QMIN"] = model["DG"]["QMAX"]

        # 3) The input check of photovoltaic generators
        if type(model["PV"]["N"]) is not float and type(model["PV"]["N"]) is not int:
            logger.error("The size of photovoltaic generator status is incorrect!")
            logger.info("The status of photovoltaic generator has been reset to online!")
            model["PV"]["N"] = [configuration_default_generators.default_RES_generator_parameters["PMAX"]] * T_short
        if type(model["PV"]["PMAX"]) is not float and type(model["PV"]["PMAX"]) is not int:
            logger.error("The data format of photovoltaic generator capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of photovoltaic generator")
                model["PV"]["PMAX"] = model["PV"]["PMAX"][0]
            except:
                logger.info(
                    "The correction of photovoltaic generator capacity failed! Restore it to default value in configuration file!")
                model["PV"]["PMAX"] = configuration_default_generators.default_RES_generator_parameters["PMAX"]
        if type(model["PV"]["PMIN"]) is not float and type(model["PV"]["PMIN"]) is not int:
            logger.error("The data format of photovoltaic generator capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of photovoltaic generator")
                model["PV"]["PMIN"] = model["PV"]["PMIN"][0]
            except:
                logger.info(
                    "The correction of photovoltaic generator capacity failed! Restore it to default value in configuration file!")
                model["PV"]["PMIN"] = configuration_default_generators.default_RES_generator_parameters["PMIN"]
        if model["PV"]["PMIN"] > model["PV"]["PMAX"]:
            logger.error("The maximal capacity of PV is smaller than the minimal capacity!")
            model["PV"]["PMIN"] = model["PV"]["PMAX"]
        if model["PV"]["PG"] > model["PV"]["PMAX"]:
            logger.error("The output of PV is out of boundary!")
            model["PV"]["PG"] = model["PV"]["PMAX"]
        if model["PV"]["QMIN"] > model["PV"]["QMAX"]:
            logger.error("The maximal reactive power capacity of PV is smaller than the minimal capacity!")
            model["PV"]["QMIN"] = model["PV"]["QMAX"]

        # 4) The input check of wind turbine generators
        if type(model["WP"]["N"]) is not int and type(model["WP"]["N"]) is not float:
            logger.error("The size of WP status is incorrect!")
            logger.info("The status of WP has been reset to online!")
            model["WP"]["N"] = [configuration_default_generators.default_RES_generator_parameters["PMAX"]] * T_short
        if type(model["WP"]["PMAX"]) is not float and type(model["WP"]["PMAX"]) is not int:
            logger.error("The data format of WP capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of WP")
                model["WP"]["PMAX"] = model["WP"]["PMAX"][0]
            except:
                logger.info("The correction of WP capacity failed! Restore it to default value in configuration file!")
                model["WP"]["PMAX"] = configuration_default_generators.default_RES_generator_parameters["PMAX"]
        if type(model["WP"]["PMIN"]) is not float and type(model["WP"]["PMIN"]) is not int:
            logger.error("The data format of WP is incorrect!")
            try:
                logger.warning("Try to fix the capacity of WP.")
                model["WP"]["PMIN"] = model["WP"]["PMIN"][0]
            except:
                logger.info("The correction of WP capacity failed! Restore it to default value in configuration file!")
                model["WP"]["PMIN"] = configuration_default_generators.default_RES_generator_parameters["PMIN"]
        if model["WP"]["PMIN"] > model["WP"]["PMAX"]:
            logger.error("The maximal capacity of WP is smaller than the minimal capacity!")
            model["WP"]["PMIN"] = model["WP"]["PMAX"]
        if model["WP"]["QMIN"] > model["WP"]["QMAX"]:
            logger.error("The maximal reactive power capacity of WP is smaller than the minimal capacity!")
            model["WP"]["QMIN"] = model["WP"]["QMAX"]
        if model["WP"]["PG"] > model["WP"]["PMAX"]:
            logger.error("The output of WP is out of boundary!")
            model["WP"]["PG"] = model["WP"]["PMAX"]

        # 5) The input check of critical AC load
        if type(model["Load_ac"]["STATUS"]) is not float and type(model["Load_ac"]["STATUS"]) is not int and type(
                model["Load_ac"]["STATUS"]) is not bool:
            logger.error("The size of critical AC load status is incorrect!")
            logger.info("The status of critical AC load has been reset to default value!")
            model["Load_ac"]["STATUS"] = configuration_default_load.default_Load_AC["STATUS"]
        if type(model["Load_ac"]["PD"]) is not float and type(model["Load_ac"]["PD"]) is not int:
            logger.error("The size of critical AC load profile is incorrect!")
            logger.info("The profile of critical AC load has been reset to default value!")
            model["Load_ac"]["PD"] = configuration_default_load.default_Load_AC["PD"]
        if model["Load_ac"]["PD"]>model["Load_ac"]["PMAX"]:
            logger.error("The critical AC load profile is overcurrent!")
            model["Load_ac"]["PD"] = model["Load_ac"]["PMAX"]


        # 6) The input check of non-critical AC load
        if type(model["Load_nac"]["STATUS"]) is not int and type(model["Load_nac"]["STATUS"]) is not float and type(
                model["Load_nac"]["STATUS"]) is not bool:
            logger.error("The size of non-critical AC load status is incorrect!")
            logger.info("The status of non-critical AC load has been reset to default value!")
            model["Load_nac"]["STATUS"] = configuration_default_load.default_Load_AC["STATUS"]
        if type(model["Load_nac"]["PD"]) is not float and type(model["Load_nac"]["PD"]) is not int:
            logger.error("The size of non-critical AC load profile is incorrect!")
            logger.info("The profile of non-critical AC load has been reset to online!")
            model["Load_nac"]["PD"] = configuration_default_load.default_Load_AC["PD"]
        if model["Load_nac"]["PD"]>model["Load_nac"]["PMAX"]:
            logger.error("The non-critical AC load profile is overcurrent!")
            model["Load_nac"]["PD"] = model["Load_nac"]["PMAX"]

        # 7) The input check of critical AC load
        if type(model["Load_dc"]["STATUS"]) is not int and type(model["Load_dc"]["STATUS"]) is not float and type(
                model["Load_dc"]["STATUS"]) is not bool:
            logger.error("The size of critical DC load status is incorrect!")
            logger.info("The status of critical DC load has been reset to default value!")
            model["Load_dc"]["STATUS"] = configuration_default_load.default_Load_DC["STATUS"]
        if type(model["Load_dc"]["PD"]) is not int and type(model["Load_dc"]["PD"]) is not float:
            logger.error("The size of critical DC load profile is incorrect!")
            logger.info("The profile of critical DC load has been reset to default value!")
            model["Load_dc"]["PD"] = configuration_default_load.default_Load_DC["PD"]
        if model["Load_dc"]["PD"]>model["Load_dc"]["PMAX"]:
            logger.error("The critical DC load profile is overcurrent!")
            model["Load_dc"]["PD"] = model["Load_dc"]["PMAX"]
        # 8) The input check of non-critical AC load
        if type(model["Load_ndc"]["STATUS"]) is not int and type(model["Load_ndc"]["STATUS"]) is not float and type(
                model["Load_ndc"]["STATUS"]) is not bool:
            logger.error("The size of non-critical DC load status is incorrect!")
            logger.info("The status of non-critical DC load has been reset to default value!")
            model["Load_ndc"]["STATUS"] = configuration_default_load.default_Load_DC["STATUS"]
        if type(model["Load_ndc"]["PD"]) is not float and type(model["Load_ndc"]["PD"]) is not int:
            logger.error("The size of non-critical DC load profile is incorrect!")
            logger.info("The profile of non-critical DC load has been reset to online!")
            model["Load_ndc"]["PD"] = configuration_default_load.default_Load_DC["PD"]
        if model["Load_ndc"]["PD"]>model["Load_ndc"]["PMAX"]:
            logger.error("The non-critical DC load profile is overcurrent!")
            model["Load_ndc"]["PD"] = model["Load_ndc"]["PMAX"]

        # 9) The input check for BIC convertors
        if type(model["BIC"]["STATUS"]) is not float and type(model["BIC"]["STATUS"]) is not int:
            logger.error("The size of BIC status is incorrect!")
            logger.info("The status of BIC has been reset to default value!")
            model["BIC"]["STATUS"] = configuration_convertors.BIC["STATUS"]

        # 10) The input check for ESSs
        if type(model["ESS"]["STATUS"]) is not float and type(model["ESS"]["STATUS"]) is not int:
            logger.error("The size of ESS status is incorrect!")
            logger.info("The status of ESS has been reset to default value!")
            model["ESS"]["STATUS"] = 1

        # 11) The input check for ESSs
        if model["ESS"]["SOC"] < model["ESS"]["SOC_MIN"]:
            logger.error("BAT SOC is out of boundary!")
            logger.info("The SOC of BAT has been reset to lower boundary!")
            model["ESS"]["SOC"] = (model["ESS"]["SOC_MIN"] + model["ESS"]["SOC_MAX"]) / 2

        if model["ESS"]["SOC"] > model["ESS"]["SOC_MAX"]:
            logger.error("BAT SOC is out of boundary!")
            logger.info("The SOC of BAT has been reset to upper boundary!")
            model["ESS"]["SOC"] = (model["ESS"]["SOC_MIN"] + model["ESS"]["SOC_MAX"]) / 2

        return model

    def model_universal_check(*args):
        model = deepcopy(args[0])  # The input model

        T_short = default_look_ahead_time_step[
            "Look_ahead_time_opf_time_step"]  # The look ahead time step for short term operation
        model = InputCheckShortTerm.model_local_check(model)

        # 1) The input check for transmission lines
        if type(model["LINE"]["STATUS"]) is not float and type(model["LINE"]["STATUS"]) is not int:
            logger.error("The size of  transmission line status is incorrect!")
            logger.info("The status of transmission line has been reset to default value!")
            model["LINE"]["STATUS"] = configuration_default_lines.default_Line["STATUS"]

        return model
