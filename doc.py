def isValid(grid, row, col, num):
    """
    Checks if it's valid to place the number 'num' at position (row, col) in the grid.
    """
    # Check row and column
    for x in range(9):
        if grid[row][x] == num or grid[x][col] == num:
            return False
    
    # Check 3x3 box
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] == num:
                return False
    
    return True

def solve_sudoku(grid, r=0, c=0):
    """
    Solves the Sudoku grid using backtracking algorithm and counts the number of solutions.

    Args:
    - grid (list): 2D list representing the Sudoku grid.
    - r (int): Row index (default: 0).
    - c (int): Column index (default: 0).

    Returns:
    - Tuple[bool, int]: Tuple containing a boolean indicating if Sudoku is solved and number of solutions found.
    """
    # Find the next empty cell
    while grid[r][c] != 0:
        print("a")
        c += 1
        if c == 9:
            r += 1
            c = 0
        if r == 9:
            return True, 1  # Entire grid filled, one solution found

    num_solutions = 0
    if num_solutions > 1:
        return False, num_solutions

    for k in range(1, 10):
        print("b")
        if isValid(grid, r, c, k):
            grid[r][c] = k
            solved, solutions = solve_sudoku(grid, r, c)
            num_solutions += solutions
            grid[r][c] = 0  # backtrack

    return True, num_solutions

# Example usage:
# Initialize your Sudoku grid
grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

solved, solutions = solve_sudoku(grid)
if solved:
    if solutions == 1:
        print("There is 1 solution.")
    else:
        print(f"There are {solutions} solutions.")
else:
    print("No solution found.")
