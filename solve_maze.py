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


# TESTING
def debug_draw_maze(grid):
    width = len(grid[0])
    # Print top border
    print("+" + "---+" * width)
    
    for row in grid:
        # 1. Print the horizontal paths (West/East)
        row_str = "|"
        for cell in row:
            # If bit 2 (EAST) is NOT set, there is a path (space)
            # If it IS set, there is a wall (|)
            wall = " " if not (cell & 2) else "|"
            row_str += "   " + wall
        print(row_str)
        
        # 2. Print the vertical paths (North/South)
        bottom_str = "+"
        for cell in row:
            # If bit 4 (SOUTH) is NOT set, there is a path (space)
            wall = "   " if not (cell & 4) else "---"
            bottom_str += wall + "+"
        print(bottom_str)

if __name__ == "__main__":
    config = parsing.parse_data("test.txt")
    if config:
        grid = maze_generation.generate_maze(config)
        
        print("\n--- DEBUG MAZE VIEW ---")
        debug_draw_maze(grid)