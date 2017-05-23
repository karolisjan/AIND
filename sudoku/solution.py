import re
import copy
from utils import *

assignments = []

def assign_value(values, box, value):
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(grid):
    """Eliminate values using the naked twins strategy.
    Args:

        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.

    """
    for unit in unit_list:
        #Find naked twins
        naked_twins = [[box1, box2] for i, box1 in enumerate(unit) 
                                    for box2 in unit[i+1:] 
                        if grid[box1] == grid[box2] and box1 != box2
                        and len(grid[box1]) == len(grid[box2]) == 2]

        #Eliminate the values of naked twins from their peers
        for twin1, twin2 in naked_twins: #In case there are more than 1 pair of naked twins
            for box in unit:
                if box != twin1 and box != twin2:
                    for d in grid[twin1]:
                        if len(grid[box]) >= len(grid[twin1]):
                            grid = assign_value(grid, box, re.sub(d, '', grid[box]))
    return grid

def eliminate(grid):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """    
    for box in grid:
        if len(grid[box]) == 1:
            for peer in peers[box]:
                grid[peer] = re.sub(grid[box], '', grid[peer])
    return grid

def only_choice(grid):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unit_list:
        for d in digits:
            choices = [box for box in unit if d in grid[box]]
            if len(choices) == 1:
                grid = assign_value(grid, choices[0], d)
    return grid

def reduce_puzzle(grid):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in grid if len(grid[box]) == 1])    
        grid = eliminate(grid)
        grid = only_choice(grid)
        grid = naked_twins(grid)
        solved_values_after = len([box for box in grid if len(grid[box]) == 1])    
        stalled = solved_values_after == solved_values_before
        if len([box for box in grid if len(grid[box]) == 0]):
            return False
    return grid

def search(grid):
    '''
    Apply Depth-First Search and Eliminate, One-choice, Naked Twins strategies 
    to solve the puzzle.
    '''    
    #Apply Eliminate, One-choice, and Naked Twins
    grid = reduce_puzzle(grid)
    
    #Base case
    if grid is False:
        return False
    if all(len(value) == 1 for value in grid.values()):
        return grid
        
    #Apply Depth-First Search starting from the box with the lower number of values
    box, val = sorted({box : grid[box] for box in grid if len(grid[box]) > 1}.items(),  
                              key=lambda x: len(x[1]))[0]
    for d in val:
        new_grid = assign_value(copy.copy(grid), box, d)
        solved_grid = search(new_grid)
        if solved_grid:
            return solved_grid
            
def solve(puzzle):
    grid = grid_values(puzzle)     
    return search(grid)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    solved_grid = solve(diag_sudoku_grid)
    if solved_grid:
        display(solved_grid)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
