# A linear constrained convex quadratic programming method is proposed for the economic dispatch
# To simplify the problem, some more general problems can be mixed integer linear programing problem.

from numpy import array, vstack, zeros
import numpy
from copy import deepcopy
from configuration import configuration_time_line

class ProblemFormulation():
	"""
	Problem formulation class for economic dispatch
	"""
	def problem_formulation_local(*args):
		from modelling.data.idx_ed_foramt import PG, RG, PUG, RUG, PBIC_AC2DC, PBIC_DC2AC, PESS_C, \
			PESS_DC, RESS, EESS, PMG, NX
		model = deepcopy(args[0])  # If multiple models are inputed, more local ems models will be formulated
		T = configuration_time_line.default_look_ahead_time_step["Look_ahead_time_ed_time_step"]
		nx = NX * T

		lb = [0] * NX
		ub = [0] * NX
		## Update lower boundary
		lb[PG] = model["DG"]["PMIN"]
		lb[RG] = model["DG"]["PMIN"]

		lb[PUG] = model["UG"]["PMIN"]
		lb[RUG] = model["UG"]["PMIN"]

		lb[PBIC_AC2DC] = 0
		lb[PBIC_DC2AC] = 0

		lb[PESS_C] = 0
		lb[PESS_DC] = 0
		lb[RESS] = 0
		lb[EESS] = model["ESS"]["SOC_MIN"] * model["ESS"]["CAP"]

		lb[PMG] = 0  # The line flow limitation, the predefined status is, the transmission line is off-line

		## Update lower boundary
		ub[PG] = model["DG"]["PMAX"]
		ub[RG] = model["DG"]["PMAX"]

		ub[PUG] = model["UG"]["PMAX"]
		ub[RUG] = model["UG"]["PMAX"]

		ub[PBIC_AC2DC] = model["BIC"]["SMAX"]
		ub[PBIC_DC2AC] = model["BIC"]["SMAX"]

		ub[PESS_C] = model["ESS"]["PMAX_CH"]
		ub[PESS_DC] = model["ESS"]["PMAX_DIS"]
		ub[RESS] = model["ESS"]["PMAX_DIS"] + model["ESS"]["PMAX_CH"]
		ub[EESS] = model["ESS"]["SOC_MAX"] * model["ESS"]["CAP"]

		ub[PMG] = 0  # The line flow limitation, the predefined status is, the transmission line is off-line
		# Finalize the boundary information
		LB = lb * T
		UB = ub * T
		## Constraints set
		# 1) Power balance equation
		Aeq = zeros((T, nx))
		beq = []
		for i in range(T):
			Aeq[i][i * NX + PG] = 1
			Aeq[i][i * NX + PUG] = 1
			Aeq[i][i * NX + PBIC_AC2DC] = -1
			Aeq[i][i * NX + PBIC_DC2AC] = model["BIC"]["EFF_DC2AC"]
			beq.append(model["Load_ac"]["PD"][i] + model["Load_nac"]["PD"][i])

		# 2) DC power balance equation
		Aeq_temp = zeros((T, nx))
		for i in range(T):
			Aeq_temp[i][i * NX + PBIC_AC2DC] = model["BIC"]["EFF_AC2DC"]
			Aeq_temp[i][i * NX + PBIC_DC2AC] = -1
			Aeq_temp[i][i * NX + PESS_C] = -1
			Aeq_temp[i][i * NX + PESS_DC] = 1
			Aeq_temp[i][i * NX + PMG] = -1
			beq.append(model["Load_dc"]["PD"][i] + model["Load_ndc"]["PD"][i] - model["PV"]["PG"][i] - model["WP"]["PG"][i])

		Aeq = vstack([Aeq, Aeq_temp])

		# 3) Energy storage system
		Aeq_temp = zeros((T, nx))
		for i in range(T):
			if i == 0:
				Aeq_temp[i][i * NX + EESS] = 1
				Aeq_temp[i][i * NX + PESS_C] = -model["ESS"]["EFF_CH"] * configuration_time_line.default_time[
					"Time_step_ed"] / 3600
				Aeq_temp[i][i * NX + PESS_DC] = 1 / model["ESS"]["EFF_DIS"] * configuration_time_line.default_time[
					"Time_step_ed"] / 3600
				beq.append(model["ESS"]["SOC"] * model["ESS"]["CAP"])

			else:
				Aeq_temp[i][(i - 1) * NX + EESS] = -1
				Aeq_temp[i][i * NX + EESS] = 1
				Aeq_temp[i][i * NX + PESS_C] = -model["ESS"]["EFF_CH"] * configuration_time_line.default_time[
					"Time_step_ed"] / 3600
				Aeq_temp[i][i * NX + PESS_DC] = 1 / model["ESS"]["EFF_DIS"] * configuration_time_line.default_time[
					"Time_step_ed"] / 3600
				beq.append(0)
		Aeq = vstack([Aeq, Aeq_temp])
		# Inequality constraints
		# 1) PG + RG <= PGMAX
		Aineq = zeros((T, nx))
		bineq = []
		for i in range(T):
			Aineq[i][i * NX + PG] = 1
			Aineq[i][i * NX + RG] = 1
			bineq.append(model["DG"]["PMAX"]*model["DG"]["STATUS"][i])
		# 2) PG - RG >= PGMIN
		Aineq_temp = zeros((T, nx))
		for i in range(T):
			Aineq_temp[i][i * NX + PG] = -1
			Aineq_temp[i][i * NX + RG] = 1
			bineq.append(-model["DG"]["PMIN"]*model["DG"]["STATUS"][i])
		Aineq = vstack([Aineq, Aineq_temp])
		# 3) PUG + RUG <= PUGMAX
		Aineq_temp = zeros((T, nx))
		for i in range(T):
			Aineq_temp[i][i * NX + PUG] = 1
			Aineq_temp[i][i * NX + RUG] = 1
			bineq.append(model["UG"]["PMAX"]*model["UG"]["STATUS"][i])
		Aineq = vstack([Aineq, Aineq_temp])
		# 4) PUG - RUG >= PUGMIN
		Aineq_temp = zeros((T, nx))
		for i in range(T):
			Aineq_temp[i][i * NX + PUG] = -1
			Aineq_temp[i][i * NX + RUG] = 1
			bineq.append(-model["UG"]["PMIN"]*model["UG"]["STATUS"][i])
		Aineq = vstack([Aineq, Aineq_temp])
		# 5) PESS_DC - PESS_C + RESS <= PESS_DC_MAX
		Aineq_temp = zeros((T, nx))
		for i in range(T):
			Aineq_temp[i][i * NX + PESS_DC] = 1
			Aineq_temp[i][i * NX + PESS_C] = -1
			Aineq_temp[i][i * NX + RESS] = 1
			bineq.append(model["ESS"]["PMAX_DIS"])
		Aineq = vstack([Aineq, Aineq_temp])
		# 6) PESS_DC - PESS_C - RESS >= -PESS_C_MAX
		Aineq_temp = zeros((T, nx))
		for i in range(T):
			Aineq_temp[i][i * NX + PESS_DC] = -1
			Aineq_temp[i][i * NX + PESS_C] = 1
			Aineq_temp[i][i * NX + RESS] = 1
			bineq.append(model["ESS"]["PMAX_CH"])
		Aineq = vstack([Aineq, Aineq_temp])
		# 7) EESS - RESS*delta >= EESSMIN
		Aineq_temp = zeros((T, nx))
		for i in range(T):
			Aineq_temp[i][i * NX + EESS] = -1
			Aineq_temp[i][i * NX + RESS] = configuration_time_line.default_time["Time_step_ed"] / 3600
			bineq.append(-model["ESS"]["SOC_MIN"] * model["ESS"]["CAP"])
		Aineq = vstack([Aineq, Aineq_temp])
		# 8) EESS + RESS*delta <= EESSMAX
		Aineq_temp = zeros((T, nx))
		for i in range(T):
			Aineq_temp[i][i * NX + EESS] = 1
			Aineq_temp[i][i * NX + RESS] = configuration_time_line.default_time["Time_step_ed"] / 3600
			bineq.append(model["ESS"]["SOC_MAX"] * model["ESS"]["CAP"])
		Aineq = vstack([Aineq, Aineq_temp])
		# 9) RG + RUG + RESS >= sum(Load)*beta + sum(PV)*beta_pv + sum(WP)*beta_wp
		# No reserve requirement
		c = [0] * NX
		if model["DG"]["COST_MODEL"] == 2:
			c[PG] = model["DG"]["COST"][1]
		else:
			c[PG] = model["DG"]["COST"][0]
		c[PUG] = model["UG"]["COST"][0]
		c[PESS_C] = model["ESS"]["COST_CH"][0]
		c[PESS_DC] = model["ESS"]["COST_DIS"][0]
		C = c * T
		# Generate the quadratic parameters
		Q = zeros((nx, nx))
		for i in range(T):
			if model["DG"]["COST_MODEL"] == 2:
				Q[i * NX + PG][i * NX + PG] = model["DG"]["COST"][1]

		mathematical_model = {"Q": Q,
							  "c": C,
							  "Aeq": Aeq,
							  "beq": beq,
							  "A": Aineq,
							  "b": bineq,
							  "lb": LB,
							  "ub": UB}

		return mathematical_model

	def problem_formulation_local_recovery(*args):
		from modelling.data.idx_ed_recovery_format import PG, RG, PUG, RUG, PBIC_AC2DC, PBIC_DC2AC, \
			PESS_C, PESS_DC, RESS, EESS, PMG, PPV, PWP, PL_AC, PL_UAC, PL_DC, PL_UDC, NX

		model = deepcopy(args[0])  # If multiple models are inputed, more local ems models will be formulated

		T = configuration_time_line.default_look_ahead_time_step["Look_ahead_time_ed_time_step"]
		nx = T * NX
		lb = [0] * nx
		ub = [0] * nx

		for i in range(T):
			## Update lower boundary
			lb[i * NX + PG] = model["DG"]["PMIN"]
			lb[i * NX + RG] = model["DG"]["PMIN"]
			lb[i * NX + PUG] = model["UG"]["PMIN"]
			lb[i * NX + RUG] = model["UG"]["PMIN"]
			lb[i * NX + PBIC_AC2DC] = 0
			lb[i * NX + PBIC_DC2AC] = 0
			lb[i * NX + PESS_C] = 0
			lb[i * NX + PESS_DC] = 0
			lb[i * NX + RESS] = 0
			lb[i * NX + EESS] = model["ESS"]["SOC_MIN"] * model["ESS"]["CAP"]
			lb[
				i * NX + PMG] = 0  # The line flow limitation, the predefined status is, the transmission line is off-line
			lb[i * NX + PPV] = 0
			lb[i * NX + PWP] = 0
			lb[i * NX + PL_AC] = 0
			lb[i * NX + PL_UAC] = 0
			lb[i * NX + PL_DC] = 0
			lb[i * NX + PL_UDC] = 0
			## Update lower boundary
			ub[i * NX + PG] = model["DG"]["PMAX"]
			ub[i * NX + RG] = model["DG"]["PMAX"]
			ub[i * NX + PUG] = model["UG"]["PMAX"]
			ub[i * NX + RUG] = model["UG"]["PMAX"]
			ub[i * NX + PBIC_AC2DC] = model["BIC"]["SMAX"]
			ub[i * NX + PBIC_DC2AC] = model["BIC"]["SMAX"]
			ub[i * NX + PESS_C] = model["ESS"]["PMAX_CH"]
			ub[i * NX + PESS_DC] = model["ESS"]["PMAX_DIS"]
			ub[i * NX + RESS] = model["ESS"]["PMAX_DIS"] + model["ESS"]["PMAX_CH"]
			ub[i * NX + EESS] = model["ESS"]["SOC_MAX"] * model["ESS"]["CAP"]
			ub[i * NX + PMG] = 0  # The line flow limitation, the predefined status is, the transmission line is off-line
			ub[i * NX + PPV] = model["PV"]["PG"][i]
			ub[i * NX + PWP] = model["WP"]["PG"][i]
			ub[i * NX + PL_AC] = model["Load_ac"]["PD"][i]
			ub[i * NX + PL_UAC] = model["Load_nac"]["PD"][i]
			ub[i * NX + PL_DC] = model["Load_dc"]["PD"][i]
			ub[i * NX + PL_UDC] = model["Load_ndc"]["PD"][i]

		## Constraints set
		# 1) Power balance equation
		Aeq = zeros((T, nx))
		beq = []
		for i in range(T):
			Aeq[i][i * NX + PG] = 1
			Aeq[i][i * NX + PUG] = 1
			Aeq[i][i * NX + PBIC_AC2DC] = -1
			Aeq[i][i * NX + PBIC_DC2AC] = model["BIC"]["EFF_DC2AC"]
			Aeq[i][i * NX + PL_AC] = -1
			Aeq[i][i * NX + PL_UAC] = -1
			beq.append(0)
		# 2) DC power balance equation
		Aeq_temp = zeros((T, nx))
		for i in range(T):
			Aeq_temp[i][i * NX + PBIC_AC2DC] = model["BIC"]["EFF_AC2DC"]
			Aeq_temp[i][i * NX + PBIC_DC2AC] = -1
			Aeq_temp[i][i * NX + PESS_C] = -1
			Aeq_temp[i][i * NX + PESS_DC] = 1
			Aeq_temp[i][i * NX + PMG] = -1
			Aeq_temp[i][i * NX + PL_DC] = -1
			Aeq_temp[i][i * NX + PL_UDC] = -1
			Aeq_temp[i][i * NX + PPV] = 1
			Aeq_temp[i][i * NX + PWP] = 1
			beq.append(0)
		Aeq = vstack([Aeq, Aeq_temp])

		# 3) Energy storage system
		# 3) Energy storage system
		Aeq_temp = zeros((T, nx))
		for i in range(T):
			if i == 0:
				Aeq_temp[i][i * NX + EESS] = 1
				Aeq_temp[i][i * NX + PESS_C] = -model["ESS"]["EFF_CH"] * configuration_time_line.default_time[
					"Time_step_ed"] / 3600
				Aeq_temp[i][i * NX + PESS_DC] = 1 / model["ESS"]["EFF_DIS"] * configuration_time_line.default_time[
					"Time_step_ed"] / 3600
				beq.append(model["ESS"]["SOC"] * model["ESS"]["CAP"])

			else:
				Aeq_temp[i][(i - 1) * NX + EESS] = -1
				Aeq_temp[i][i * NX + EESS] = 1
				Aeq_temp[i][i * NX + PESS_C] = -model["ESS"]["EFF_CH"] * configuration_time_line.default_time[
					"Time_step_ed"] / 3600
				Aeq_temp[i][i * NX + PESS_DC] = 1 / model["ESS"]["EFF_DIS"] * configuration_time_line.default_time[
					"Time_step_ed"] / 3600
				beq.append(0)
		Aeq = vstack([Aeq, Aeq_temp])

		# Inequality constraints
		# Inequality constraints
		# 1) PG + RG <= PGMAX
		Aineq = zeros((T, nx))
		bineq = []
		for i in range(T):
			Aineq[i][i * NX + PG] = 1
			Aineq[i][i * NX + RG] = 1
			bineq.append(model["DG"]["PMAX"]*model["DG"]["STATUS"][i])
		# 2) PG - RG >= PGMIN
		Aineq_temp = zeros((T, nx))
		for i in range(T):
			Aineq_temp[i][i * NX + PG] = -1
			Aineq_temp[i][i * NX + RG] = 1
			bineq.append(-model["DG"]["PMIN"]*model["DG"]["STATUS"][i])
		Aineq = vstack([Aineq, Aineq_temp])
		# 3) PUG + RUG <= PUGMAX
		Aineq_temp = zeros((T, nx))
		for i in range(T):
			Aineq_temp[i][i * NX + PUG] = 1
			Aineq_temp[i][i * NX + RUG] = 1
			bineq.append(model["UG"]["PMAX"]*model["UG"]["STATUS"][i])
		Aineq = vstack([Aineq, Aineq_temp])
		# 4) PUG - RUG >= PUGMIN
		Aineq_temp = zeros((T, nx))
		for i in range(T):
			Aineq_temp[i][i * NX + PUG] = -1
			Aineq_temp[i][i * NX + RUG] = 1
			bineq.append(-model["UG"]["PMIN"]*model["UG"]["STATUS"][i])
		Aineq = vstack([Aineq, Aineq_temp])
		# 5) PESS_DC - PESS_C + RESS <= PESS_DC_MAX
		Aineq_temp = zeros((T, nx))
		for i in range(T):
			Aineq_temp[i][i * NX + PESS_DC] = 1
			Aineq_temp[i][i * NX + PESS_C] = -1
			Aineq_temp[i][i * NX + RESS] = 1
			bineq.append(model["ESS"]["PMAX_DIS"])
		Aineq = vstack([Aineq, Aineq_temp])
		# 6) PESS_DC - PESS_C - RESS >= -PESS_C_MAX
		Aineq_temp = zeros((T, nx))
		for i in range(T):
			Aineq_temp[i][i * NX + PESS_DC] = -1
			Aineq_temp[i][i * NX + PESS_C] = 1
			Aineq_temp[i][i * NX + RESS] = 1
			bineq.append(model["ESS"]["PMAX_CH"])
		Aineq = vstack([Aineq, Aineq_temp])
		# 7) EESS - RESS*delta >= EESSMIN
		Aineq_temp = zeros((T, nx))
		for i in range(T):
			Aineq_temp[i][i * NX + EESS] = -1
			Aineq_temp[i][i * NX + RESS] = configuration_time_line.default_time["Time_step_ed"] / 3600
			bineq.append(-model["ESS"]["SOC_MIN"] * model["ESS"]["CAP"])
		Aineq = vstack([Aineq, Aineq_temp])
		# 8) EESS + RESS*delta <= EESSMAX
		Aineq_temp = zeros((T, nx))
		for i in range(T):
			Aineq_temp[i][i * NX + EESS] = 1
			Aineq_temp[i][i * NX + RESS] = configuration_time_line.default_time["Time_step_ed"] / 3600
			bineq.append(model["ESS"]["SOC_MAX"] * model["ESS"]["CAP"])
		Aineq = vstack([Aineq, Aineq_temp])
		# 9) RG + RUG + RESS >= sum(Load)*beta + sum(PV)*beta_pv + sum(WP)*beta_wp

		# No reserve requirement
		c = [0] * NX
		if model["DG"]["COST_MODEL"] == 2:
			c[PG] = model["DG"]["COST"][1]
		else:
			c[PG] = model["DG"]["COST"][0]
		c[PUG] = model["UG"]["COST"][0]
		c[PESS_C] = model["ESS"]["COST_CH"][0]
		c[PESS_DC] = model["ESS"]["COST_DIS"][0]
		# The sheding cost
		c[PPV] = -model["PV"]["COST"]
		c[PWP] = -model["WP"]["COST"]
		c[PL_AC] = -model["Load_ac"]["COST"][0]
		c[PL_UAC] = -model["Load_nac"]["COST"][0]
		c[PL_DC] = -model["Load_dc"]["COST"][0]
		c[PL_UDC] = -model["Load_ndc"]["COST"][0]

		C = c * T
		# Generate the quadratic parameters
		Q = zeros((nx, nx))
		for i in range(T):
			if model["DG"]["COST_MODEL"] == 2:
				Q[i * NX + PG][i * NX + PG] = model["DG"]["COST"][1]
		mathematical_model = {"Q": Q,
							  "c": C,
							  "Aeq": Aeq,
							  "beq": beq,
							  "A": Aineq,
							  "b": bineq,
							  "lb": lb,
							  "ub": ub}

		return mathematical_model

	def problem_formulation_universal(*args):
		# Formulate mathematical models for different operations
		local_model = args[0]
		universal_model = args[1]
		type = args[len(args) - 1]  # The last one is the type
		T = configuration_time_line.default_look_ahead_time_step["Look_ahead_time_ed_time_step"]

		## Formulating the universal energy models
		if type == "Feasible":
			from modelling.data.idx_ed_foramt import PMG, NX
			local_model_mathematical = ProblemFormulation.problem_formulation_local(local_model)
			universal_model_mathematical = ProblemFormulation.problem_formulation_local(universal_model)
		else:
			from modelling.data.idx_ed_recovery_format import PMG, NX
			local_model_mathematical = ProblemFormulation.problem_formulation_local_recovery(local_model)
			universal_model_mathematical = ProblemFormulation.problem_formulation_local_recovery(universal_model)
		# Modify the boundary information

		for i in range(T):
			local_model_mathematical["lb"][i * NX + PMG] = -universal_model["LINE"]["STATUS"][i] * \
														   universal_model["LINE"]["RATE_A"]
			local_model_mathematical["ub"][i * NX + PMG] = universal_model["LINE"]["STATUS"][i] * \
														   universal_model["LINE"]["RATE_A"]
			universal_model_mathematical["lb"][i * NX + PMG] = -universal_model["LINE"]["STATUS"][i] * \
															   universal_model["LINE"]["RATE_A"]
			universal_model_mathematical["ub"][i * NX + PMG] = universal_model["LINE"]["STATUS"][i] * \
															   universal_model["LINE"]["RATE_A"]
		## Modify the matrix
		nx = T * NX
		neq = local_model_mathematical["Aeq"].shape[0]  # Number of equality constraint
		nineq = local_model_mathematical["A"].shape[0]  # Number of inequality constraint
		Aeq_compact = zeros((2 * neq, 2 * nx))
		beq_compact = zeros(2 * neq)
		Aineq_compact = zeros((2 * nineq, 2 * nx))
		bineq_compact = zeros(2 * nineq)
		c_compact = zeros(2 * nx)
		# The combination of local ems and universal ems problems
		Aeq_compact[0:neq, 0:nx] = local_model_mathematical["Aeq"]
		Aeq_compact[neq:2 * neq, nx:2 * nx] = universal_model_mathematical["Aeq"]
		beq_compact[0:neq] = local_model_mathematical["beq"]
		beq_compact[neq:2 * neq] = universal_model_mathematical["beq"]

		Aineq_compact[0:nineq, 0:nx] = local_model_mathematical["A"]
		Aineq_compact[nineq:2 * nineq, nx:2 * nx] = universal_model_mathematical["A"]
		bineq_compact[0:nineq] = local_model_mathematical["b"]
		bineq_compact[nineq:2 * nineq] = universal_model_mathematical["b"]

		c_compact[0:nx] = local_model_mathematical["c"]
		c_compact[nx:2 * nx] = universal_model_mathematical["c"]
		c_compact = array(c_compact)

		lb = numpy.append(local_model_mathematical["lb"], universal_model_mathematical["lb"])
		ub = numpy.append(local_model_mathematical["ub"], universal_model_mathematical["ub"])

		Aeq_compact_temp = zeros((T, 2 * nx))
		for i in range(T):
			Aeq_compact_temp[i][i * NX + PMG] = 1
			Aeq_compact_temp[i][nx + i * NX + PMG] = 1
			beq_compact = numpy.append(beq_compact, zeros(1))
		Aeq_compact = vstack([Aeq_compact, Aeq_compact_temp])

		Q_compact = zeros((2 * nx, 2 * nx))
		Q_compact[0:nx, 0:nx] = local_model_mathematical["Q"]
		Q_compact[nx:2 * nx, nx:2 * nx] = universal_model_mathematical["Q"]

		model = {"Q": Q_compact,
				 "c": c_compact,
				 "Aeq": Aeq_compact,
				 "beq": beq_compact,
				 "A": Aineq_compact,
				 "b": bineq_compact,
				 "lb": lb,
				 "ub": ub}
		return model
