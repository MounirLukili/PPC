from solver import Solver
from csp import  CSP
from constraint import *
from typing import Dict, List, Optional

if __name__ == "__main__":
    variables: List[str] = ["x", "y","z"]
    domains: Dict[str, List[int]] = {}
    for var in variables:
        domains[var] = [1, 2, 3]
    csp = CSP(variables, domains)
    csp.add_constraint(Different("x", "y"))
    csp.add_constraint(Superior("x", "z"))

    solver = Solver()
    #
    print("\n\n===========================================")
    print("===========================================\n\n")
    solver.backtracking_search(csp)
    print("BT SEARCH Number of nodes: ",solver.nbNodes)
    print("\n\n===========================================")
    print("===========================================\n\n")
    solver.nbNodes = 0
    solver.bt_forward(csp,None)
    print("BT FORWARD Number of nodes: ",solver.nbNodes)
    print("\n\n===========================================")
    print("===========================================\n\n")
    solver.nbNodes = 0
    solver.bt_propagation(csp,"AC1")
    print("BT PROPAGATION AC1 Number of nodes: ",solver.nbNodes)
    print("\n\n===========================================")
    print("===========================================\n\n")
    solver.nbNodes = 0
    solver.bt_propagation(csp,"AC3")
    print("BT PROPAGATION AC3 Number of nodes: ",solver.nbNodes)
    print("\n\n===========================================")
    print("===========================================\n\n")
    solver.nbNodes = 0
    solver.solve_all(csp, "bt_forward", None)
    print("Number of nodes: ",solver.nbNodes)
    print("\n\n===========================================")
    print("===========================================\n\n")
    #
        
