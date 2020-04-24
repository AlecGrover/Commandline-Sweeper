import itertools
from sympy.logic.boolalg import to_cnf

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

def translate(point, row_len):
	x, y = point
	return "x"+str(x*row_len + y)

def find_negative_constraints(clause, i, j, curr_board):
	offsets_cpmr = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
	# negate all neighbors that are enforced in the clause
	for offset in offsets_cpmr:
		point = (i+offset[0], j+offset[1])
		# check if point is not out of bounds
		if point[0] >= 0 and point[0] <= (len(curr_board)-1) and point[1] >= 0 and point[1] <= (len(curr_board[0])-1):
			point_translated = translate(point, len(curr_board[0]))
			if point_translated not in clause:
				# check if point is not explored already
				if curr_board[point[0]][point[1]] == "?":
					clause.append("~{}".format(point_translated))
	return clause

def clause_to_string(clause):
	ret = "{}".format(str(clause[0]))
	for i in range(1, len(clause)):
		ret += " & {}".format(str(clause[i]))
	return ret

def format_correctly(to_write, op):
	ret = "("
	for i in range(len(to_write)):
		elem = to_write[i]
		ret += elem 
		if i != len(to_write)-1:
			ret += " {} ".format(op)
	ret += ")"
	return ret

def offsets_to_constraints(i, j, offsets, curr_board):
	# print("\ncell ({},{})".format(i, j))
	to_write = []
	for combination in offsets:
		clause = []
		for offset in combination:
			point = (i+offset[0], j+offset[1])
			# add to constraints only if not explored
			if curr_board[point[0]][point[1]] == "?":
				# cell_id = len(curr_board[0])*point[0] + point[1]
				clause.append(translate(point, len(curr_board[0])))
			else:
				clause = []
				break
		if clause != []:
			clause = find_negative_constraints(clause, i, j, curr_board)
			clause = clause_to_string(clause)
			to_write.append("("+clause+ ")")
	to_write = format_correctly(to_write, "|")
	# print("DNF: ",to_write)
	to_write = to_cnf(to_write, simplify=True)
	# print("CNF: ",to_write)
	return str(to_write)

def save_constraints(to_write, filename):
	f = open(filename, "w")
	f.write(to_write)
	# print("\nConstraints have been generated and saved into {}".format(filename))
	return 0

def parse_multiple(interval):
	ret = []
	num = ""
	for char in interval:
		if char == "~":
			num += "-"
		if char.isdigit():
			num += char
		if char == "|" or char == ")":
			ret.append(int(num))
			num = ""
	return ret

def parse_one(num):
	ret = ''
	for char in num:
		if char == "~":
			ret += "-"
		if char.isdigit():
			ret += char
	return [int(ret)]

def dpll_format(constraints):
	ret = []
	constraints = constraints.split("&")
	for elem in constraints:
		# multiple
		if len(elem) > 7:
			ret.append(parse_multiple(elem))
		else:
			ret.append(parse_one(elem))
	return ret

def generate_constraints(curr_board, filename="constraints.txt"):
	constraints = []
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
					constraints.append(offsets_to_constraints(i, j, offsets, curr_board))
	# fix constraints
	constraints = format_correctly(constraints, "&")
	# get rid of the extra brackets
	constraints = constraints[1:len(constraints)-1]
	constraints = dpll_format(constraints)
	# save_constraints(constraints, filename)
	return constraints

