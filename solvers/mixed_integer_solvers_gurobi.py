"""Branch and bound method for mix_integer linear programming (MILP) using Gurobi
		Minimize a linear objective function, subject to optional linear constraints and variable bounds::

				min f(x) := inner(c,x)
				 x

		subject to::

				A*x == beq          (linear constraints, equality)
				A*x <= b            (linear constraints, inequality)
				xmin <= x <= xmax   (variable bounds)
				x {binary, discrete, continuous }

		All parameters are optional except C and vtype.
		@param c: Linear function that evaluates the objective function
		@type f_fcn: array
		@param Aeq: Optional equality linear constraints.
		@type Aeq: csr_matrix
		@param beq: Optional equality linear constraints.
		@type beq: array
		@param A: Optional linear constraints.
		@type A: csr_matrix
		@param b: Optional linear constraints. Default values are M{Inf}.
		@type b: array
		@param xmin: Optional lower bounds on the M{x} variables, defaults are
					 M{-Inf}.
		@type xmin: array
		@param xmax: Optional upper bounds on the M{x} variables, defaults are
					 M{Inf}.
		@type xmax: array
		@param vtype: list to depict the variable types, i.e.binary, discrete, continuous.
		@type vtypr: list
		@param opt: optional options dictionary with the following keys, all of
					which are also optional (default values shown in parentheses)
		@type opt: dict

		@rtype: array
		@return: The solution dictionary has the following keys:
				   - x - solution vector
				   - f - final objective function value
				   - success - exit status
					   - 0 = first order optimality conditions satisfied
					   - 1 = no solution found
"""
from numpy import Inf, ones
from gurobipy import *

def mixed_integer_linear_programming(c, Aeq=None, beq=None, A=None, b=None, xmin=None, xmax=None, vtypes=None, opt=None):
	if type(c) == list:
		nx=len(c)
	else:
		nx = c.shape[0]  # number of decision variables

	if A is not None:
		if A.shape[0]!= None:
			nineq = A.shape[0]  # number of equality constraints
		else:
			nineq = 0
	else:
		nineq = 0

	if Aeq is not None:
		if Aeq.shape[0]!= None:
			neq = Aeq.shape[0]  # number of inequality constraints
		else:
			neq = 0
	else:
		neq = 0
	# Fulfilling the missing informations
	if beq is None or len(beq) == 0: beq = -Inf * ones(neq)
	if b is None or len(b) == 0: b = Inf * ones(nineq)
	if xmin is None or len(xmin) == 0: xmin = -Inf * ones(nx)
	if xmax is None or len(xmax) == 0: xmax = Inf * ones(nx)

	# modelling based on the high level gurobi api
	try:
		gurobi_model = Model("MIP")
		# Declear the variables
		x = {}
		for i in range(nx):
			if vtypes[i] == "b" or vtypes[i] == "B":
				x[i] = gurobi_model.addVar(lb=xmin[i], ub=xmax[i], vtype=GRB.BINARY, name='"x{0}"'.format(i))
			elif vtypes[i] == "d" or vtypes[i] == "D":
				x[i] = gurobi_model.addVar(lb=xmin[i], ub=xmax[i], vtype=GRB.INTEGER, name='"x{0}"'.format(i))
			else:
				x[i] = gurobi_model.addVar(lb=xmin[i], ub=xmax[i], vtype=GRB.CONTINUOUS, name='"x{0}"'.format(i))
		# Constraints set
		# Equal constraints
		if neq != 0:
			for i in range(neq):
				expr = 0
				for j in range(nx):
					expr += x[j] * Aeq[i, j]
				gurobi_model.addConstr(lhs=expr, sense=GRB.EQUAL, rhs=beq[i])

		# Inequal constraints
		if nineq != 0:
			for i in range(nineq):
				expr = 0
				for j in range(nx):
					expr += x[j] * A[i, j]
				gurobi_model.addConstr(lhs=expr, sense=GRB.LESS_EQUAL, rhs=b[i])
		# Set the objective function
		obj = 0
		for i in range(nx):
			obj += x[i] * c[i]

		gurobi_model.setObjective(obj)

		gurobi_model.Params.OutputFlag = 0
		gurobi_model.Params.LogToConsole = 0
		gurobi_model.Params.DisplayInterval = 1
		gurobi_model.Params.LogFile = ""

		gurobi_model.optimize()
		xx = []
		for v in gurobi_model.getVars():
			xx.append(v.x)

		obj = obj.getValue()
		success = 1

	except GurobiError as e:
		print('Error code ' + str(e.errno) + ": " + str(e))
		xx = 0
		obj = 0
		success = 0

	except AttributeError:
		print('Encountered an attribute error')
		xx = 0
		obj = 0
		success = 0


	return xx, obj, success

if __name__ == "__main__":
	# A test problem from Gurobi
	#  maximize
	#        x +   y + 2 z
	#  subject to
	#        x + 2 y + 3 z <= 4
	#        x +   y       >= 1
	#  x, y, z binary

	from numpy import array
	from scipy.sparse import csr_matrix

	c = array([1, 1, 2])
	A = csr_matrix(array([[1, 2, 3],
						  [-1, -1, 0]]))  # A sparse matrix
	b = array([4, -1])
	vtypes = []
	vtypes.append('b')
	vtypes.append('b')
	vtypes.append('b')

	solution = mixed_integer_linear_programming(c, A=A, b=b, vtypes=vtypes)
	print(solution)