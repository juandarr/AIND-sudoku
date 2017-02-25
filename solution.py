#Initialization of array to store variable assignments
assignments = []

#Rows and cols strings
rows = 'ABCDEFGHI'
cols = '123456789'

#Switch to define if the sudoku to solve is a regular one or one with diagonal restrictions
isSudokuDiagonal = False

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

if (isSudokuDiagonal):
    a = [s for s in 'ABCDEFGHI']
    b = [s for s in '123456789']
    #One of the diagonal unit
    x1 = z = ["".join(item) for item in zip(a, b)]
    #The other diagonal unit
    a.reverse()
    x2 = ["".join(item) for item in zip(a, b)]
    diagonal_units = [x1]+[x2]
    unitlist = row_units + column_units + square_units + diagonal_units
else:
    unitlist = row_units + column_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    for unit in unitlist:
        #Store boxes with two digits in array
        twoDigits = [(box, values[box]) for box in unit if len(values[box])==2]
        toRemove = []
        for i in range(0,len(twoDigits)-1):
            for j in range(i+1,len(twoDigits)):
                if twoDigits[i][1]==twoDigits[j][1]:
                    # Store couples of boxes with the same value and the value in format [((box1,box2),value)]
                    toRemove += [((twoDigits[i][0],twoDigits[j][0]) , twoDigits[i][1])]
        # Eliminate the naked twins as possibilities for their peers
        #Go through all the elements of toRemove to delete same values in the unit
        for i in toRemove:
            for b in unit:
                if b not in i[0]:
                    for s in i[1]:
                        if (len(values[b]) > 1):
                            if (s in values[b]):
                                #Replace repeated value with ""
                                assign_value(values,b, values[b].replace(s, ""))
                                #values[b] = values[b].replace(s, "")

    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, "Grid length must be 81 for a 9x9 sudoku"
    return dict((boxes[i], '123456789' if grid[i] == '.' else grid[i]) for i in range(len(grid)))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

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
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
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
