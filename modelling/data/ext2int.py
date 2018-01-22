updated_attributes_static_ac_generator = ["ID", "PMIN", "PMAX", "QMIN", "QMAX", "SMAX", "RAMP_AGC", "RAMP_10",
                                                  "COST_START_UP",
                                                  "COST_SHUT_DOWN", "COST_MODEL", "NCOST", "PF_LIMIT", "COST"]

updated_attributes_static_res_generator = ["N", "TYPE", "PMAX", "PMIN", "QMIN", "QMAX", "SMAX", "COST"]

updated_attributes_static_ac_load = ["ID", "PMAX", "PMIN", "FLEX", "MODEL", "COST_MODEL", "NCOST", "COST"]

updated_attributes_static_dc_load = ["ID", "PMAX", "PMIN", "FLEX", "MODEL", "COST_MODEL", "NCOST", "COST"]

updated_attributes_static_ess = ["ID", "CAP", "PMAX_DIS", "PMAX_CH", "EFF_DIS", "EFF_CH", "SOC_MAX", "SOC_MIN",
                                 "COST_MODEL", "NCOST_DIS", "COST_DIS", "NCOST_CH", "COST_CH"]

updated_attributes_static_bic = ["ID", "SMAX", "EFF_AC2DC", "EFF_DC2AC"]



updated_attributes_ac_generator_single_period = ["ID","STATUS", "PG", "QG", "VG", "APF", "COMMAND_START_UP", "COMMAND_VG", "COMMAND_PG","COMMAND_QG","COMMAND_RG"]

updated_attributes_res_generator_single_period = ["N", "PG", "QG", "COMMAND_CURT", "COMMAND_PG"]

updated_attributes_ac_load_single_period = ["ID","STATUS","PD", "QD", "PF", "APF", "COMMAND_PD", "COMMAND_RD"]

updated_attributes_dc_load_single_period = ["ID","STATUS","PD", "COMMAND_PD", "COMMAND_RD"]

updated_attributes_ess_single_period = ["ID", "STATUS", "SOC", "PG", "RG", "COMMAND_PG", "COMMAND_RG"]

updated_attributes_bic_single_period = ["ID","STATUS", "P_AC2DC", "P_DC2AC", "Q_AC","COMMAND_AC2DC","COMMAND_DC2AC","COMMAND_Q"]