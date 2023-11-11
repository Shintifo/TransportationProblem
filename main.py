import numpy as np

LOG = True

def log(message):
	if LOG:
		print(message)

def north_west(supply, demand, cost):
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
	log(f"Total cost: {total_cost}")


def russel(supply, demand, cost):
	s = np.copy(supply)
	d = np.copy(demand)
	total_cost = 0
	distribution = np.zeros(shape=cost.shape)

	min_rows = cost.max(axis=1)
	min_columns = cost.max(axis=0)
	delta = cost - min_columns - min_rows[:, np.newaxis]

	while np.any(s != 0) and np.any(d != 0):
		min_val = np.unravel_index(delta.argmin(), delta.shape)
		delta[min_val] = 0
		if s[min_val[0]] == d[min_val[1]] == 0:
			continue
		distribution[min_val] = min(s[min_val[0]], d[min_val[1]])
		s[min_val[0]] -= distribution[min_val]
		d[min_val[1]] -= distribution[min_val]
		total_cost += distribution[min_val] * cost[min_val]
	log(f"Total cost: {total_cost}")


def vogel(supply, demand, cost):
	def columns() -> tuple:
		min_column_values = np.min(c, axis=0)

		second_column_min_values = np.partition(c, 1, axis=0)[1] # Replace np.inf with 0
		second_column_min_values[np.isinf(second_column_min_values)] = 0

		column_penalties = abs(second_column_min_values - min_column_values) # Replace np.inf with 0
		column_penalties[np.isinf(column_penalties)] = 0

		column_index = np.argmax(column_penalties)
		row_index = np.argmin(c[:, column_index])
		location = (row_index, column_index)
		return location

	def rows() -> tuple:
		min_row_values = np.min(c, axis=1)

		second_min_row_values = np.partition(c, 1, axis=1)[:, 1]
		second_min_row_values[np.isinf(second_min_row_values)] = 0

		rows_penalties = abs(second_min_row_values - min_row_values)
		rows_penalties[np.isinf(rows_penalties)] = 0

		row_index = np.argmax(rows_penalties)
		column_index = np.argmin(c[row_index])
		location = (row_index, column_index)
		return location

	def f(location: tuple, total_cost:int):
		row_index, column_index = location

		if d[column_index] < s[row_index]:
			distribution[location] = d[column_index]
			total_cost += distribution[location] * c[location]
			c[:, column_index] = np.inf

		elif d[column_index] > s[row_index]:
			distribution[location] = s[row_index]
			total_cost += distribution[location] * c[location]
			c[row_index] = np.inf

		else:
			distribution[location] = d[column_index]
			total_cost += distribution[location] * c[location]
			c[:, column_index] = np.inf
			c[row_index] = np.inf

		d[column_index] -= distribution[location]
		s[row_index] -= distribution[location]
		return total_cost

	s = np.copy(supply)
	d = np.copy(demand)
	c = np.copy(cost)
	distribution = np.zeros(shape=cost.shape)
	total_cost = 0

	while np.any(s != 0) and np.any(d != 0):
		total_cost = f(columns(), total_cost)
		print(distribution)
		total_cost = f(rows(), total_cost)
		print(distribution)

	log(f"Distribution:\n {distribution}")
	log(f"Total_dist: {total_cost}")


if __name__ == '__main__':
	s = np.array([300, 400, 500])
	d = np.array([250, 350, 400, 200])
	c = np.array([[3, 1, 7, 4],
						  [2, 6, 5, 9],
						  [8, 3, 3, 2]], dtype=float)


	# north_west(s, d, c)
	vogel(s, d, c)
	# russel(s, d, c)

