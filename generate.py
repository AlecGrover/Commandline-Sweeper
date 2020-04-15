import itertools


def get_offsets(n, top=False, bottom=False, left=False, right=False):
    if not top and not bottom and not left and not right:
        offsets = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
        return [offset_set for offset_set in itertools.combinations(offsets, n)]
    if top:
        if right:
            offsets = [(0, -1), (-1, -1), (-1, 0)]
            return [offset_set for offset_set in itertools.combinations(offsets, n)]
        if left:
            offsets = [(1, 0), (1, -1), (0, -1)]
            return [offset_set for offset_set in itertools.combinations(offsets, n)]
        offsets = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
        return [offset_set for offset_set in itertools.combinations(offsets, n)]
    if bottom:
        if right:
            offsets = [(-1, 0), (-1, 1), (0, 1)]
            return [offset_set for offset_set in itertools.combinations(offsets, n)]
        if left:
            offsets = [(1, 1), (1, 0), (0, 1)]
            return [offset_set for offset_set in itertools.combinations(offsets, n)]
        offsets = [(1, 1), (1, 0), (-1, 0), (-1, 1), (0, 1)]
        return [offset_set for offset_set in itertools.combinations(offsets, n)]
    if right:
        offsets = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
        return [offset_set for offset_set in itertools.combinations(offsets, n)]
    if left:
        offsets = [(1, 1), (1, 0), (1, -1), (0, -1), (0, 1)]
        return [offset_set for offset_set in itertools.combinations(offsets, n)]


def is_edge(curr_board, i, j):
	top=False
	bottom=False
	left=False
	right=False
	# left edge
	if i == 0:
		left = True
	# right edge
	if i == len(curr_board) - 1:
		right = True
	# bottom edge
	if j == 0:
		bottom = True
	# top edge
	if j == len(curr_board[0]) - 1:
		top = True
	return (top, bottom, left, right)

def find_negative_constraints(clause, i, j, curr_board):
	offsets_cpmr = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
	# negate all neighbors that are enforced in the clause
	for offset in offsets_cpmr:
		point = (i+offset[0], j+offset[1])
		# check if point is not out of bounds
		if point[0] >= 0 and point[0] <= (len(curr_board)-1) and point[1] >= 0 and point[1] <= (len(curr_board[0])-1):
			if point not in clause:
				# check if point is not explored already
				if curr_board[point[0]][point[1]] == "?":
					clause.append("-{}".format(point))
	return clause

def clause_to_string(clause):
	ret = "{}".format(str(clause[0]))
	for i in range(1, len(clause)):
		ret += " {}".format(str(clause[i]))
	return ret

def offsets_to_constraints(i, j, offsets, curr_board):
	to_write = ""
	# f.write("Now the file has more content!")
	constraints = []
	# print("\nat cell ({},{}) constraints are:".format(i,j))
	for combination in offsets:
		clause = []
		for offset in combination:
			point = (i+offset[0], j+offset[1])
			# add to constraints only if not explored
			if curr_board[point[0]][point[1]] == "?":
				# cell_id = len(curr_board[0])*point[0] + point[1]
				clause.append(point)
			else:
				clause = []
				break
		if clause != []:
			clause = find_negative_constraints(clause, i, j, curr_board)
			clause = clause_to_string(clause)
			to_write += clause+"\n"
	return to_write

def save_constraints(to_write, filename):
	f = open(filename, "w")
	f.write(to_write)
	print("Constraints have been generated and saved into {}".format(filename))
	return 0

def generate_constraints(curr_board, filename="constraints.txt"):
	constraints = ""
	for i in range(len(curr_board)):
		row = curr_board[i]
		for j in range(len(row)):
			n = row[j]
			# only check for explored boxes
			if n != "?":
				# check if edge
				top, bottom, left, right = is_edge(curr_board, i, j)
				# find offsets
				offsets = get_offsets(n, top, bottom, left, right)
				if offsets != [()]:
					constraints += offsets_to_constraints(i, j, offsets, curr_board)
	print(constraints)
	save_constraints(constraints, filename)
	return 0
	
