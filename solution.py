import operator
from collections import defaultdict

assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

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
    # Eliminate the naked twins as possibilities for their peers

    'for each unit(row,col,square,diag) find boxes which has 2 options. store them in map'
    for u in unitlist:
      pairs=defaultdict(lambda: [])
      for b in u:
        if(len(values[b]) == 2):
          pairs[values[b]].append(b)
      'if 2 box has same option in a unit. start eliminating them from other boxes in unit'
      for p,bs in pairs.items():
        if(len(bs) == 2):
          for b in u:
            if(b not in bs):
              assign_value(values,b,''.join([c for c in values[b] if c not in p]))
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

"list of all boxes"
boxes = cross(rows, cols)

"list of rows. each row is list of boxes in that row"
row_units = [cross(r, cols) for r in rows]
"list of cols. each col is list of boxes in that col"
column_units = [cross(rows, c) for c in cols]
"list of squares. each square is list of boxes in that square"
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
"2 diagonals. each diagonal is list of boxes in that diagonal"
diag_units = [[s+t for (s,t) in zip(rows,cols)] , [s+t for (s,t) in zip(rows,cols[::-1])]]

unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

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
    return {k:(v if v!='.' else '123456789') for (k,v) in  zip(boxes,grid)}

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    singleValueBox = [b for b in boxes if len(values[b]) == 1]
    for b in singleValueBox:
        for p in peers[b]:
            assign_value(values,p,''.join([c for c in values[p] if c!=values[b]]))
    return values

def only_choice(values):
    for u in unitlist:
        choices=defaultdict(lambda: [])
        for b in u:
            for c in values[b]:
                choices[c].append(b)
        for c,b in choices.items():
            if len(b) == 1:
                assign_value(values,b[0],c)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = only_choice(eliminate(naked_twins(values)))

        # Your code here: Use the Only Choice Strategy

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values:
        solved_values = len([box for box in values.keys() if len(values[box]) == 1])
        if solved_values == 81:
            return values
        box = min([(box,len(values[box])) for box in values.keys() if len(values[box]) != 1],key=operator.itemgetter(1))[0]
        for c in values[box]:
            new_values = { k:(v if k!=box else c) for (k,v) in values.items()}
            result = search(new_values)
            if (result):
                return result
    else:
        return False

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
