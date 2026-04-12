from solver import Solver
from csp import CSP
from constraint import Different
import time

# --- GRILLES DE TEST ---
# 0 = case vide
SUDOKU_EASY = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0], [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3], [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

SUDOKU_HARD = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 6, 0, 0, 0, 0, 0], [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 4, 5, 7, 0, 0], [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8], [0, 0, 8, 5, 0, 0, 0, 1, 0], [0, 9, 0, 0, 0, 0, 4, 0, 0]
]

def build_sudoku_csp(grid):
    """Crée le CSP : variables, domaines et contraintes d'inégalité."""
    variables = [f"R{i}C{j}" for i in range(1, 10) for j in range(1, 10)]
    domains = {}
    
    for i in range(1, 10):
        for j in range(1, 10):
            val = grid[i-1][j-1]
            domains[f"R{i}C{j}"] = [val] if val != 0 else list(range(1, 10))

    csp = CSP(variables, domains)

    # Helper pour ajouter AllDifferent sur une liste de variables
    def add_alldiff(vars_list):
        for k, var_a in enumerate(vars_list):
            for var_b in vars_list[k+1:]:
                csp.add_constraint(Different(var_a, var_b))

    # Lignes, Colonnes et Blocs 3x3
    for i in range(1, 10):
        add_alldiff([f"R{i}C{j}" for j in range(1, 10)]) # Lignes
        add_alldiff([f"R{j}C{i}" for j in range(1, 10)]) # Colonnes

    for bi in range(3):
        for bj in range(3):
            block = [f"R{bi*3+r+1}C{bj*3+c+1}" for r in range(3) for c in range(3)]
            add_alldiff(block)

    return csp

def display_grid(grid):
    """Affichage simple de la grille."""
    for i, row in enumerate(grid):
        if i % 3 == 0 and i != 0: print("-" * 21)
        r_str = ""
        for j, val in enumerate(row):
            if j % 3 == 0 and j != 0: r_str += "| "
            r_str += f"{val if val != 0 else '.'} "
        print(r_str)

def run_benchmark(grid, name):
    """Lance et compare les algos sur une grille donnée."""
    print(f"\n=== TEST GRILLE : {name} ===")
    display_grid(grid)
    
    algos = [
        ("Backtracking (BT)", "backtracking", "AC1"),
        ("BT + Forward Checking", "bt_forward", "AC1"),
        ("BT + AC1", "bt_propagation", "AC1"),
        ("BT + AC3", "bt_propagation", "AC3")
    ]

    print(f"\n{'Algorithme':<25} | {'Nœuds':<8} | {'Temps':<10}")
    print("-" * 50)

    for label, algo_type, ac_ver in algos:
        csp = build_sudoku_csp(grid)
        solver = Solver()
        
        start = time.time()
        solver.solve_all(csp, algo=algo_type, choixAC=ac_ver, k=1)
        elapsed = (time.time() - start) * 1000

        print(f"{label:<25} | {solver.nbNodes:<8} | {elapsed:>7.2f} ms")

if __name__ == "__main__":
    run_benchmark(SUDOKU_EASY, "FACILE")
    run_benchmark(SUDOKU_HARD, "DIFFICILE")