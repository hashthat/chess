#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox

# Chessboard initialization (same as before)
def initialize_board():
    return [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"]
    ]

# Print board for debugging purposes (console)
def print_board(board):
    for row in board:
        print(" ".join(row))
    print()

# Function to update the board display
def update_gui_board(board, canvas, square_size=60):
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            color = "white" if (i + j) % 2 == 0 else "gray"
            x1, y1 = j * square_size, i * square_size
            x2, y2 = (j + 1) * square_size, (i + 1) * square_size

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

            if piece != ".":
                canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=piece, font=("Arial", 24))

# Handle move logic (updating the board state)
def move_piece(board, start, end):
    start_x, start_y = start
    end_x, end_y = end
    board[end_x][end_y] = board[start_x][start_y]
    board[start_x][start_y] = "."

# Parse the move (same logic as before)
def parse_move(move_str, color):
    if 'to' not in move_str:
        start_y = ord(move_str[0]) - ord('a')
        start_x = 6 if color == 'white' else 1
        end_x = 8 - int(move_str[1])
        end_y = ord(move_str[0]) - ord('a')
        return (start_x, start_y), (end_x, end_y)

    start, end = move_str.split(" to ")
    start_x = 8 - int(start[1])
    start_y = ord(start[0]) - ord('a')
    end_x = 8 - int(end[1])
    end_y = ord(end[0]) - ord('a')
    return (start_x, start_y), (end_x, end_y)

# Handle user click events on the board
def on_square_click(event, board, canvas, selected_square, color):
    x, y = event.x, event.y
    square_size = 60
    row, col = y // square_size, x // square_size

    if selected_square[0] is None:
        # First click to select piece
        selected_square[0] = (row, col)
        piece = board[row][col]
        if piece == "." or (color == "white" and piece.islower()) or (color == "black" and piece.isupper()):
            selected_square[0] = None  # Invalid piece selected
            return
    else:
        # Second click to select destination
        start = selected_square[0]
        end = (row, col)

        move = f"{chr(start[1] + 97)}{8 - start[0]} to {chr(end[1] + 97)}{8 - end[0]}"
        if validate_move(board, start, end, color):
            move_piece(board, start, end)
            selected_square[0] = None  # Reset selected square
            update_gui_board(board, canvas)  # Update the board display

def validate_move(board, start, end, color):
    piece = board[start[0]][start[1]]
    if color == "white" and piece.islower() or color == "black" and piece.isupper():
        return False  # Can't move opponent's piece
    # Add further validation logic here for specific piece movements
    return True

# Initialize the Tkinter window
def main():
    window = tk.Tk()
    window.title("Chess Game")

    # Set up the canvas to draw the chessboard
    canvas = tk.Canvas(window, width=480, height=480)
    canvas.pack()

    board = initialize_board()
    selected_square = [None]  # To track selected square

    # Draw the initial board
    update_gui_board(board, canvas)

    # Bind click event for square selection
    canvas.bind("<Button-1>", lambda event: on_square_click(event, board, canvas, selected_square, "white"))

    # Start the Tkinter event loop
    window.mainloop()

if __name__ == "__main__":
    main()

