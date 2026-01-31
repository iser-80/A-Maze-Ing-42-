import random
import parse_data

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

def export_maze(config, grid, path_string=""):
    output_file = config.get("OUTPUT_FILE", "maze.txt")
    
    with open(output_file, "w") as f:
        f.write(str(grid) + "\n")
        f.write("\n")
        
        entry = config["ENTRY"]
        exit_ = config["EXIT"]
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_[0]},{exit_[1]}\n")
        
        f.write(path_string + "\n")
    
    print(f"Successfully exported maze data to {output_file}")

if __name__ == "__main__":
    CONFIG_FILE = "test.txt"
    
    print(f"--- Step 1: Parsing {CONFIG_FILE} ---")
    config = parse_data.read_map(CONFIG_FILE)
    
    # 3. Validate the configuration
    if config and parse_data.validate_config(config):
        print("Config Validated.")
        
        print(f"--- Step 2: Generating {config['WIDTH']}x{config['HEIGHT']} Maze ---")
        final_grid = unlock_maze(config) 
        
        print(f"--- Step 3: Exporting to {config.get('OUTPUT_FILE')} ---")
        export_maze(config, final_grid, path_string="PATH_PENDING_BFS")
        
        print("\nthe output file is created")
    else:
        print("Error: Maze generation aborted due to invalid config.")