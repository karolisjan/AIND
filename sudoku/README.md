# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The naked twins is not so much a problem but more a strategy/rule that can
   be used to further reduce the search space. The naked twins, i.e. two boxes 
   within the same unit that share the same two values, are used to reduce the 
   total number of possible values within the same unit by eliminating the naked 
   twins values from all the other boxes in the same unit as naked twins. Once 
   the number of possible values is sufficiently reduced by"eliminate", "only-choice", 
   and "naked twins" strategies, depth-first search is used to explore the remaining possibilities. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The same way a regular sudoku is solved. The rules of a regular, i.e. numbers
   1 to 9 occurring once in rows, columns, and 3x3 boxes, are extended two diagonal
   units. This extra rule is used to solve the sudoku by applying "eliminate", 
   "only choice" and "naked twins" strategies. For example, whenever there is a box
   with a single value, this value is eliminated from the set of values of all 
   its peers, where peers are the boxes sharing the same row, column, 3x3 box, and a
   diagonal. This reduces significantly reduces the search space before depth-first 
   search is applied.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.