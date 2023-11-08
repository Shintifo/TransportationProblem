import numpy as np


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
	print("Total cost:", total_cost)


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
	print("Total cost:", total_cost)


def vogel(supply, demand, cost):
	s = np.copy(supply)
	d = np.copy(demand)
	min_column_values = np.min(cost, axis=0)
	second_column_min_values = np.partition(cost, 1, axis=0)[1]

	min_row_values = np.min(cost, axis=1)
	second_min_row_values = np.partition(cost, 1, axis=1)[:, 1]


if __name__ == '__main__':
	s = np.array([300, 400, 500])
	d = np.array([250, 350, 400, 200])
	c = np.array([[3, 1, 7, 4],
				  [2, 6, 5, 9],
				  [8, 3, 3, 2]])

	north_west(s, d, c)
	russel(s, d, c)
