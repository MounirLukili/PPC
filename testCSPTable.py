from solver import Solver
from csp import CSP
from constraint import *
from typing import Dict, List, Optional

if __name__ == "__main__":
    variables: List[str] = ["x", "y","z"]
    domains: Dict[str, List[int]] = {}
    for var in variables:
        domains[var] = [1, 2, 3]
    csp = CSP(variables, domains)
    #csp.add_constraint(Table(['x','y'],[[1,2],[2,2],[3,3]]))
    #csp.add_constraint(Table(['y','z'],[[1,2],[2,1],[2,3],[3,1]]))
    #csp.add_constraint(Table(['z','x'],[[1,1],[2,3],[3,2]]))
    csp.add_constraint(Table(['x','y'],[[1,1],[1,3],[2,2],[3,1],[3,3]]))
    csp.add_constraint(Table(['x','z'],[[1,2],[1,3],[2,3]]))
    csp.add_constraint(Table(['y','z'],[[1,2],[3,1],[3,3]]))
    
    solver = Solver()
    #
    print("\n\n===========================================")
    print("===========================================\n\n")
    solver.backtracking_search(csp)
    print("BT Search Number of nodes: ",solver.nbNodes)
    print("\n\n===========================================")
    print("===========================================\n\n")
    solver.nbNodes = 0
    solver.bt_forward(csp,None)
    print("BT forward Number of nodes: ",solver.nbNodes)
    print("\n\n===========================================")
    print("===========================================\n\n")
    solver.nbNodes = 0
    solver.bt_propagation(csp,"AC1")
    print("AC1 Number of nodes: ",solver.nbNodes)
    print("\n\n===========================================")
    print("===========================================\n\n")
    solver.nbNodes = 0
    solver.bt_propagation(csp,"AC3")
    print("AC3 Number of nodes: ",solver.nbNodes)
    print("\n\n===========================================")
    print("===========================================\n\n")
    solver.nbNodes = 0
    solver.solve_all(csp, "bt_forward", None)
    print("Number of nodes: ",solver.nbNodes)
    print("\n\n===========================================")
    print("===========================================\n\n")
        

                
