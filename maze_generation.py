import random
import Parsing


def break_wall(grid, x1, y1, x2, y2):
	dx = x2 - x1
	dy = y2 - y1

	if dy == -1:
		grid[y1][x1] -= 1
		grid[y2][x2] -= 4
	elif dx == 1:
		grid[y1][x1] -= 2
		grid[y2][x2] -= 8
	elif dy == 1:
		grid[y1][x1] -= 4
		grid[y2][x2] -= 1
	elif dx == -1:
		grid[y1][x1] -= 8
		grid[y2][x2] -= 2


def generate_maze(maze):
	try:
		width = int(maze["WIDTH"])
		height = int(maze["HEIGHT"])
		x, y = maze["ENTRY"]
		is_perfect = maze["PERFECT"]

		stack = [(x, y)]
		directions = [
			(0, -1, 1),
			(1, 0, 2),
			(0, 1, 4),
			(-1, 0, 8),
		]
		visited = set()
		visited.add((x, y))
		grid = [[15 for _ in range(width)] for _ in range(height)]

		while stack:
			unvisited_cells = []
			current_x, current_y = stack[-1]

			for dir_x, dir_y, bit in directions:
				nx_x, nx_y = current_x + dir_x, current_y + dir_y
				if 0 <= nx_x < width and 0 <= nx_y < height and (nx_x, nx_y) not in visited:
					unvisited_cells.append((nx_x, nx_y, bit))
			
			if unvisited_cells:
				nx_x, nx_y, bit = random.choice(unvisited_cells)
				break_wall(grid, current_x, current_y, nx_x, nx_y)
				visited.add((nx_x, nx_y))
				stack.append((nx_x, nx_y))
			else:
				stack.pop()

		if not is_perfect:
            for _ in range(10):
                random_x = random.randrange(0, width)
                random_y = random.randrange(0, height)
                possible_walls = []

                for dir_x, dir_y, bit in directions:
                    nx, ny = random_x + dir_x, random_y + dir_y
            
                    if 0 <= nx < width and 0 <= ny < height:
                        if grid[random_y][random_x] & bit:
                            possible_walls.append((nx, ny, bit))
                
                if possible_walls:
                    target_x, target_y, bit = random.choice(possible_walls)
                    break_wall(grid, random_x, random_y, target_x, target_y)

		return grid
	except Exception as e:
		print(f"Error: an unexpected error occured {e}")