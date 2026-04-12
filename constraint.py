from abc import ABC, abstractmethod
from typing import Dict, List, Optional, TypeVar

#Var = 'str'
Var = TypeVar('str') # type pour variable
#Value = 'int'
Value = TypeVar('int') # type pour domaine

# 
class Constraint(ABC):
    '''Classe pour les contraintes'''
    # constructeur initie les variables
    def __init__(self, variables: List[Var]) -> None:
        '''
        Crée une contrainte avec les variables

        Parameters
        ----------
        variables : List[Var]
        '''
        #
        self.variables = variables
        '''liste des variables de la contrainte'''
        #

    # fonctions à redéfinir pour chaque contrainte
    @abstractmethod
    def unsat(self, domains: Dict[Var, List[Value]]) -> bool:
        '''
        Tester si les domaines sont en conflit dans la contrainte
        Retourner True s'il y a un conflit (la contrainte est donc unsatisfaisable) et False sinon
        '''
        ...

    # fonctions à redéfinir pour chaque contrainte
    @abstractmethod
    def checkSupport(self, var: Var, value: Value, domains: Dict[Var, List[Value]]) -> bool:
        '''
        Tester si la valeur `value` de la variable `var` a un support et
        retourner True si oui et False sinon
        '''
        ...
        
    # 
    def revise(self, revisedVar, domains: Dict[Var, List[Value]]) -> bool:
        '''
        Enlever les valeurs sans support de la variable `revisedVar` et
        retourner True si ces valeurs existent
        '''
        listRem = []
        for val in domains[revisedVar]:
            if self.checkSupport(revisedVar, val, domains) == False:
                listRem.append(val)
        for val in listRem:
            domains[revisedVar].remove(val)
        if len(listRem)==0:
            return False
        return True

# 
class Different(Constraint):
    '''Contrainte v1 != v2'''
    def __init__(self, v1, v2) -> None:
        super().__init__([v1, v2])
        self.v1 = v1
        self.v2 = v2

    def unsat(self, domains: Dict[str, List[int]]) -> bool: # TODO
        return domains[self.v1][0] == domains[self.v2][0]
    
    def checkSupport(self, var, value, domains) -> bool: # TODO
        other_var = self.v2 if var == self.v1 else self.v1
        for val_other in domains[other_var]:
            if value != val_other:
                return True
        return False

# 
class Superior(Constraint):
    '''Contrainte v1 > v2'''
    def __init__(self, v1: str, v2:str):
        super().__init__([v1, v2])
        self.v1 = v1
        self.v2 = v2
    
    def unsat(self, domains: Dict[str, List[int]]) -> bool: # TODO
       return not (domains[self.v1][0] > domains[self.v2][0])
    
    def checkSupport(self, var, value, domains) -> bool: # TODO
        if var == self.v1:
            # Existe-t-il une  val2 tq value > val2 ?
            # Il suffit que value soit > au min du domaine de v2
            return value > min(domains[self.v2])
        else: 
            # var == self.v2
            # une valeur val1 telle que val1 > value ?
            # Il suffit que le max du domaine de v1 soit > value
            return max(domains[self.v1]) > value

# 
class SumSup(Constraint):
    '''Contrainte v1 + v2 > a'''
    def __init__(self, v1: str, v2:str, a:int):
        super().__init__([v1, v2])
        self.v1 = v1
        self.v2 = v2
        self.a = a
    
    def unsat(self, domains: Dict[str, List[int]]) -> bool:
        return not (domains[self.v1][0] + domains[self.v2][0] > self.a)
    
    def checkSupport(self, var, value, domains) -> bool:
        other_var = self.v2 if var == self.v1 else self.v1
        # une valeur telle que value + val_other > a ?
        # Il suffit que value + le max de l'autre domaine  > a
        return value + max(domains[other_var]) > self.a
    
# 
class Table(Constraint):
    '''Contrainte définie en extension (la table liste les tuples satisfaisant la contrainte)'''
    def __init__(self, varList, tupleTable):
        super().__init__(varList)
        self.table = tupleTable
        
    def unsat(self, domains: Dict[str, List[int]]) -> bool:
        # On construit le tuple des valeurs actuels
        current_tuple = [domains[v][0] for v in self.variables]
        # Si le tuple n'est pas dans la table la contrainte est insatisfaite
        return current_tuple not in self.table
    
    def checkSupport(self, var, value, domains) -> bool:
        # Indice de la variable dans la contrainte
        idx = self.variables.index(var)
        # on parcourt chaque tuple autorisé dans la table
        for t in self.table:
            # Le tuple support si :
            #  La valeur pour 'var' = 'value'
            #  Pour toutes les autres variables, la valeur du tuple est dans leur domaine
            if t[idx] == value:
                is_supported = True
                for i, v in enumerate(self.variables):
                    if i != idx and t[i] not in domains[v]:
                        is_supported = False
                        break
                if is_supported:
                    return True
        return False
