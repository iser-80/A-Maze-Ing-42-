import random

def break_wall(grid, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dy == -1: # North
        grid[y1][x1] -= 1
        grid[y2][x2] -= 4
    elif dx == 1: # East
        grid[y1][x1] -= 2
        grid[y2][x2] -= 8
    elif dy == 1: # South
        grid[y1][x1] -= 4
        grid[y2][x2] -= 1
    elif dx == -1: # West
        grid[y1][x1] -= 8
        grid[y2][x2] -= 2


def unlock_maze(maze):
    width = maze["WIDTH"]
    height = maze["HEIGHT"]
    grid = [[15 for _ in range(width)] for _ in range(height)]
    
    x, y = maze["ENTRY"]
    stack = [(x, y)]
    visited = set()
    visited.add((x, y))

    directions = [(0, -1, 1), (1, 0, 2), (0, 1, 4), (-1, 0, 8)]
    while stack:
        curr_x, curr_y = stack[-1]

        unvisited_cells = []
        for dx, dy, bit in directions:
            nx, ny = curr_x + dx, curr_y + dy

            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                unvisited_cells.append((nx, ny, dx, dy))
        
        if unvisited_cells:
            nx_x, nx_y, dx, dy = random.choice(unvisited_cells)

            break_wall(grid, curr_x, curr_y, nx_x, nx_y)

            visited.add((nx_x, nx_y))
            stack.append((nx_x, nx_y))
        else:
            stack.pop()
    
    return grid
