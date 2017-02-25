from utilities import *

def instancesNaked(unit,values):
    """Find all the instances of naked twins in a unit
    Args:
        unit: a unit defining a set of boxes in the model
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        an array of tuples with all the naked twin instances in the unit in format [((box1,box2),value),...]
    """
    # Store boxes with two digits in array
    twoDigits = [(box, values[box]) for box in unit if len(values[box]) == 2]
    toRemove = []
    for i in range(0, len(twoDigits) - 1):
        for j in range(i + 1, len(twoDigits)):
            if twoDigits[i][1] == twoDigits[j][1]:
                # Store couples of boxes with the same value and the value in format [((box1,box2),value)]
                toRemove += [((twoDigits[i][0], twoDigits[j][0]), twoDigits[i][1])]
    return toRemove

def removeNakedValues(nakedInstancesForUnit,unit,values):
    """Remove naked values from all the peers of naked boxes in a unit
    Args:
        nakedInstancesForUnit: an array of tuples with form [((box1, box2), value),...]
        unit: a unit defining a set of boxes in the model
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    """
    # Go through all the elements of toRemove to delete same values in the unit
    for i in nakedInstancesForUnit:
        for b in unit:
            if b not in i[0]:
                for s in i[1]:
                    if (len(values[b]) > 1):
                        if (s in values[b]):
                            # Replace repeated value with ""
                            assign_value(values, b, values[b].replace(s, ""))
                            # values[b] = values[b].replace(s, "")

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Go through every unit
    for unit in unitlist:
        # Find all instances of naked twins in each unit
        nakedInstancesForUnit = instancesNaked(unit, values)

        # Eliminate the naked twins as possibilities for their peers in each unit
        removeNakedValues(nakedInstancesForUnit,unit,values)
    return values

def eliminate(values):
    """Eliminate values from peers of each box with a single value.
    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for i in values.keys():
        if (len(values[i]) == 1):
            for p in peers[i]:
                if (len(values[p]) > 1):
                    if (values[i] in values[p]):
                        assign_value(values, p, values[p].replace(values[i], ""))
                        #values[p] = values[p].replace(values[i], "")
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    numbers = '123456789'
    for unit in unitlist:
        for digit in numbers:
            boxesWithDigit = []
            for box in unit:
                if digit in values[box]:
                    boxesWithDigit += [box]
            if len(boxesWithDigit) == 1:
                assign_value(values, boxesWithDigit[0], digit)
                #values[boxesWithDigit[0]] = digit
    return values

def reduce_puzzle(values):
    """
        Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
        If the sudoku is solved, return the sudoku.
        If after an iteration of both functions, the sudoku remains the same, return the sudoku.
        Input: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check the number of solved boxes before
        before_solved_boxes = len([box for box in values.keys() if len(values[box]) == 1])
        # Elimination
        eliminate(values)
        # Naked twins
        naked_twins(values)
        # Only choice
        only_choice(values)
        # Check the number of solved boxes after
        after_solved_boxes = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = before_solved_boxes == after_solved_boxes
        # Sanity check: return false if the value of some box is empty
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """Using depth-first search and propagation, create a search tree and solve the sudoku.
    Args:
        values(dict): Sudoku in dictionary form.

    Returns:
        Solution if there is one or false
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:
        return False
    # Choose one of the unfilled squares with the fewest possibilities
    unfilled_values = [(box, int(len(values[box]))) for box in values.keys() if len(values[box]) > 1]
    if len(unfilled_values) == 0:
        return values
    unfilled_values.sort(key=lambda tup: tup[1])
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for s in values[unfilled_values[0][0]]:
        new_values = values.copy()
        new_values[unfilled_values[0][0]] = s
        result = search(new_values)
        if result:
            return result

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
