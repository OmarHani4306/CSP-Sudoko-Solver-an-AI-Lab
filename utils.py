import random


def generate_valid_sudoku(difficulty):
    board = [[0 for _ in range(9)] for _ in range(9)]
    clues_count = get_clue_count(difficulty)
    fill_board_randomly(board, clues_count)
    return board


def get_clue_count(difficulty):
    clue_counts = {"easy": 56, "medium": 36, "hard": 10}
    return clue_counts.get(difficulty, 36)


def fill_board_randomly(board, clues_count):
    empty_cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(empty_cells)

    for i, j in empty_cells[:clues_count]:
        possible_values = set(range(1, 10)) - set(board[i])
        possible_values -= set(board[x][j] for x in range(9))
        grid_row, grid_col = (i // 3) * 3, (j // 3) * 3
        possible_values -= {board[x][y] for x in range(grid_row, grid_row + 3) for y in range(grid_col, grid_col + 3)}
        if possible_values:
            board[i][j] = random.choice(list(possible_values))


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
