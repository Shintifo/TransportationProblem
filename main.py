import numpy as np
from tabulate import tabulate


def log(message):
	if LOG:
		print(message)


def north_west(supply, demand, cost):
	vector = []
	log("North-West:")
	s = np.copy(supply)
	d = np.copy(demand)
	current_state = (0, 0)
	distribution = np.zeros(shape=cost.shape)
	total_cost = 0
	while current_state[0] < s.shape[0] and current_state[1] < d.shape[0]:
		x, y = current_state
		distribution[current_state] = min(s[x], d[y])
		next_move = (1, 0) if distribution[current_state] == s[x] else (0, 1)
		next_state = tuple(map(sum, zip(current_state, next_move)))

		s[x] -= distribution[current_state]
		d[y] -= distribution[current_state]
		total_cost += distribution[current_state] * cost[current_state]
		current_state = next_state
	for row in distribution:
		for cell in row:
			vector.append(int(cell))
	log(vector)


def russel(supply, demand, cost):
	log("Russel rule:")
	s = np.copy(supply)
	d = np.copy(demand)
	c = np.copy(cost)
	total_cost = 0
	vector = []
	distribution = np.zeros(shape=c.shape)

	while np.any(s != 0) and np.any(d != 0):
		max_rows = c.max(axis=1)
		max_columns = c.max(axis=0)

		max_columns[np.where(np.isinf(max_columns))] = 0
		max_rows[np.where(np.isinf(max_rows))] = 0

		delta = c - max_columns - max_rows[:, np.newaxis]
		inf_indices = np.where(np.isinf(delta))
		delta[inf_indices] = np.inf

		min_val = np.unravel_index(delta.argmin(), delta.shape)
		delta[min_val] = 0

		if s[min_val[0]] == d[min_val[1]] == 0:
			continue

		distribution[min_val] = min(s[min_val[0]], d[min_val[1]])
		s[min_val[0]] -= distribution[min_val]
		d[min_val[1]] -= distribution[min_val]
		total_cost += distribution[min_val] * c[min_val]

		if s[min_val[0]] == 0:
			c[min_val[0]] = -np.inf
		elif d[min_val[1]] == 0:
			c[:, min_val[1]] = -np.inf

	for row in distribution:
		for cell in row:
			vector.append(int(cell))
	log(vector)


def vogel(supply, demand, cost):
	def col() -> list[int]:
		min_column_values = np.min(c, axis=0)

		second_column_min_values = np.partition(c, 1, axis=0)[1]
		second_column_min_values[np.isinf(second_column_min_values)] = 0

		column_penalties = abs(second_column_min_values - min_column_values)
		column_penalties[np.isinf(column_penalties)] = -np.inf
		return column_penalties

	def row() -> list[int]:
		min_row_values = np.min(c, axis=1)

		second_min_row_values = np.partition(c, 1, axis=1)[:, 1]
		second_min_row_values[np.isinf(second_min_row_values)] = 0

		rows_penalties = abs(second_min_row_values - min_row_values)
		rows_penalties[np.isinf(rows_penalties)] = -np.inf
		return rows_penalties

	log("Vogel rule:")
	s = np.copy(supply)
	d = np.copy(demand)
	c = np.copy(cost)
	vector = []
	distribution = np.zeros(shape=cost.shape)
	total_cost = 0

	while np.any(s != 0) and np.any(d != 0):
		column_penalties = col()
		rows_penalties = row()

		if max(column_penalties) < max(rows_penalties):
			row_index = np.argmax(rows_penalties)
			column_index = np.argmin(c[row_index])
			location = (row_index, column_index)
		else:
			column_index = np.argmax(column_penalties)
			row_index = np.argmin(c[:, column_index])
			location = (row_index, column_index)

		row_index, column_index = location

		if d[column_index] == s[row_index] == 0:
			break

		distribution[location] = min(d[column_index], s[row_index])
		total_cost += distribution[location] * c[location]

		if d[column_index] < s[row_index]:
			c[:, column_index] = np.inf

		elif d[column_index] > s[row_index]:
			c[row_index] = np.inf

		else:
			c[:, column_index] = np.inf
			c[row_index] = np.inf

		d[column_index] -= distribution[location]
		s[row_index] -= distribution[location]

	for row in distribution:
		for cell in row:
			vector.append(int(cell))
	log(vector)


def input(file_path):
	with open(file_path, "r") as file:
		supply = np.loadtxt(file, max_rows=1, skiprows=1)
		demand = np.loadtxt(file, max_rows=1, skiprows=1)
		cost = np.loadtxt(file, skiprows=1)

	if (cost.shape[0] != supply.shape[0] or cost.shape[1] != demand.shape[0]
			or np.any(cost == 0) or np.any(demand == 0)):
		print("The method is not applicable!")
		exit(1)
	if sum(supply) != sum(demand):
		print("The problem is not balanced!")
		exit(1)

	return supply, demand, cost


def print_parameter_table(s, d, c):
	log("Initial table:")
	table_list = np.column_stack((c, s)).tolist()
	table_list.append(d.tolist())

	headers = ['1', '2', '3', '4', 'S']
	table_format_options = {'numalign': 'center', 'stralign': 'center'}

	print(tabulate(table_list, headers, tablefmt="fancy_grid",
				   **table_format_options))


LOG = True

if __name__ == '__main__':
	s, d, c = input("input.txt")
	print_parameter_table(s, d, c)

	north_west(s, d, c)
	vogel(s, d, c)
	russel(s, d, c)
