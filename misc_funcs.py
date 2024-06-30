from flask import request, session
import numpy as np
import chess
from sudoku import Sudoku


def session_handling():
    if "dark_mode" not in session:
        session["dark_mode"] = False
    if "language" not in session:
        session["language"] = "english"
    if request.method == "POST":
        form_type = request.form.get("form_type")
        if form_type == "dark_mode":
            print("!!form type is dank mode!!")
            session["dark_mode"] = not session["dark_mode"]
        elif form_type == "language":
            print("!!form type is lang!!")
            print(f"old language = {session['language']}")
            if session["language"] == "english":
                session["language"] = "chinese"
            elif session["language"] == "chinese":
                session["language"] = "english"
            print(f"new language = {session['language']}")

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


def generate_random_puzzle():
    difficulty = np.random.rand()*0.5 + 0.25
    seed = np.random.randint(10000)
    puzzle = Sudoku(3, seed=seed).difficulty(difficulty).board
    # Change None to empty string
    puzzle = [[cell if cell is not None else "" for cell in row] for row in puzzle]
    return puzzle


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
        return np.flip(np_board, axis=1)
    else:
        return np.flip(np_board, axis=0)


def squares_to_uci(selected_squares, colour):
    """
    Convert the selected squares input to uci string.
    """
    columns = ["a","b","c","d","e","f","g","h"]
    rows = [str(num) for num in range(8,0,-1)]
    if colour == "black":
        rows.reverse()
        columns.reverse()
    uci_string = ""
    uci_string += columns[int(selected_squares[0][1])]
    uci_string += rows[int(selected_squares[0][0])]
    uci_string += columns[int(selected_squares[1][1])]
    uci_string += rows[int(selected_squares[1][0])]
    return uci_string

# def board_to_bitwise(board, colour):
#     def is_upper(string):
#         return string.isupper()

#     def is_lower(string):
#         return string.islower()

#     if colour == "white":
#         your_piece = is_upper
#     else:
#         your_piece = is_lower

#     bit_board = np.zeros((6,8,8), dtype=int)

#     for square in chess.SQUARES:
#         piece = board.piece_at(square)
#         if piece is None:
#             continue
#         piece = piece.symbol()
#         if piece.lower() == "p":
#             if your_piece(piece):
#                 bit_board[0][chess.square_rank(square)][chess.square_file(square)] = 1
#             else:
#                 bit_board[0][chess.square_rank(square)][chess.square_file(square)] = -1
#         elif piece.lower() == "n":
#             if your_piece(piece):
#                 bit_board[1][chess.square_rank(square)][chess.square_file(square)] = 1
#             else:
#                 bit_board[1][chess.square_rank(square)][chess.square_file(square)] = -1
#         elif piece.lower() == "b":
#             if your_piece(piece):
#                 bit_board[2][chess.square_rank(square)][chess.square_file(square)] = 1
#             else:
#                 bit_board[2][chess.square_rank(square)][chess.square_file(square)] = -1
#         elif piece.lower() == "r":
#             if your_piece(piece):
#                 bit_board[3][chess.square_rank(square)][chess.square_file(square)] = 1
#             else:
#                 bit_board[3][chess.square_rank(square)][chess.square_file(square)] = -1
#         elif piece.lower() == "q":
#             if your_piece(piece):
#                 bit_board[4][chess.square_rank(square)][chess.square_file(square)] = 1
#             else:
#                 bit_board[4][chess.square_rank(square)][chess.square_file(square)] = -1
#         elif piece.lower() == "k":
#             if your_piece(piece):
#                 bit_board[5][chess.square_rank(square)][chess.square_file(square)] = 1
#             else:
#                 bit_board[5][chess.square_rank(square)][chess.square_file(square)] = -1

#     if colour == "black":
#         return np.flip(bit_board, axis=2)
#     else:
#         return np.flip(bit_board, axis=1)