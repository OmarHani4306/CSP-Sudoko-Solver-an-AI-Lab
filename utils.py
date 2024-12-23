def define_sudoku_arcs():
    """
    Define arcs for a Sudoku CSP based on rows, columns, and 3x3 subgrids.
    
    Returns:
        list: A list of all arcs (tuples of variable pairs).
    """
    arcs = []

    # Add row arcs
    for r in range(9):
        for c1 in range(9):
            for c2 in range(c1 + 1, 9):
                arcs.append(((r, c1), (r, c2)))
                arcs.append(((r, c2), (r, c1)))  # Add reverse arc

    # Add column arcs
    for c in range(9):
        for r1 in range(9):
            for r2 in range(r1 + 1, 9):
                arcs.append(((r1, c), (r2, c)))
                arcs.append(((r2, c), (r1, c)))  # Add reverse arc

    # Add subgrid arcs
    for r_b in range(0, 9, 3):
        for c_b in range(0, 9, 3):
            cells = [
                (r, c)
                for r in range(r_b, r_b + 3)
                for c in range(c_b, c_b + 3)
            ]
            for i in range(len(cells)):
                for j in range(i + 1, len(cells)):
                    arcs.append((cells[i], cells[j]))
                    arcs.append((cells[j], cells[i]))  # Add reverse arc

    return arcs


def create_sudoku_csp(puzzle):
    """
    Create a CSP representation for a Sudoku puzzle.
    
    Args:
        puzzle (list of list): A 9x9 grid where 0 represents an empty cell, and other numbers are fixed values.
    
    Returns:
        dict: A CSP with 'variables', 'domains', and 'constraints'.
    """
    variables = [(r, c) for r in range(9) for c in range(9)]
    domains = {
        (r, c): {puzzle[r][c]} if puzzle[r][c] != 0 else set(range(1, 10))  
        for r, c in variables
    }
    # for r in range(9):
    #     for c in range(9):
    #         print((r, c), domains[(r, c)])  
    

    sudoku_constraint = lambda x, y: x != y
    constraints = {}
    
    # Add row constraints
    for r in range(9):
        for c1 in range(9):
            for c2 in range(c1 + 1, 9):
                constraints[((r, c1), (r, c2))] = sudoku_constraint
    
    # Add column constraints
    for c in range(9):
        for r1 in range(9):
            for r2 in range(r1 + 1, 9):
                constraints[((r1, c), (r2, c))] = sudoku_constraint
    
    # Add subgrid constraints
    for r_b in range(0, 9, 3):
        for c_b in range(0, 9, 3):
            cells = [
                (r, c)
                for r in range(r_b, r_b + 3)
                for c in range(c_b, c_b + 3)
            ]
            for i in range(len(cells)):
                for j in range(i + 1, len(cells)):
                    constraints[(cells[i], cells[j])] = sudoku_constraint
    
    return {
        'variables': variables,
        'domains': domains,
        'constraints': constraints,
    }

