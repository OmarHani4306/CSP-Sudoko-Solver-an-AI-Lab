from asyncio import Queue
from utils import *
sudoku_csp = None
arcs = None

def ac3():
    
    queue = []
    print(1123)
    for arc in arcs:
        queue.append(arc)
    # print(queue)
    
    while len(queue) != 0:
        (Xi, Xj) = queue.pop()
        if revise(Xi, Xj):
            if len(sudoku_csp['domains'][Xi]) == 0:
                return False
            for Xk in sudoku_csp['variables']:
                if Xk != Xi and Xk != Xj:
                    queue.put((Xk, Xi))
    return True


def revise(Xi, Xj):
    revised = False
    for x in sudoku_csp['domains'][Xi]:
        if not any((x, y) for y in sudoku_csp['domains'][Xj] if sudoku_csp['constraints'][(Xi, Xj)](x, y)):
            sudoku_csp['domains'][Xi].remove(x)
            revised = True
    return revised


def print_tree():
    pass


if __name__ == "__main__":

    # Example Sudoku puzzle (0 represents an empty cell)
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    sudoku_csp = create_sudoku_csp(puzzle)
    print(sudoku_csp['constraints'])
    arcs = define_sudoku_arcs()
    ac3()
    for r in range(3):
        for c in range(3):
            print(sudoku_csp['domains'][(r, c)])
    

