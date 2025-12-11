import gurobipy as gp
from gurobipy import GRB

def solve_atsp_mtz(n, C, time_limit=3600):
    """
    Modelo MTZ para ATSP usando Gurobi.
    C : Matriz de costos NxN (numpy array)
    """
    modelo = gp.Model("ATSP_MTZ")
    modelo.setParam('TimeLimit', time_limit)

    #Variables x[i,j] binarias que indican si se viaja de i a j
    x = modelo.addVars(n, n, vtype=GRB.BINARY, name="x")

    #Variables de orden u[i] para las restricciones MTZ
    u = modelo.addVars(n, vtype=GRB.CONTINUOUS, lb=0, ub= n -1 , name="u")

    #Función objetivo: minimizar el costo total
    modelo.setObjective(gp.quicksum(C[i][j] * x[i,j] for i in range(n) for j in range(n) if i != j), GRB.MINIMIZE)

    #Restricciones: no se puede viajar de un nodo a sí mismo
    for i in range(n):
        modelo.addConstr(x[i,i] == 0, name=f"no_self_loop_{i}")
    
    #Restricciones: cada nodo debe ser entrado y salido exactamente una vez
    for i in range(n):
        modelo.addConstr(gp.quicksum(x[i,j] for j in range(n) if j != i) == 1, name=f"out_{i}")
        modelo.addConstr(gp.quicksum(x[j,i] for j in range(n) if j != i) == 1, name=f"in_{i}")

    #Restriccion para el primer nodo
    modelo.addConstr(u[0] == 0, name="u_0_fixed")

    #Restricciones MTZ para eliminar subciclos
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                modelo.addConstr(u[i] - u[j] + (n - 1) * x[i,j] <= n - 2, name=f"mtz_{i}_{j}")


    modelo.optimize()

    return{
        "objective_value": modelo.ObjVal if modelo.status == GRB.OPTIMAL or modelo.status == GRB.TIME_LIMIT else None,
        "gap": modelo.MIPGap if modelo.status == GRB.TIME_LIMIT else 0,
        "tiempo": modelo.Runtime,
        "vars": modelo.NumVars,
        "constraints": modelo.NumConstrs,
    }

def solve_atsp_gg(n, C, time_limit=3600):
    """
    Modelo GG para ATSP usando Gurobi.
    C : Matriz de costos NxN (numpy array)
    """
    modelo = gp.Model("ATSP_GG")
    modelo.setParam('TimeLimit', time_limit)

    #Variables x[i,j] binarias que indican si se viaja de i a j
    x = modelo.addVars(n, n, vtype=GRB.BINARY, name="x")

    #Varibles de flujo f[i,j]
    f = modelo.addVars(n, n, vtype=GRB.CONTINUOUS, lb=0, ub=n - 1, name="f")

    #Función objetivo: minimizar el costo total
    modelo.setObjective(gp.quicksum(C[i][j] * x[i,j] for i in range(n) for j in range(n) if i != j), GRB.MINIMIZE)

    #Restricciones: no se puede viajar de un nodo a sí mismo
    for i in range(n):
        modelo.addConstr(x[i,i] == 0, name=f"no_self_loop_{i}")

    #Restricción de flujo hacia el nodo 0
    for j in range(1, n):
        modelo.addConstr(f[j,0] == 0, name=f"flow_to_0_{j}")


    #Restricciones: cada nodo debe ser entrado y salido exactamente una vez
    for i in range(n):
        modelo.addConstr(gp.quicksum(x[i,j] for j in range(n) if j != i) == 1, name=f"out_{i}")
        modelo.addConstr(gp.quicksum(x[j,i] for j in range(n) if j != i) == 1, name=f"in_{i}")
    
    #Restricciones de flujo para eliminar subciclos
    for i in range(1, n):
        modelo.addConstr(gp.quicksum(f[j,i] for j in range(n) if j != i) - gp.quicksum(f[i,j] for j in range(n) if j != i) == 1, name=f"flow_{i}")
    
    #Restricción de flujo para el nodo inicial
    modelo.addConstr(gp.quicksum(f[0,j] for j in range(1, n)) == n - 1, name="flow_0")

    #Restricciones que vinculan flujo y variables de decisión
    for i in range(n):
        for j in range(n):
            if i != j:
                modelo.addConstr(f[i,j] <= (n - 1) * x[i,j], name=f"flow_link_{i}_{j}")

    modelo.optimize()

    return{
        "objective_value": modelo.ObjVal if modelo.status == GRB.OPTIMAL or modelo.status == GRB.TIME_LIMIT else None,
        "gap": modelo.MIPGap if modelo.status == GRB.TIME_LIMIT else 0  ,
        "tiempo": modelo.Runtime,
        "vars": modelo.NumVars,
        "constraints": modelo.NumConstrs,
    }