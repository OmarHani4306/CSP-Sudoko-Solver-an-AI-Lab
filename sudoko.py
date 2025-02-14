import tkinter as tk
from tkinter import messagebox
from time import time
from utils import generate_valid_sudoku, is_valid_board
from solver import *

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.board = [[tk.StringVar() for _ in range(9)] for _ in range(9)]
        self.create_board()

        self.mode_frame = tk.Frame(self.root)
        self.mode_frame.pack(pady=5)

        tk.Button(self.mode_frame, text="User Mode", command=self.user_mode).pack(side=tk.LEFT, padx=5)
        tk.Button(self.mode_frame, text="Computer Mode", command=self.computer_mode).pack(side=tk.LEFT, padx=5)

        self.difficulty_frame = None

        tk.Button(self.root, text="Solve", command=self.solve_puzzle).pack(pady=10)

        self.start_time = None  # Initialize start time

    def create_board(self):
        self.entries = []
        for i in range(9):
            row = []
            for j in range(9):
                entry = tk.Entry(self.frame, textvariable=self.board[i][j], width=2, font=('Arial', 18), justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                bg_color = "#e0e0e0" if (i // 3 + j // 3) % 2 == 0 else "white"
                entry.config(bg=bg_color)
                entry.configure({"disabledbackground": bg_color, "disabledforeground": "grey"})
                row.append(entry)
            self.entries.append(row)

    def user_mode(self):
        self.clear_board()
        self.enable_entries(True)
        if self.difficulty_frame:
            self.difficulty_frame.destroy()
            self.difficulty_frame = None
        

    def computer_mode(self):
        self.clear_board()
        self.enable_entries(False)
        if self.difficulty_frame:
            self.difficulty_frame.destroy()

        self.difficulty_frame = tk.Frame(self.root)
        self.difficulty_frame.pack(pady=5)

        tk.Label(self.difficulty_frame, text="Select Difficulty:").pack(side=tk.LEFT, padx=5)
        tk.Button(self.difficulty_frame, text="Easy", command=lambda: self.generate_puzzle("easy")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.difficulty_frame, text="Medium", command=lambda: self.generate_puzzle("medium")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.difficulty_frame, text="Hard", command=lambda: self.generate_puzzle("hard")).pack(side=tk.LEFT, padx=5)

    def generate_puzzle(self, difficulty):
        self.clear_board()
        
        puzzle = generate_valid_sudoku(difficulty)
        
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    self.board[i][j].set(puzzle[i][j])
        

    def clear_board(self):
        for i in range(9):
            for j in range(9):
                self.board[i][j].set("")

    def enable_entries(self, enable):
        for i in range(9):
            for j in range(9):
                if enable:
                    self.entries[i][j].config(fg="black", state=tk.NORMAL)
                else:
                    self.entries[i][j].config(fg="black", state=tk.DISABLED, disabledforeground="black")

    def solve_puzzle(self):
        user_board = [[0 for _ in range(9)] for _ in range(9)]
        try:
            for i in range(9):
                for j in range(9):
                    value = self.board[i][j].get()
                    if value != "" and (not value.isdigit() or not 1 <= int(value) <= 9):
                        raise ValueError
                    user_board[i][j] = int(value) if value != "" else 0
        except ValueError:
            messagebox.showerror("Invalid Board", "The Sudoku board is invalid!")
            return

        if is_valid_board(user_board):
            initial_state = ''.join(map(str, [item for sublist in user_board for item in sublist])).zfill(81)

            self.start_time = time()  # Start the timer *before* solving
            states = solve_sudoku_with_states(initial_state)
            end_time = time()      # Stop the timer *after* solving
            solving_time = end_time - self.start_time

            if states is None:
                messagebox.showerror("No Solution", "The board has no solution!")
                return

            states.insert(0, initial_state)
            self.simulate_gameplay(states, solving_time) # Pass solving time

        else:
            messagebox.showerror("Invalid Board", "The Sudoku board is invalid!")

    def simulate_gameplay(self, states, solving_time):
        self.state_idx = 0
        self.states = states
        self.solving_time = solving_time # Store solving time
        self.update_board()

    def update_board(self):
        state = self.states[self.state_idx]
        initial_state = self.states[0]

        for idx, char in enumerate(state):
            row, col = divmod(idx, 9)
            if char == "0":
                self.board[row][col].set("")
                self.entries[row][col].config(fg="black", state=tk.DISABLED, disabledforeground="black")
            else:
                self.board[row][col].set(char)
                if initial_state[idx] == "0" and char != "0":
                    self.entries[row][col].config(fg="red", state=tk.DISABLED, disabledforeground="red")
                else:
                    self.entries[row][col].config(fg="black", state=tk.DISABLED, disabledforeground="black")

        if self.state_idx < len(self.states) - 1:
            self.state_idx += 1
            self.root.after(10, self.update_board)
        else:
            messagebox.showinfo("Solved!", f"Puzzle solved in {self.solving_time:.4f} seconds.") # Display time

if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()