import parsing
import maze_generation

from collections import deque


def solve_maze(grid, entry, exit):
	width = len(grid[0])
	height = len(grid)
	start = tuple(entry)
	end = tuple(exit)

	directions = [
        (0, -1, 1, 'N'),
        (1, 0, 2, 'E'),
        (0, 1, 4, 'S'),
        (-1, 0, 8, 'W'),
    ]
	queue = deque([start])
	paths = {start: None}

	while queue:
		cur_x, cur_y = queue.popleft()
		if (cur_x, cur_y) == end:
			return reconstruct_path(paths, start, end)
		
		for dir_x, dir_y, bit, char in directions:
			nx_x, nx_y = cur_x + dir_x, cur_y + dir_y
			if 0 <= nx_x < width and 0 <= nx_y < height:
				if not (grid[cur_y][cur_x] & bit) and (nx_x, nx_y) not in paths:
					paths[(nx_x, nx_y)] = ((cur_x, cur_y), char)
					queue.append((nx_x, nx_y))

	return "path not found"

def reconstruct_path(paths, start, end):
	current = end
	path_letter = []

	while current != start:
		(prev_x, prev_y), dir_char = paths[current]
		path_letter.append(dir_char)
		current = (prev_x, prev_y)

	return "".join(reversed(path_letter))


if __name__ == "__main__":
	config = parsing.parse_data("test.txt")

	if config and parsing.validate_config_data(config):
		grid = maze_generation.generate_maze(config)
		path = solve_maze(grid, config["ENTRY"], config["EXIT"])

	print(path)

