from flask import request, session
import numpy as np
import chess

def handle_dark_mode():
    if "dark_mode" not in session:
        session["dark_mode"] = False
    if request.method == "POST":
        session["dark_mode"] = not session["dark_mode"]


# def handle_sudoku_input():
#     sudoku_puzzle = np.empty((9,9), dtype=int)
#     for i in range(0,9):
#         for j in range(0,9):
#             sudoku_puzzle[i,j] = get_digit(request.form[f"r{i}c{j}"])
#     return sudoku_puzzle


def get_digit(usr_input):
    digits = {"1","2","3","4","5","6","7","8","9",
              "-1","-2","-3","-4","-5","-6"}
    if usr_input in digits:
        return int(usr_input)
    else:
        return 0


def handle_grid_input(num_rows,num_cols):
    grid = np.empty((num_rows,num_cols), dtype=int)
    for i in range(0,num_rows):
        for j in range(0,num_cols):
            grid[i,j] = get_digit(request.form[f"r{i}c{j}"])
    return grid


def chess_to_numpy(board, colour):
    """
    Convert the chessboard object to a numpy array.
    """
    np_board = np.zeros((8, 8), dtype=np.int8)
    # Define a mapping between chess pieces and their values
    piece_values = {'p':  6, 'r':  3, 'n':  5, 'b':  4, 'q':  2, 'k':  1,
                    'P': -6, 'R': -3, 'N': -5, 'B': -4, 'Q': -2, 'K': -1}
    # Iterate over the squares and fill the NumPy array
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            piece_symbol = piece.symbol()
            np_board[chess.square_rank(square)][chess.square_file(square)] = piece_values[piece_symbol]
    if colour == "black":
        return np_board
    else:
        return np_board[::-1]


def squares_to_uci(selected_squares, colour):
    """
    Convert the selected squares input to uci string.
    """
    columns = ["a","b","c","d","e","f","g","h"]
    rows = [str(num) for num in range(8,0,-1)]
    if colour == "black":
        columns.reverse()
        row.reverse()
    uci_string = ""
    uci_string += columns[int(selected_squares[0][1])]
    uci_string += rows[int(selected_squares[0][0])]
    uci_string += columns[int(selected_squares[1][1])]
    uci_string += rows[int(selected_squares[1][0])]
    return uci_string
