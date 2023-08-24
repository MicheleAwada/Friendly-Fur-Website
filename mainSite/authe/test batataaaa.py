def solve_sudoku(board):
    # Find an empty cell, if any
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True  # All cells are filled, puzzle solved

    row, col = empty_cell

    # Try placing digits from 1 to 9
    for num in map(str, range(1, 10)):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):  # Recursive call
                return True

            board[row][col] = '.'  # Backtrack if placement doesn't work

    return False  # No valid digit found, backtrack further


def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == '.':
                return i, j
    return None


def is_valid(board, row, col, num):
    # Check row and column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Check 3x3 box
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True


# Example Sudoku puzzle (0 or '.' represents an empty cell)

puzzle = [[".",".","9","7","4","8",".",".","."],
 ["7",".",".",".",".",".",".",".","."],
 [".","2",".","1",".","9",".",".","."],
 [".",".","7",".",".",".","2","4","."],
 [".","6","4",".","1",".","5","9","."],
 [".","9","8",".",".",".","3",".","."],
 [".",".",".","8",".","3",".","2","."],
 [".",".",".",".",".",".",".",".","6"],
 [".",".",".","2","7","5","9",".","."]]

solve_sudoku(puzzle)

# Printing the solved puzzle
print(puzzle)
for row in puzzle:
    print(" ".join(row))