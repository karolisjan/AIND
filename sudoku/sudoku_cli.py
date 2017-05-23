# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 22:36:30 2017

Sudoku solver

Use:
    $ python sudoku_cli.py puzzle
    
    where puzzle is a concatenation of all the readings of the digits in the rows,
    taking the rows from top to bottom. If the puzzle is not solved, a . is used 
    a placeholder for an empty box.
    
Example:
    $ python sudoku_cli.py 4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......

Uses constraint propagation and depth-first search for a first pass.
If unsuccessful, uses backtracking to solve the puzzle.
    
@author: Karolis
"""

import sys
import re
import copy
from utils import *
    
def backtrack(puzzle):
    '''
    Use backtacking to solve any puzzle in case constraint propagation and
    depth-first search fail.
    '''
    steps = 0
    go_back = False
    next_num = 1
    c = 0
    r = 0
    
    puzzle = {boxes[i] : 0 if val is '.' else int(val) for i, val in enumerate(puzzle)}
    grid = copy.copy(puzzle)
            
    def if_valid(box):
        for peer in peers[box]:
            if grid[box] == grid[peer]:
                return False
        return True
                   
    while True:
        if c > 8:
            c = 0
            r += 1
            if r > 8:
                return grid, steps
            
        if next_num > 9:
            go_back = True
            if puzzle[rows[r]+cols[c]] == 0:
                grid[rows[r]+cols[c]] = 0
            if c == 0:
                c = 9
                r -= 1
            c -= 1
            next_num = grid[rows[r]+cols[c]] + 1
        
        if puzzle[rows[r]+cols[c]] == 0:
            for i in range(next_num, 10):
                grid[rows[r]+cols[c]] = i
                if if_valid(rows[r]+cols[c]):
                    go_back = False
                    c += 1
                    next_num = 1
                    break
                elif i == 9:
                    go_back = True
                    grid[rows[r]+cols[c]] = 0
                    if c == 0:
                        c = 9
                        r -= 1
                    c -= 1
                    next_num = grid[rows[r]+cols[c]] + 1
                    break
        else:
            if go_back:
                if c == 0:
                    c = 9
                    r -= 1
                c -= 1
                next_num = grid[rows[r]+cols[c]] + 1
            else:
                c += 1                            
        steps += 1
        if steps % 1e7 == 0:
            print("Still running... %d steps" % steps)

def naked_twins(grid):
    """Eliminate values using the naked twins strategy.
    Args:

        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.

    """
    for unit in unit_list:
        naked_twins = [[box1, box2] for i, box1 in enumerate(unit) 
                                    for box2 in unit[i+1:] 
                        if grid[box1] == grid[box2] and box1 != box2
                        and len(grid[box1]) == len(grid[box2]) == 2]
        for twin1, twin2 in naked_twins:
            for box in unit:
                if box != twin1 and box != twin2:
                    for d in grid[twin1]:
                        if len(grid[box]) >= len(grid[twin1]):
                            grid[box] = re.sub(d, '', grid[box]) 
    return grid

def grid_values(puzzle):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """    
    return {boxes[i] : digits if val is '.' else val for i, val in enumerate(puzzle)}

def display(grid):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(str(grid[s])) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(str(grid[r+c]).center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)

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
                grid[choices[0]] = d
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
        grid = naked_twins(grid)
        grid = only_choice(grid)
        solved_values_after = len([box for box in grid if len(grid[box]) == 1])    
        stalled = solved_values_after == solved_values_before
        if len([box for box in grid if len(grid[box]) == 0]):
            return False
    return grid

def search(grid):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    grid = reduce_puzzle(grid)
    if grid is False:
        return False
    if all(len(value) == 1 for value in grid.values()):
        return grid
    box, val = sorted({box : grid[box] for box in grid if len(grid[box]) > 1}.items(),  
                       key=lambda x: len(x[1]))[0]
    for d in val:
        new_grid = copy.copy(grid)
        new_grid[box] = d
        solved_grid = search(new_grid)
        if solved_grid:
            return solved_grid

def solve(puzzle):
    grid = grid_values(puzzle)
    return search(grid)

if __name__ == '__main__':
    puzzle = sys.argv[1]
    
    assert len(puzzle) == 81, 'puzzle_string must be 81 chars long'

    for val in puzzle:
        if val is not '.':
            assert val in digits, 'puzzle_string can only contain \'.\' or digits 1-9' 
    
    solved_grid = solve(puzzle)
    if solved_grid:
        display(solved_grid)
        print("\nSolved using Constraint Propagation and Depth-First Search!")
    else:
        print("\nConstraint Propagation and Depth-First Search failed. Running Backtracking...\n")
        solved_grid, steps = backtrack(puzzle)
        display(solved_grid)
        print("\nSolved using Backtracking in %d steps!" % steps)

    