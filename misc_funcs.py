from flask import request, session
import numpy as np

def handle_dark_mode():
    if "dark_mode" not in session:
        session["dark_mode"] = False
    if request.method == "POST":
        session["dark_mode"] = not session["dark_mode"]


def handle_sudoku_input():
    sudoku_puzzle = np.empty((9,9), dtype=int)
    for i in range(0,9):
        for j in range(0,9):
            sudoku_puzzle[i,j] = get_sudoku_digit(request.form[f"r{i}c{j}"])
    return sudoku_puzzle

def get_sudoku_digit(usr_input):
    digits = {"1","2","3","4","5","6","7","8","9"}
    if usr_input in digits:
        return int(usr_input)
    else:
        return 0