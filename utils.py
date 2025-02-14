

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

import random


def generate_valid_sudoku(difficulty):
    clues_count = get_clue_count(difficulty)
    board = fill_board_randomly(clues_count)
    return board


def get_clue_count(difficulty):
    clue_counts = {"easy": 56, "medium": 36, "hard": 10}
    return clue_counts.get(difficulty, 36)


def fill_board_randomly(clues_count):
    def is_valid(board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if solve(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    board = [[0 for _ in range(9)] for _ in range(9)]
    solve(board)  # Generate a valid Sudoku board

    clues = random.sample(range(81), clues_count)  # Randomly select positions to keep clues
    puzzle_board = [[0] * 9 for _ in range(9)]  # Reset the board for the puzzle

    for clue in clues:
        row, col = clue // 9, clue % 9
        puzzle_board[row][col] = board[row][col]

    return puzzle_board

def is_valid_board(board):
    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num == 0:
                continue
            if num in board[i][:j] or num in board[i][j + 1:]:
                return False
            if num in [board[x][j] for x in range(9)][:i] or num in [board[x][j] for x in range(9)][i + 1:]:
                return False
            grid_row = (i // 3) * 3
            grid_col = (j // 3) * 3
            for x in range(grid_row, grid_row + 3):
                for y in range(grid_col, grid_col + 3):
                    if board[x][y] == num and (x != i or y != j):
                        return False
    return True
