# fonctionnement d'un solveur CSP
import time
from typing import Dict, List, Optional
from constraint import Var, Value
from csp import CSP

class Solver:
    def __init__(self):
        self.reset_stats()

    def reset_stats(self):
        self.nbNodes = 0
        self.nbSolutions = 0
        self.solutions: Dict[int, Dict[Var, Value]] = {}
        self.nbFailures = 0
        self.runtime = 0.0

    def check_if_solution(self, csp: CSP) -> bool:
        if csp.singleton() and csp.instSatisfied():
            self.solutions[self.nbSolutions] = csp.solution()
            self.nbSolutions += 1
            return True
        return False
    
    def check_if_failure(self, csp: CSP) -> bool:
        if csp.emptyDomain():
            self.nbFailures += 1
            return True
        return False

    def select_unassigned_variable(self, csp: CSP, search: str = "seq") -> Var:
        if search == "minDom":
            vars_to_check = [v for v in csp.variables if len(csp.domains[v]) > 1]
            if not vars_to_check: return None
            return min(vars_to_check, key=lambda v: len(csp.domains[v]))
        return csp.unassignedVar()

    def backtracking_search(self, csp: CSP, k: Optional[int] = None, search: str = "seq"):
        if k is not None and self.nbSolutions >= k: return
        self.nbNodes += 1
        
        if self.check_if_failure(csp): return
        if self.check_if_solution(csp): return
        if csp.check_unsat(): return

        var = self.select_unassigned_variable(csp, search)
        if var is None: return
        
        for val in list(csp.domains[var]):
            old_domains = csp.domainsCopy()
            csp.domains[var] = [val]
            self.backtracking_search(csp, k, search)
            csp.domains = old_domains

    def forward_checking(self, csp: CSP, X: Var) -> bool:
        for ctr in csp.vcList[X]:
            for Y in ctr.variables:
                if Y != X:
                    if ctr.revise(Y, csp.domains):
                        if len(csp.domains[Y]) == 0: return False
        return True

    def bt_forward(self, csp: CSP, k: Optional[int] = None, search: str = "seq"):
        if k is not None and self.nbSolutions >= k: return
        self.nbNodes += 1
        
        if self.check_if_failure(csp): return
        if self.check_if_solution(csp): return

        var = self.select_unassigned_variable(csp, search)
        if var is None: return
        
        for val in list(csp.domains[var]):
            old_domains = csp.domainsCopy()
            csp.domains[var] = [val]
            if self.forward_checking(csp, var):
                self.bt_forward(csp, k, search)
            csp.domains = old_domains

    def bt_propagation(self, csp: CSP, choixAC: str, k: Optional[int] = None, search: str = "seq"):
        if k is not None and self.nbSolutions >= k: return
        self.nbNodes += 1
        
        if self.check_if_failure(csp): return
        if self.check_if_solution(csp): return

        var = self.select_unassigned_variable(csp, search)
        if var is None: return

        for val in list(csp.domains[var]):
            old_domains = csp.domainsCopy()
            csp.domains[var] = [val]
            
            ok = self.propagate_AC1(csp) if choixAC == "AC1" else self.propagate_AC3(csp)
            if ok:
                self.bt_propagation(csp, choixAC, k, search)
            csp.domains = old_domains

    def propagate_AC1(self, csp: CSP) -> bool:
        modification = True
        while modification:
            modification = False
            for ctr in csp.ctrList:
                for v in ctr.variables:
                    if ctr.revise(v, csp.domains):
                        if len(csp.domains[v]) == 0: return False
                        modification = True
        return True
    
    def propagate_AC3(self, csp: CSP) -> bool:
        queue = [(v, ctr) for ctr in csp.ctrList for v in ctr.variables]
        while queue:
            var, ctr = queue.pop(0)
            if ctr.revise(var, csp.domains):
                if len(csp.domains[var]) == 0: return False
                for related_ctr in csp.vcList[var]:
                    for other_var in related_ctr.variables:
                        if other_var != var:
                            queue.append((other_var, related_ctr))
        return True

    def solve_all(self, csp: CSP, algo: str = "backtracking", choixAC: str = "AC1", search: str = "seq", k: Optional[int] = None):
        self.reset_stats()
        start_time = time.time()
        
        if algo == "backtracking":
            self.backtracking_search(csp, k, search)
        elif algo == "bt_forward":
            self.bt_forward(csp, k, search)
        elif algo == "bt_propagation":
            self.bt_propagation(csp, choixAC, k, search)
            
        self.runtime = time.time() - start_time
        self.print_stats(algo, choixAC)

    def print_stats(self, algo: str, choixAC: Optional[str]):
        print(f"\n--- Statistiques ({algo} {choixAC if choixAC else ''}) ---")
        print(f"Solutions trouvées : {self.nbSolutions}")
        print(f"Nœuds explorés     : {self.nbNodes}")
        print(f"Échecs rencontrés   : {self.nbFailures}")
        print(f"Temps d'exécution  : {self.runtime:.4f} sec")