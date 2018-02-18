from utility import *
import collections
import itertools

def cleaning_numbers(cells_status, cell_idx):
	clean_row(cell_idx, cells_status)
	clean_col(cell_idx, cells_status)
	clean_box(cell_idx, cells_status)
	print(" * check this number", row_cells(cell_idx), col_cells(cell_idx), box_cells(cell_idx))
	for i in set(row_cells(cell_idx) + col_cells(cell_idx) + box_cells(cell_idx)):
			print(cells_status[i])

def inference(cells_status, rule_id):
	if rule_id == 11:
		return naked_single(cells_status)
	else:
		changed = False
		for i in range(0,10):
			slot_idx = [i] + col_cells(i)
			changed = changed or inference_slots(cells_status, rule_id, slot_idx)
			slot_idx = [i] + row_cells(i)
			changed = changed or inference_slots(cells_status,rule_id, slot_idx)
			slot_idx = [i] + box_cells(i)
			changed = changed or inference_slots(cells_status, rule_id, slot_idx)
		return changed

def inference_slots(cells_status, rule_id, slot_idx):
	if rule_id == 12:
		return hidden_single(cells_status, slot_idx)
	elif rule_id == 21:
		return naked_pairs(cells_status, slot_idx)
	elif rule_id == 22:
		return hidden_pairs(cells_status, slot_idx)
	elif rule_id == 31:
		return naked_triples(cells_status, slot_idx)
	elif rule_id == 32:
		return hidden_triples(cells_status, slot_idx)
	else:
		print("Wrong rule_id!")
		exit(0)

# Assign to any cell a value x if it is the only value left in its domain
# I am alone in my cell and no other cells have my number.
# before = [[],[],[6,8,9],[6,7,9],[9],[7,9],[4,6,8,9],[],[]]
# target single value = 9
# after = [[],[],[6,8],[6,7,9],[],[7],[4,6,8],[],[]]
def naked_single(cells_status):
	print("=================== [Naked_Single] ===================")
	# count the lenth of domain for all cells
	remain_num = [len(elem[1]) for elem in cells_status.values()]
	idx_list = [index for index, value in enumerate(remain_num) if value == 1]

	changed = False
	for cell_idx in idx_list:
		print("* Change cell", idx_list)
		print("* Previous", cells_status[cell_idx])
		print("* Assigning value", cells_status[cell_idx][1][0])
		cells_status[cell_idx][0] = cells_status[cell_idx][1][0]
		cells_status[cell_idx][1] = []
		# remove this assigned value from the other relavant cells
		print("* Cleaning values in other cells...")
		cleaning_numbers(cells_status, cell_idx)
		print("* After", cells_status[cell_idx])
		changed = True
		return changed

# Assign to any cell a value x if x is not in the domain of any other cell
# in that row (column or box)
# There are a pair (no other numbers) in at least two cells.
# domain_col = [[],[],[2,6,7],[2,6],[],[2,6],[2,5,6],[],[4,5]]
# target single value = 7
# after = [[],[],[7],[2,6],[],[2,6],[2,5,6],[],[4,5]]
def hidden_single(cells_status, slot_idx):
	domain = [cells_status[x][1] for x in slot_idx]
	flat_list = [item for sublist in domain for item in sublist]
	counter = collections.Counter(flat_list)
	counter_values = collections.Counter(flat_list).values()
	counter_keys = collections.Counter(flat_list).keys()
	counter_idx_list = [index for index, value in enumerate(counter_values) if value == 1]

	changed = False
	if len(counter_idx_list) > 0:
		count_idx = counter_idx_list[0]
		value = counter_keys[count_idx]
		i = 0
		for sublist in domain:
			if value in sublist:
				cell_idx = slot_idx[i]
				print("=================== [Hidden_Single] ===================")
				print("* Change cell", cell_idx)
				print("* Domain", domain)
				print("* Previous", cells_status[cell_idx])
				print("* Assigning value", value)
				cells_status[cell_idx][0] = value
				cells_status[cell_idx][1] = []
				print("* Cleaning values in other cells...")
				cleaning_numbers(cells_status, cell_idx)
				print("* After", cells_status[cell_idx])
				changed = True
				return changed
			i = i + 1

