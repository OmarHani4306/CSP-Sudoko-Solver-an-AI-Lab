# CSP-Sudoko-Solver

## Overview  
This project implements a **Sudoku Solver** using **Constraint Satisfaction Problem (CSP) techniques**. It supports:  
- **Automatic solving** of Sudoku puzzles using Backtracking and Arc Consistency (AC-3).  
- **User-input mode**, allowing players to enter their own Sudoku puzzles for the AI to solve.  
- **Random puzzle generation** with validation to ensure solvability.  

## Features  
✅ **Graphical User Interface (GUI)** for easy interaction.  
✅ **Backtracking Search** for solving and validating puzzles.  
✅ **Arc Consistency (AC-3)** to enforce constraints dynamically.  
✅ **Supports 9x9 Sudoku grids** with standard rules.  

## Algorithms Used  
### 1. **Backtracking Search**  
- Used for puzzle validation (ensuring a given Sudoku board is solvable).  
- Generates **random Sudoku puzzles** by filling the board and removing numbers while ensuring solvability.  

### 2. **Arc Consistency (AC-3)**  
- **Defines Sudoku as a CSP** where each cell is a variable, and constraints enforce row, column, and 3x3 subgrid rules.  
- **Reduces domains** by eliminating values that violate Sudoku rules before searching.  
- **Optimizes solving speed** by reducing the number of backtracking steps.  

## How It Works  
1. **User Input Mode**:  
   - Enter a partially completed Sudoku board.  
   - The AI **applies Arc Consistency** and **solves the puzzle**.  

2. **Auto-Solve Mode**:  
   - The AI generates a **random valid puzzle**.  
   - Uses **Backtracking & AC-3** to fill the board.  
