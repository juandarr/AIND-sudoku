# Sudoku agent solver

This program includes a Sudoku agent solver using several search and contraint propagation strategies as heuristics given any initial Sudoku configuration.

## Strategies

### Naked Twins

In this section we use constraint propagation to solve the naked twins problem. The constraint: given two boxes in the same unit with the same possible values of two digits, these two digits can only be included in these two boxes. 
Implication: these two digits are excluded as possible values for all the other boxes in the same unit.
When applying constraint propagation to solve a sudoku puzzle this exclusion strategy is used for every unit in the sudoku, and wherever
naked twins are found it may help to reduce the number of possible values by two. In the project, it helps to further reduce the
puzzle (since it is a different constraint in nature compared to elimination or only choice) and reach faster a potential solution.
As an example, let's say we have a unit with the values/possibilities, [25, 3, 647, 45 ,1 , 45, 3456, 9, 8]. A quick inspection shows
that box 4 and 6 are naked (visible) twins (couple). Since there are only two possible solutions: box4=4 and box6=5 or box4=5 and box6=4,
these two numbers are excluded from all the other boxes in the unit. Therefore, box 1 is reduced from 25 to 2, box 3 from 647 to 67,
box 7 is reduced from 3456 to 36 and we get a new simplified unit: [2, 3 , 67, 45 , 1, 45, 36, 9 , 8]. This constraint propagated
through all the units helps to reduce the whole puzzle.

### Diagonal Sudoku

Here we use constraint propagation to solve the diagonal sudoku problem. The constraint: for every unit there is a unique set of numbers from 1 to 9. In the regular sudoku puzzle we only propagate this constraint for rows, columns and regions. When we are dealing with a diagonal sudoku puzzle, we need to include two additional units where this elimination constraint has to be applied: one for the diagonal from top right to bottom left, one for the diagonal from top left to bottom right. This new set is added to the whole set of units required to solve just the
regular sudoku, getting a new total of 29 units (instead of the 27 units for the model of a regular sudoku). Once these units are
defined, the constraint 'elimination' (unique set of numbers from 1 to 9 for each unit) can be propagated through all the units, helping
to reduce the puzzle and combined with other techniques (naked twins, only choice, etc) to reach a solution where for every unit,
there is a unique set from 1 to 9.

# Instructions

This project requires **Python 3**.

We recommend the installation of [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - This file contains the implementation of the strategies. Run the agent with `python solution.py`. It will use Pygame if you have it installed in your system, otherwise it will print the solution on the terminal prompt.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.

# License

Copyright (c) Udacity and Juan David Rios. All rights reserved.

Licensed under the [MIT](https://github.com/juandarr/Sudoku-agent/blob/master/LICENSE) License.
