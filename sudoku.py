from pprint  import pprint

def find_empty(matrix) -> (int, int) or (None, None):
    # finds the row or column that is empty (depicted by 0)
    for row in range(9):
        for col in range(9):
            if matrix[row][col] == 0:
                return row, col
    return None, None

def transpose(matrix) -> [[int]]:
    # turns rows into columns and columns into rows
    # useful for gathering the values of the columns
    return [[matrix[row][col] for row in range(len(matrix))] for col in range(len(matrix[0]))]


def determine_valid(matrix, guess, row, col) -> bool:
    # determines if the guess is valid, returns True if valid else False
    row_values = matrix[row]
    if guess in row_values:
        return False
    col_values = transpose(matrix)[col]
    if guess in col_values:
        return False
    # checks the row and columns in the 3 x 3 chunks that are in typical sudoku
    row_chunk = (row // 3) * 3
    col_chunk = (col // 3) * 3
    
    for i in range(row_chunk, row_chunk + 3, 1):
        for j in range(col_chunk, col_chunk + 3, 1):
            if guess == matrix[i][j]:
                return False
    return True

def determineSolvable(matrix) -> bool:
    # ensures that the starting board is solvable
    for row in matrix:
        #tracks all important values (0 is blank slot), returns False if any  
        #element is present more than once
        elements = [val for val in row if val != 0]
        if len(elements) != len(set(elements)):
            return False
    for col in transpose(matrix):
        #tracks all important values (0 is blank slot), returns False if any  
        #element is present more than once
        elements = [val for val in col if val != 0]
        if len(elements) != len(set(elements)):
            return False
    for i in range(0, 8, 3):
        for j in range(0, 8, 3):
            #grabs all the pieces in a 3x3 format, returns false
            #if any element is present more than once
            cube = [matrix[i][j], matrix[i][j+1], matrix[i][j+2], matrix[i+1][j], matrix[i+1][j+1], matrix[i+1][j+2], matrix[i+2][j], matrix[i+2][j+1], matrix[i+2][j+2]]
            l = [element for element in cube if element != 0]
            if len(set(l)) != len(l):
                return False

def solve(matrix) -> bool:
    # solves the sudoku using backtracking
    if determineSolvable(matrix) == False:
        return False
    row, col = find_empty(matrix)
    if row == None and col == None:
        return True
    for guess in range(1, 10):
        if determine_valid(matrix, guess, row , col):
            matrix[row][col] = guess
            if solve(matrix):
                return True
        matrix[row][col] = 0
    return False

if __name__ == '__main__':
    example_board = [
        [0, 9, 0,   1, 4, 0,   0, 0, 0],
        [0, 0, 5,   0, 0, 0,   0, 2, 0],
        [0, 3, 0,   0, 0, 0,   0, 6, 0],
        
        [0, 4, 6,   0, 0, 0,   0, 0, 0],
        [1, 2, 0,   9, 3, 0,   0, 4, 5],
        [0, 0, 3,   0, 0, 4,   0, 0, 6],
        
        [4, 0, 0,   0, 0, 1,   2, 0, 0],
        [0, 8, 0,   4, 0, 0,   0, 0, 3],
        [3, 5, 0,   7, 0, 0,   9, 0, 0]
    ]
    print(solve(example_board))
    pprint(example_board)
