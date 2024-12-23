def build_arcs():
    arcs = []

    # Add row arcs
    for r in range(9):
        for c1 in range(9):
            for c2 in range(c1 + 1, 9):
                arcs.append(((r, c1), (r, c2)))
                arcs.append(((r, c2), (r, c1)))
                # arcs.append(int(f"{r}{c1}{r}{c2}"))
                # arcs.append(int(f"{r}{c2}{r}{c1}"))

    # Add column arcs
    for c in range(9):
        for r1 in range(9):
            for r2 in range(r1 + 1, 9):
                arcs.append(((r1, c), (r2, c)))
                arcs.append(((r2, c), (r1, c)))
                # arcs.append(int(f"{r1}{c}{r2}{c}"))
                # arcs.append(int(f"{r2}{c}{r1}{c}"))

    # Add subgrid arcs
    for r_b in range(0, 9, 3):
        for c_b in range(0, 9, 3):
            cells = [
                # int(f"{r}{c}")
                (r, c)
                for r in range(r_b, r_b + 3)
                for c in range(c_b, c_b + 3)
            ]
            # print(cells)
            for i in range(len(cells)):
                for j in range(i + 1, len(cells)):
                    arcs.append((cells[i], cells[j]))
                    arcs.append((cells[j], cells[i]))
                    # print(cells[i], cells[j])
                    # print(cells[i] << 8 | cells[j])
                    # arcs.append(int(f"{cells[i]}{cells[j]}"))
                    # arcs.append(int(f"{cells[j]}{cells[i]}"))
 

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
        (r, c): puzzle[r][c] if puzzle[r][c] != 0 else 123456789
        for r, c in variables
    }
    # for r in range(9):
    #     for c in range(9):
    #         print((r, c), domains[(r, c)])  

    
    return {
        'variables': variables,
        'domains': domains,
    }

