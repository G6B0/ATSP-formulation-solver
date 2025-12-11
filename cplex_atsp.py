import numpy as np
from docplex.mp.model import Model

# MTZ CPLEX

def solve_atsp_mtz_cplex(n, C, time_limit=3600):

    # Model de docplex en lugar de modelo = gp.Model("ATSP_MTZ")
    mdl = Model(name="ATSP_MTZ")

    # mdl.parameters.timelimit en lugar de modelo.setParam('TimeLimit', time_limit)
    mdl.parameters.timelimit = time_limit

    # se crean variables con binary_var en un diccionario en lugar de x = modelo.addVars(n, n, vtype=GRB.BINARY, name="x")
    x = {(i,j): mdl.binary_var(name=f"x_{i}_{j}") for i in range(n) for j in range(n)}

    # se crean con continuous_var en un diccionario en lugar de u = modelo.addVars(n, vtype=GRB.CONTINUOUS, lb=0, ub=n-1, name="u")
    u = {i: mdl.continuous_var(lb=0, ub=n-1, name=f"u_{i}") for i in range(n)}

    # mdl.minimize(...) en lugar de modelo.setObjective(..., GRB.MINIMIZE)
    mdl.minimize(mdl.sum(C[i][j]*x[i,j] for i in range(n) for j in range(n) if i!=j))

    # mdl.add_constraint(...) en lugar de modelo.addConstr(...)
    for i in range(n):
        mdl.add_constraint(x[i,i] == 0)
        mdl.add_constraint(mdl.sum(x[i,j] for j in range(n) if j!=i) == 1)
        mdl.add_constraint(mdl.sum(x[j,i] for j in range(n) if j!=i) == 1)

    mdl.add_constraint(u[0] == 0)

    for i in range(1,n):
        for j in range(1,n):
            if i!=j:
                mdl.add_constraint(u[i] - u[j] + (n-1)*x[i,j] <= n-2)

    # se usa mdl.solve() en lugar de modelo.optimize()
    sol = mdl.solve(log_output=True)

    # sol.objective_value, mdl.solve_details.mip_relative_gap, mdl.solve_details.time, mdl.number_of_variables, mdl.number_of_constraints
    # en Gurobi era modelo.ObjVal, modelo.MIPGap, modelo.Runtime, modelo.NumVars, modelo.NumConstrs
   
    return {
        "objective_value": sol.objective_value if sol else None,
        "gap": mdl.solve_details.mip_relative_gap if sol else None,
        "tiempo": mdl.solve_details.time,
        "vars": mdl.number_of_variables,
        "constraints": mdl.number_of_constraints,
    }

# GG CPLEX

def solve_atsp_gg_cplex(n, C, time_limit=3600):
    mdl = Model(name="ATSP_GG")
    mdl.parameters.timelimit = time_limit

    # binary_var en diccionario en lugar de x = modelo.addVars(n, n, vtype=GRB.BINARY, name="x")
    x = {(i,j): mdl.binary_var(name=f"x_{i}_{j}") for i in range(n) for j in range(n)}

    # continuous_var en diccionario en lugar de f = modelo.addVars(n, n, vtype=GRB.CONTINUOUS, lb=0, ub=n-1, name="f")
    f = {(i,j): mdl.continuous_var(lb=0, ub=n-1, name=f"f_{i}_{j}") for i in range(n) for j in range(n)}

    # setObjective → minimize
    mdl.minimize(mdl.sum(C[i][j]*x[i,j] for i in range(n) for j in range(n) if i!=j))

    # Restricciones: addConstr → add_constraint
    for i in range(n):
        mdl.add_constraint(x[i,i] == 0)
        mdl.add_constraint(mdl.sum(x[i,j] for j in range(n) if j!=i) == 1)
        mdl.add_constraint(mdl.sum(x[j,i] for j in range(n) if j!=i) == 1)

    for j in range(1,n):
        mdl.add_constraint(f[j,0] == 0)

    for i in range(1,n):
        mdl.add_constraint(mdl.sum(f[j,i] for j in range(n) if j!=i) - mdl.sum(f[i,j] for j in range(n) if j!=i) == 1)

    mdl.add_constraint(mdl.sum(f[0,j] for j in range(1,n)) == n-1)

    for i in range(n):
        for j in range(n):
            if i!=j:
                mdl.add_constraint(f[i,j] <= (n-1)*x[i,j])

    sol = mdl.solve(log_output=True)

    return {
        "objective_value": sol.objective_value if sol else None,
        "gap": mdl.solve_details.mip_relative_gap if sol else None,
        "tiempo": mdl.solve_details.time,
        "vars": mdl.number_of_variables,
        "constraints": mdl.number_of_constraints,
    }

