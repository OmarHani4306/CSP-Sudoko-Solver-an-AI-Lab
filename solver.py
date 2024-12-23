from collections import deque
import tkinter as tk
from asyncio import Queue
from collections import deque


def create_sudoku_csp(puzzle):
    
    variables = [(r, c) for r in range(9) for c in range(9)]
    domains = {
        (r, c): [int(puzzle[r * 9 + c])] if puzzle[r * 9 + c] != '0' else list(range(1, 10))
        for r, c in variables
    }

    return {
        'variables': variables,
        'domains': domains,
    }

def select_unassigned_variable(csp, assignment):
    
    unassigned = [var for var in csp['variables'] if var not in assignment]
    return min(unassigned, key=lambda var: len(csp['domains'][var]))

def build_arcs():
    arcs = []

    # Add row arcs
    for r in range(9):
        for c1 in range(9):
            for c2 in range(c1 + 1, 9):
                arcs.append(((r, c1), (r, c2)))
                arcs.append(((r, c2), (r, c1)))

    # Add column arcs
    for c in range(9):
        for r1 in range(9):
            for r2 in range(r1 + 1, 9):
                arcs.append(((r1, c), (r2, c)))
                arcs.append(((r2, c), (r1, c)))

    # Add subgrid arcs
    for r_b in range(0, 9, 3):
        for c_b in range(0, 9, 3):
            cells = [(r, c) for r in range(r_b, r_b + 3) for c in range(c_b, c_b + 3)]
            for i in range(len(cells)):
                for j in range(i + 1, len(cells)):
                    arcs.append((cells[i], cells[j]))
                    arcs.append((cells[j], cells[i]))

    return arcs

def get_neighbors(var):
    
    r, c = var
    neighbors = set()

    # Row and Column
    for i in range(9):
        neighbors.add((r, i))
        neighbors.add((i, c))

    # Subgrid
    subgrid_r, subgrid_c = 3 * (r // 3), 3 * (c // 3)
    for i in range(subgrid_r, subgrid_r + 3):
        for j in range(subgrid_c, subgrid_c + 3):
            neighbors.add((i, j))

    neighbors.discard(var)  # Remove self
    return neighbors

def arc3(domains):
   
    queue = deque(arcs)  # Use dynamically built arcs
    log_buffer = []
    valid = True
    len_old_domains = [len(domains[(r, c)]) for r in range(9) for c in range(9)]
    log_buffer.append('\nBefore ARC Domains:')

    for r in range(9):
        for c in range(9):
            log_buffer.append(f"{(r, c)}: {domains[(r, c)]}")

    while len(queue) != 0:
        (Xi, Xj) = queue.popleft()

        if revise(domains, Xi, Xj):
            if len(domains[Xi]) == 0:  # If domain is empty, CSP is unsolvable
                valid = False
                break
            for xi, xj in arcs:
                if xj == Xi:
                    queue.append((xi, Xi))

    log_buffer.append('After ARC Domains:')

    for r in range(9):
        for c in range(9):
            if len(domains[(r, c)]) != len_old_domains[r * 9 + c]:
                log_buffer.append(f"{(r, c)}: {domains[(r, c)]}")

    with open('log.txt', 'a') as f:
        f.write('\n'.join(log_buffer))

    log_buffer.clear()
    return valid


def revise(domains, Xi, Xj):
    
    revised = False
    for x in domains[Xi][:]:  # Iterate over a copy of the domain of Xi
        if not any(x != y for y in domains[Xj]):  # Check if there's no consistent value in Xj
            domains[Xi].remove(x)  # Remove inconsistent value
            revised = True
    return revised

def order_domain_values(var, assignment, csp):
    
    def count_constraints(value):
        neighbors = get_neighbors(var)
        return sum(value in csp['domains'][neighbor] for neighbor in neighbors if neighbor not in assignment)

    return sorted(csp['domains'][var], key=count_constraints)


def board_to_string(assignment, initial_puzzle):  # take initial puzzle as input
   
    board = list(initial_puzzle)  # convert to list for mutability
    for (r, c), value in assignment.items():
        board[r * 9 + c] = str(value)  # update the board
    return "".join(board)  # convert back to string

def backtracking_search(csp):
    
    return backtrack({}, csp)

def backtrack(assignment, csp, states, initial_puzzle):
    if len(assignment) == len(csp['variables']):
        final_state = board_to_string(assignment, initial_puzzle)
        if final_state not in states: #Check for duplicates before appending the final state
            states.append(final_state)
        return assignment

    var = select_unassigned_variable(csp, assignment)
    for value in order_domain_values(var, assignment, csp):
        if is_consistent(var, value, assignment, csp):
            assignment[var] = value
            current_state = board_to_string(assignment, initial_puzzle)
            if current_state not in states:
                states.append(current_state)

            domains_copy = csp['domains'].copy()
            csp['domains'][var] = [value]
            
            if arc3(csp['domains']):
                result = backtrack(assignment, csp, states, initial_puzzle)
                if result:
                    return result

            csp['domains'] = domains_copy
            del assignment[var]

    return None

def is_consistent(var, value, assignment, csp):
    
    neighbors = get_neighbors(var)
    return all(value != assignment.get(neighbor) for neighbor in neighbors)


def solve_sudoku_with_states(puzzle):
    
    global arcs  # Use global to make arcs accessible across functions
    csp = create_sudoku_csp(puzzle)  # Create CSP representation
    arcs = build_arcs()  # Dynamically build arcs

    states = []  # List to record states
    assignment = {}  # Start with an empty assignment

    result = backtrack(assignment, csp, states, puzzle)  # Call backtracking search
    if result:
        print("Solved Sudoku!")
        return states
    else:
        print("No solution exists.")
        return None

    
