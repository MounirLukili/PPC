from solver import Solver
from csp import  CSP
from constraint import *
from typing import Dict, List, Optional

if __name__ == "__main__":
    variables: List[str] = ["A", "B","C", "D", "E", "F"]
    domains: Dict[str, List[int]] = {}
    for var in variables:
        domains[var] = [1, 2, 3, 4, 5]
    csp = CSP(variables, domains)
    csp.add_constraint(Superior("B", "A"))
    csp.add_constraint(Superior("D", "A"))
    csp.add_constraint(Superior("E", "A"))
    csp.add_constraint(Superior("C", "B"))
    csp.add_constraint(Superior("D", "B"))
    csp.add_constraint(Superior("E", "B"))
    csp.add_constraint(Superior("D", "C"))
    csp.add_constraint(Superior("C", "F"))
    csp.add_constraint(Superior("E", "D"))
    csp.add_constraint(Superior("E", "F"))
    
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
    #
        
