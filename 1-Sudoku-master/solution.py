assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
	'''
	Cross product of elements in A and elements in B.
	Args:
		a(list) - a list with 'ABCDEFGHI'
		b(list) - a list with '123456789'
	Returns:
		 (list) - a list consists of 'A1', 'A2', ..., 'I9'. 
	'''
	return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [['A1','B2','C3','D4','E5','F6','G7','H8','I9'],['A9','B8','C7','D6','E5','F4','G3','H2','I1']]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)




def assign_value(values, box, value):
	"""
	replace the string in the dictionary values[box] with value
	Args:
		values(dict) - a dictionary of the form {'box_name': '123456789', ...}
		box(string) - a key of the dict pointing to the box that needs to be changed
		value(string) - a string that the values of values[box] should change into
	Returns:
		values(dict) - a dict with one of its box's value changed
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
	
	twin_numbers = ''				# a string that stores the two values of naked_twins boxes
	twin_box = ''					# a copy of the key of a box which has exactly two values
	twin_box2 = ''					# a copy of the key of a box which has the same values as the box found before
	same_unit = []					# a copy of the two boxes' same unit
	
	
	for box in values:				# in that loop, go through all boxes in the soduku
		same_unit = []				# for each loop, reset the value of same_unit
		if len(values[box]) == 2:			# if found a box with two values, record its key and value
			twin_numbers = values[box]
			twin_box = box
			for box in peers[twin_box]:		# search the box's peers to see if there are another box that has the same values, if so record the key
				if values[box] == twin_numbers:
					twin_box2 = box
					
					# search for the two boxes' same unit, then copy the unit to a new list
					
					for i in range(len(row_units)):		# search row_units
						found = False
						if box in row_units[i] and twin_box in row_units[i]:
							same_unit = row_units[i]
							found = True
					if not found:
						for i in range(len(column_units)):    	# search column_units
							if box in column_units[i] and twin_box in column_units[i]:
								same_unit = column_units[i]
								found = True
					if not found:
						for i in range(len(diagonal_units)):	# search diagonal_units
							if box in diagonal_units[i] and twin_box in diagonal_units[i]:
								same_unit = diagonal_units[i]
								found = True
					if not found:
						for i in range(len(square_units)):		# search square_units
							if box in square_units[i] and twin_box in square_units[i]:
								same_unit = square_units[i]
					break		# break the second loop and start eliminating 
				
				
				
			if same_unit:			# make sure if there are two boxes with the same two values and their same unit had been correctly copied
				for i in same_unit:			# for every box in the same unit except twins, remove the twin's two values
					if i == twin_box or i == twin_box2:			# skip the two boxes
						continue
					assign_value(values, i, values[i].replace(twin_numbers[0], ''))			# remove the first of the two values
					assign_value(values, i, values[i].replace(twin_numbers[1],''))			# remove the second of the two values
	return values		

def grid_values(grid):
	"""
	Convert grid into a dict of {square: char} with '123456789' for empties.
	Args:
		grid(string) - A grid in string form.
	Returns:
		A grid in dictionary form
			Keys: The boxes, e.g., 'A1'
			Values: The value in each box, e.g., ' 8'. If the box has no value, then the value will be '123456789'.
	"""
	chars = []
	digits = '123456789'
	for c in grid:
		if c in digits:
			chars.append(c)
		if c == '.':
			chars.append(digits)
	assert len(chars) == 81
	return dict(zip(boxes, chars))
	



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
	'''
	for any box with a single number in the values dictionary, remove that number in all of its peers boxes
	Args:
		values(dict): a dictionary of the form {'box_name': '123456789', ...}
	Return:
		values(dict): an updated dictionary 
	'''
	solved_values = [box for box in values.keys() if len(values[box]) == 1]
	for box in solved_values:
		digit = values[box]
		for peer in peers[box]:
			assign_value(values, peer, values[peer].replace(digit,''))
	return values

def only_choice(values):
	'''
	If there is number only in a box but not its peer boxes and that box contains more than one number, replace its value with the number
	Args:
		values(dict): a dictionary of the form {'box_name': '123456789', ...}
	Return:
		values(dict): an updated dictionary
	'''
	for unit in unitlist:
		for digit in '123456789':
			dplaces = [box for box in unit if digit in values[box]]
			if len(dplaces) == 1:
				assign_value(values, dplaces[0], digit)
	return values

def reduce_puzzle(values):
	'''
	constantly call eliminate and only_choice until the values dictionary stops changing
	Args:
		values(dict): a dictionary of the form {'box_name': '123456789', ...}
	Return:
		values(dict): an updated dictionary
	'''
	solved_values = [box for box in values.keys() if len(values[box]) == 1]
	stalled = False
	while not stalled:
		solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
		values = eliminate(values)
		values = only_choice(values)
		values = naked_twins(values)
		solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
		stalled = solved_values_before == solved_values_after
		if len([box for box in values.keys() if len(values[box]) == 0]):
			return False
	return values
	

def search(values):
	'''
	Pick a box with a minimal number of possible values. Try to solve each of the puzzles obtained by choosing each of these values, recursively
	Args:
		values(dict): a dictionary of the form {'box_name': '123456789', ...}
	Return:
		values(dict): an updated dictionary
	'''
	values = reduce_puzzle(values)
	if values is False:
		return False ## Failed earlier
	if all(len(values[s]) == 1 for s in boxes): 
		return values ## Solved!
	# Choose one of the unfilled squares with the fewest possibilities
	n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
	# Now use recurrence to solve each one of the resulting sudokus, and 
	for value in values[s]:
		new_sudoku = values.copy()
		#new_sudoku[s] = value
		assign_value(new_sudoku, s, value)
		attempt = search(new_sudoku)
		if attempt:
			return attempt

def solve(grid):
	"""
	Find the solution to a Sudoku grid.
	Args:
		grid(string): a string representing a sudoku grid.
			Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
	Returns:
		The dictionary representation of the final sudoku grid. False if no solution exists.
	"""
	values = grid_values(grid)
	result = search(values)
	if result:
		return result
	else: return False	

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
