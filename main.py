from enum import Enum

import numpy as np


class TaskType(Enum):
	MAXIMIZE = 0,
	MINIMIZE = 1


def north_west(s: np.array(int), d: np.array(int), c: np.array(int)):
	current_state = (0, 0)
	distribution = np.zeros(shape=c.shape)
	ans = 0
	while current_state[0] < s.shape[0] and current_state[1] < d.shape[0]:
		distribution[current_state] = min(s[current_state[0]], d[current_state[1]])
		if distribution[current_state] == s[current_state[0]]:
			next_state = tuple(map(sum, zip(current_state, (1, 0))))
		else:
			next_state = tuple(map(sum, zip(current_state, (0, 1))))
		s[current_state[0]] -= distribution[current_state]
		d[current_state[1]] -= distribution[current_state]
		ans += distribution[current_state] * c[current_state]
		current_state = next_state
	print("Distribution:\n", distribution)
	print("Total cost: ", ans)


def russel(s: np.array(int), d: np.array(int), c: np.array(int)):
	max_rows = np.asarray([max(elem) for elem in c])
	max_columns = np.asarray([max(c[0:, column]) for column in range(d.shape[0])])

	delta = np.zeros(shape=c.shape)
	for i in range(s.shape[0]):
		for j in range(d.shape[0]):
			delta[i][j] = +c[i][j] - max_columns[j] - max_rows[i]

	print(delta)
	# while True:
	max_val = np.unravel_index(a.argmax(), a.shape)


def vogel(S: np.array(int), D: np.array(int), C: np.array(int)):
	print("vogel")


if __name__ == '__main__':
	tass_type = TaskType.MAXIMIZE
	accuracy = 0.001
	s = np.array([160, 140, 170])
	d = np.array([120, 50, 190, 110])

	c = np.array([[7, 8, 1, 2],
				  [4, 5, 9, 8],
				  [9, 2, 3, 6]])

	a = np.array([[1, 1, 21], [20, 20, 20]])
# russel(s, d, c)