# An identical pair that occurs in a row, column, or box.
# Remove it from other rows, columns or boxes that share both these cells.
# Two indentical pair: only two numbers in a cell and only two cells that have the pair
# domain = [[4,6],[],[4,6],[],[],[],[3,4,6,8],[],[3,4,6,8]]
# target pair = (4,6)
# after = [[4,6],[],[4,6],[],[],[],[3,8],[],[3,8]]
def naked_pairs(cells_status, slot_idx):
	domain = [cells_status[x][1] for x in slot_idx]
	dupes = [x for n, x in enumerate(domain) if x in domain[:n]]
	pair = [value for index, value in enumerate(dupes) if len(value) == 2]
	changed = False
	if (len(pair) > 0):
		for cell_idx in slot_idx:
			if(len(cells_status[cell_idx][1]) > 0 and cells_status[cell_idx][1] != pair[0]):
				common_values = set(cells_status[cell_idx][1]) & set(pair[0])
				if len(common_values) > 0:
					print("=================== [Naked_Pairs] ===================")
					print("* Change cell", cell_idx)
					print("* Domain", domain)
					print("* Previous", cells_status[cell_idx])
					print("* Pair", pair)
					cells_status[cell_idx][1] = list(set(cells_status[cell_idx][1]) - set(common_values))
					print("* After", cells_status[cell_idx])
					changed = True
	return changed

# A pair of numbers that occurs only in two cells in a row, column, or box.
# Eliminate the other numbers from them.
# Two identical pair with friends in only two cells: a pair with other numbers but only appear in two cells
# domain = [[],[1,7],[2,7,9],[3,4,5,7],[3,4,5,7],[3,4,7],[1,2,3,5,9],[1,3,5],[]]
# target pair = (2,9)
# after = [[4,6],[],[4,6],[],[],[],[3,8],[],[3,8]]
def hidden_pairs(cells_status, slot_idx):
	domain = [cells_status[x][1] for x in slot_idx]
	flat_list = [item for sublist in domain for item in sublist]
	counter_freq = collections.Counter(flat_list)
	counter_freq_values = collections.Counter(flat_list).values()
	counter_freq_keys = collections.Counter(flat_list).keys()
	counter_freq_idx = [index for index, value in enumerate(counter_freq_values) if value == 1]
	changed = False

	pair_list = []
	for i in domain:
		for pair in itertools.combinations(i, 2):
			pair_list.append(pair)

	counter_pair = collections.Counter(pair_list)
	counter_pair_values = collections.Counter(pair_list).values()
	counter_pair_keys = collections.Counter(pair_list).keys()
	counter_pair_idx = [index for index, value in enumerate(counter_pair_values) if value == 2]

	for counter_idx in counter_pair_idx:
		pair = counter_pair_keys[counter_idx]
		if (counter_freq[pair[0]] == 2 and counter_freq[pair[1]] == 2):
			cell_idx = [slot_idx[index] for index, value in enumerate(domain) if len(set(value) & set(pair)) == 2]
			for idx in cell_idx:
				print("=================== [Hidden_Pairs] ===================")
				print("* Change cell", idx)
				print("* Domain", domain)
				print("* Previous", cells_status[idx])
				print("* Pair", pair)
				cells_status[idx][1] = list(pair)
				print("* After", cells_status[idx])
				changed = True
			#break
			return changed

def naked_triples(cells_status, slot_idx):
	domain_col = [cells_status[x][1] for x in slot_idx]
	flat_list = [item for sublist in domain_col for item in sublist]
	triple_list = list(itertools.combinations(set(flat_list), 3))
	changed = False

	for triple in triple_list:
		cell_idx = [slot_idx[index] for index, value in enumerate(domain_col)
								if 	len(value) > 0 and
									len(set(triple) & set(value)) > 0 and
									len(set(value) - set(triple)) == 0]

		remain_cell_idx = set(slot_idx) - set(cell_idx)
		if len(cell_idx) == 3:
			for idx in remain_cell_idx:
				common_values = set(cells_status[idx][1]) & set(triple)
				if len(common_values) > 0:
					print("=================== [Naked_Triples] =================== ")
					print("* Change cell", idx)
					print("domain_col", domain_col)
					print("triple", triple)
					print("* Previous", cells_status[idx])
					cells_status[idx][1] = list(set(cells_status[idx][1]) - set(common_values))
					print("* After", cells_status[idx])
					changed = True
	return changed

def hidden_triples(cells_status, slot_idx):
	changed = False
	domain_col = [cells_status[x][1] for x in slot_idx]
	flat_list = [item for sublist in domain_col for item in sublist]
	triple_list = list(itertools.combinations(set(flat_list), 3))

	for triple in triple_list:
		cell_idx = [slot_idx[index] for index, value in enumerate(domain_col)
								if 	len(value) > 0 and
									len(set(triple) & set(value)) > 0]
		if len(cell_idx) == 3:
			for idx in cell_idx:
				common_values = list(set(triple) & set(cells_status[idx][1]))
				remove_values = list(set(cells_status[idx][1]) - set(common_values))
				if len(common_values) > 0 and len(remove_values) > 0:
					print("=================== [Naked_Triples] =================== ")
					print("* Change cell", idx)
					print("domain_col", domain_col)
					print("triple", triple)
					print("* Previous", cells_status[idx])
					cells_status[idx][1] = list(set(triple) & set(cells_status[idx][1]))
					print("* After", cells_status[idx])
					changed = True
			#break
			return changed