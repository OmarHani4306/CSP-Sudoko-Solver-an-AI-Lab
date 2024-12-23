import tkinter as tk
from tkinter import messagebox
from utils import generate_valid_sudoku, is_valid_board
from solver import *
class SudokuGame:
    def __init__(self, root):
        # Initialize the main game window
        self.root = root
        self.root.title("Sudoku Game")

        # Board frame: A frame to hold the Sudoku grid
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        # Create a 9x9 board using StringVar for dynamic updates
        self.board = [[tk.StringVar() for _ in range(9)] for _ in range(9)]
        self.create_board()

        # Mode selection frame: Buttons to choose User Mode or Computer Mode
        self.mode_frame = tk.Frame(self.root)
        self.mode_frame.pack(pady=5)

        tk.Button(self.mode_frame, text="User Mode", command=self.user_mode).pack(side=tk.LEFT, padx=5)
        tk.Button(self.mode_frame, text="Computer Mode", command=self.computer_mode).pack(side=tk.LEFT, padx=5)

        self.difficulty_frame = None

        # Solve button: Button to trigger solving the current puzzle
        tk.Button(self.root, text="Solve", command=self.solve_puzzle).pack(pady=10)


    def create_board(self):
        """Create the 9x9 Sudoku grid with entry widgets."""
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
        """Switch to User Mode where the user can enter their own Sudoku puzzle."""
        self.clear_board()
        self.enable_entries(True)
        if self.difficulty_frame:
            self.difficulty_frame.destroy()
            self.difficulty_frame = None
        messagebox.showinfo("Mode Selected", "User Mode Selected. Enter your Sudoku puzzle.")


    def computer_mode(self):
        """Switch to Computer Mode where a Sudoku puzzle is generated based on difficulty."""
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
        """Generate a new Sudoku puzzle based on the selected difficulty level."""
        self.clear_board()
        puzzle = generate_valid_sudoku(difficulty)
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    self.board[i][j].set(puzzle[i][j])
        messagebox.showinfo("Puzzle Generated", f"{difficulty.capitalize()} puzzle generated")


    def clear_board(self):
        """Clear the Sudoku board by resetting all cells."""
        for i in range(9):
            for j in range(9):
                self.board[i][j].set("")


    def enable_entries(self, enable):
        """Enable or disable the entry widgets for user input."""
        for i in range(9):
            for j in range(9):
                if enable:
                    self.entries[i][j].config(fg="black", state=tk.NORMAL)
                else:
                    self.entries[i][j].config(fg="black", state=tk.DISABLED, disabledforeground="black")


    def solve_puzzle(self):
        """Solve the current Sudoku puzzle entered by the user."""
        user_board = [[0 for _ in range(9)] for _ in range(9)]

        with open('log.txt', 'w') as f:
            pass
        
        for i in range(9):
            for j in range(9):
                try:
                    # Attempt to get the value from the entry widget and convert to int
                    value = self.board[i][j].get()
                    
                    # Check if the value is an integer and within the valid range
                    if value != "" and (not value.isdigit() or not 1 <= int(value) <= 9):
                        raise ValueError

                    # If valid, update the user_board
                    user_board[i][j] = int(value) if value != "" else 0
                except ValueError:
                    messagebox.showerror("Invalid Board", "The Sudoku board is invalid!")
                    return
                    
        if is_valid_board(user_board):
            # Flatten the user_board to create the initial state
            initial_state = ''.join(map(str, [item for sublist in user_board for item in sublist])).zfill(81)
            
            # Solve the Sudoku and get all intermediate states
            states = solve_sudoku_with_states(initial_state)
            
            if states is None:
                messagebox.showerror("No Solution", "The board has no solution!")
                return
            
            # Insert the initial state at the beginning of the list of states
            states.insert(0, initial_state)
            
            # Simulate the gameplay with the states
            self.simulate_gameplay(states)
        else:
            messagebox.showerror("Invalid Board", "The Sudoku board is invalid!")


    def simulate_gameplay(self, states):
        """Simulate gameplay by updating the board step by step."""

        self.state_idx = 0
        self.states = states

        self.update_board()


    def update_board(self):
        """Update the board to the next state in the predefined sequence."""
        state = self.states[self.state_idx]
        initial_state = self.states[0]

        for idx, char in enumerate(state):
            row, col = divmod(idx, 9)
            if char == "0":
                self.board[row][col].set("")
                self.entries[row][col].config(fg = "black", state=tk.DISABLED, disabledforeground="black")
            else:
                self.board[row][col].set(char)
                if initial_state[idx] == "0" and char != "0":
                    self.entries[row][col].config(fg="red", state=tk.DISABLED, disabledforeground="red")
                else:
                    self.entries[row][col].config(fg="black", state=tk.DISABLED, disabledforeground="black")

        if self.state_idx < len(self.states) - 1:
            self.state_idx += 1
            self.root.after(10, self.update_board)
        

if __name__ == "__main__":
    # Start the Tkinter main loop to run the Sudoku game
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()
