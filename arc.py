from asyncio import Queue
from collections import deque
import time
from utils import *
sudoku_csp = None
arcs = None

def arc3(domains):
    
    queue = deque(arcs)
    log_buffer = []
    valid = True

    log_buffer.append('Before ARC Domains:')

    for r in range(9):
        for c in range(9):
            log_buffer.append(f"{(r, c)}: {domains[(r, c)]}")

    while len(queue) != 0:
        
        # tmp = str(queue.popleft()).zfill(4)
        # Xi, Xj = (int(tmp[0]), int(tmp[1])), (int(tmp[2]), int(tmp[3]))
        (Xi, Xj) = queue.popleft()
        # print(Xi, Xj)
        # time.sleep(1)

        if revise(domains, Xi, Xj):
            if len(domains[Xi]) == 0:
                valid = False
                break
            # for temp in arcs:
            #     temp = str(temp).zfill(4)
            #     xi, xj = (int(temp[0]), int(temp[1])), (int(temp[2]), int(temp[3]))

            for xi, xj in arcs:
                if xj == Xi:
                    queue.append((xi, Xi))


        

    log_buffer.append('After ARC Domains:')

    for r in range(9):
        for c in range(9):
            log_buffer.append(f"{(r, c)}: {domains[(r, c)]}")

    with open('log.txt', 'w') as f:
        f.write('\n'.join(log_buffer))

    log_buffer.clear()

    return valid


def revise(domains, Xi, Xj):
    # return True
    revised = False
    for x in str(domains[Xi]):
        if not any((x, y) for y in str(domains[Xj]) if  int(x) != int(y)):
            domains[Xi] = str(domains[Xi]).replace(x, '')
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




    arcs = build_arcs()
    print(arcs[:10])
    print(arc3(sudoku_csp['domains']))
    check=3
    for r in range(check):
        for c in range(check):
            print(sudoku_csp['domains'][(r, c)])
