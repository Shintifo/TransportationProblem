import numpy as np


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
		vector.append(int(distribution[current_state]))
		next_move = (1, 0) if distribution[current_state] == s[x] else (0, 1)
		next_state = tuple(map(sum, zip(current_state, next_move)))

		s[x] -= distribution[current_state]
		d[y] -= distribution[current_state]
		total_cost += distribution[current_state] * cost[current_state]
		current_state = next_state
	log(f"Vector:\n {vector}")
	# log(f"Distribution:\n {distribution}")
	# log(f"Total cost: {total_cost}\n")


def russel(supply, demand, cost):
	log("Russel rule:")
	s = np.copy(supply)
	d = np.copy(demand)
	c = np.copy(cost)
	total_cost = 0

	distribution = np.zeros(shape=c.shape)



	while np.any(s != 0) and np.any(d != 0):
		max_rows = c.max(axis=1)
		max_columns = c.max(axis=0)

		rows_indices = np.where(np.isinf(max_rows))
		columns_indices = np.where(np.isinf(max_columns))
		max_columns[columns_indices] = 0
		max_rows[rows_indices] = 0

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

	# log(f"Distribution:\n {distribution}")
	log(f"Total cost: {total_cost},\n")


def vogel(supply, demand, cost):
	"""
	How "columns()" and "rows()" function works?

	It finds min and second min values in each column or row, depending on the function.
	As matrix may have infinity both in rows and columns (that have been already distributed),
	It replaces infinity in second_min_values with 0
	and in penalties with -inf, to prevent from operations like:
		1) np.inf - np.inf
		2) np.inf - n (n = any number)
	For example:
		Matrix of costs:
		inf  inf  inf  inf
		inf   6    5    9
		inf  inf  inf inf
	Therefore:
			min_column = [inf, 6, 5, 9]
			second_min_column = [0, 0, 0, 0]
			penalty = [-inf, 6, 5 ,9]

	Hence, columns with fully distributed demand and rows with distributed supply are not considered.

	After that, do not do anything special, but ordinary steps of Vogel rule


	:param supply: Vector of supply
	:param demand: Vector of demand
	:param cost: Matrix of cost between supplies and demands
	"""

	def columns() -> tuple:
		min_column_values = np.min(c, axis=0)

		second_column_min_values = np.partition(c, 1, axis=0)[1]
		# Replace np.inf with 0
		second_column_min_values[np.isinf(second_column_min_values)] = 0

		column_penalties = abs(second_column_min_values - min_column_values)
		# Replace np.inf with -np.inf
		column_penalties[np.isinf(column_penalties)] = -np.inf

		column_index = np.argmax(column_penalties)
		row_index = np.argmin(c[:, column_index])
		return row_index, column_index

	def rows() -> tuple:
		min_row_values = np.min(c, axis=1)

		second_min_row_values = np.partition(c, 1, axis=1)[:, 1]
		second_min_row_values[np.isinf(second_min_row_values)] = 0

		rows_penalties = abs(second_min_row_values - min_row_values)
		rows_penalties[np.isinf(rows_penalties)] = -np.inf

		row_index = np.argmax(rows_penalties)
		column_index = np.argmin(c[row_index])
		location = (row_index, column_index)
		return location

	def apply_choose(location: tuple, cost: int) -> int:
		row_index, column_index = location

		if d[column_index] == s[row_index] == 0:
			return cost

		distribution[location] = min(d[column_index], s[row_index])
		vector.append(int(distribution[location]))
		cost += distribution[location] * c[location]

		if d[column_index] < s[row_index]:
			c[:, column_index] = np.inf

		elif d[column_index] > s[row_index]:
			c[row_index] = np.inf

		else:
			c[:, column_index] = np.inf
			c[row_index] = np.inf

		d[column_index] -= distribution[location]
		s[row_index] -= distribution[location]
		return cost

	log("Vogel rule:")
	s = np.copy(supply)
	d = np.copy(demand)
	c = np.copy(cost)
	vector = []
	distribution = np.zeros(shape=cost.shape)
	total_cost = 0

	while np.any(s != 0) and np.any(d != 0):
		total_cost = apply_choose(columns(), total_cost)
		total_cost = apply_choose(rows(), total_cost)

	log(f"Vector:\n {vector}")
	log(f"Distribution:\n {distribution}")
	log(f"Total cost: {total_cost},\n")


LOG = True


def input(file_path):
	try:
		with open(file_path, "r") as file:
			supply = np.array(file.readline().split()).astype(int)
			demand = np.array(file.readline().split()).astype(int)
			cost = np.loadtxt(file)
			cost = cost.reshape(3, 4)
			return supply, demand, cost

	except Exception as e:
		print(e)
		return None


def print_parameter_table(s, d, c):
	print("Initial parameter table:")
	print("  I   II   III   IV | S:")
	for i in range(3):
		for j in range(4):
			print(f"  {int(c[i][j])}  ", end="")
		print(f"| {s[i]}")
	print("D:", end="")
	for i in range(4):
		print(f" {int(d[i])} ", end="")
	print("\n")


if __name__ == '__main__':
	s, d, c = input("input.txt")
	print_parameter_table(s, d, c)

	# print(s)
	# print(d)
	# print(c)
	# TODO output
	# north_west(s, d, c)
	# vogel(s, d, c)
	russel(s, d, c)
