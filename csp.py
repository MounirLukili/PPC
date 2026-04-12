# definition d'un CSP

from typing import Generic, TypeVar, Dict, List, Optional
from constraint import Constraint, Var, Value

        
# 
class CSP:
    '''
    Un CSP est définit par une liste de variables 
    chacune avec son domaine et un ensemble de contraintes
    '''
    #
    def __init__(self, variables: List[Var], domains: Dict[Var, List[Value]]):
        '''
        Crée un CSP avec les variables et les domaines donnés

        Parameters
        ----------
        variables : List[Var]
        domains : Dict[Var, List[Value]]
        '''
        # les variables du CSP
        self.variables: List[Var] = variables
        #
        # les domaines
        self.domains: Dict[Var, List[Value]] = domains
        #
        # la liste qui contiendra les contraintes qui sont à ajouter
        self.ctrList: List[Constraint[Var, Value]] = []
        #
        self.vcList: Dict[Var, List[Constraint[Var, Value]]] = {}
        for var in self.variables:
            self.vcList[var] = []
            if var not in self.domains:
                raise LookupError("Chaque variable doit avoir son domaine")

    
    def add_constraint(self, constraint):
        self.ctrList.append(constraint)
        for var in constraint.variables:
            if var not in self.variables:
                raise LookupError("Variable n'est pas du CSP")
            else:
                self.vcList[var].append(constraint)
                
    # 
    def check_unsat(self) -> bool:
        '''Vérifier si une affectation partielle (les domaines singletons) ne satisfait pas une contrainte'''
        for constr in self.ctrList:
            allSingleton=True
            for var in constr.variables:
                if len(self.domains[var]) > 1:
                    allSingleton=False
            if allSingleton and constr.unsat(self.domains):
                return True
        return False
                
    # 
    def singleton(self) -> bool:
        '''Vérifier si tous les domaines sont singletons'''
        for var in self.variables:
            if len(self.domains[var]) > 1:
                return False
        return True

    # 
    def instSatisfied(self) -> bool: 
        '''Quand toutes les variables sont instanciées, vérifier si le CSP est satisfait'''
        for constr in self.ctrList:
            if constr.unsat(self.domains):
                return False
        return True
 
    # 
    def solution(self) -> Dict[Var, Value]:
        '''Créer une solution sous forme de dictionnaire'''
        sol:Dict[Var, Value] = {}
        for var in self.variables:
            sol[var]= self.domains[var][0]
        return sol

    # 
    def unassignedVar(self) -> Var:
        '''Retourner une variable dont le domaine n'est pas singleton'''
        for var in self.variables:
            if len(self.domains[var]) > 1:
                return var
        return None

    # 
    def domainsCopy(self) :
        '''Créer une copie des domaines'''
        d_copy = self.domains.copy()
        for var in self.variables:
            d_copy[var] = self.domains[var].copy()
        return d_copy

    # 
    def emptyDomain(self):
        '''Vérifier si un des domaines est vide'''
        for var in self.variables:
            if self.domains[var]==[]:
                return True
        return False
