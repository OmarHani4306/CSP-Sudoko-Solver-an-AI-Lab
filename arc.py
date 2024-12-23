from asyncio import Queue
from utils import *
sudoku_csp = None
arcs = None


def ac3():
    
    queue = []
    print(1123)
    queue.extend(arcs)
    log_buffer = []
    valid = True

    log_buffer.append('Before ARC Domains:')

    for r in range(9):
        for c in range(9):
            log_buffer.append(f"{(r, c)}: {sudoku_csp['domains'][(r, c)]}")
    
    while len(queue) != 0:
        (Xi, Xj) = queue.pop()
        
        if revise(Xi, Xj):
            if len(sudoku_csp['domains'][Xi]) == 0:
                valid = False
                break
            for Xk in sudoku_csp['variables']:
                if Xk != Xi and Xk != Xj and (Xk, Xi) not in queue:
                    queue.append((Xk, Xi))
            # break

    log_buffer.append('After ARC Domains:')

    for r in range(9):
        for c in range(9):
            log_buffer.append(f"{(r, c)}: {sudoku_csp['domains'][(r, c)]}")

    with open('log.txt', 'a') as f:
        f.write('\n'.join(log_buffer))

    log_buffer.clear()

    return valid


def revise(Xi, Xj):
    # return True
    revised = False
    for x in sudoku_csp['domains'][Xi].copy():
        if not any((x, y) for y in sudoku_csp['domains'][Xj] if  x != y):
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

    arcs = define_sudoku_arcs()
    print(ac3())
    check=3
    for r in range(check):
        for c in range(check):
            print(sudoku_csp['domains'][(r, c)])
    

