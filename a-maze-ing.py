import time
import os
import sys

def parsing(file_name):
    if not os.path.isfile(file_name):
        print(f"Error the config file {file_name} was not found")
        sys.exit(1)
    config = {}
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config
class Maze:
    N, E, S, W = 1, 2, 4, 8
    def __init__(self, config):
        self.config = config
        self.solution_path = ""
        self.width = int(config.get('WIDTH', 10))
        self.height = int(config.get('HEIGHT', 10))
        entry = config.get('ENTRY', "0,0")
        self.entry = [int(x) for x in entry.split(",")]
        self.grid = [[15 for _ in range(self.width)]
                     for _ in range(self.height)]
        print(f"Maze created {self.width}x{self.height}")

    def display(self, show_path = False, color_mode = 0):
        colors = [
            '\033[31m',
            '\033[32m',
            '\033[33m',
            '\033[34m',
            '\033[35m',
            '\033[36m',
            '\033[37m',
        ]
        RESET = '\033[0m'
        PATH_COLOR = '\033[35m'

        if color_mode == 0:
            wall_color = '\033[37m'
        elif color_mode == 1:
            wall_color = '\033[31m'
        elif color_mode == 2:
            color = int(time.time() * 5) % len(colors)
            wall_color = colors[color]
        else:
            wall_color = '\033[34m'

        WALL = f"{wall_color}██{RESET}"
        SPACE = "  "
        path_cells = set()
        if show_path and self.solution_path:
            cx, cy = self.entry
            path_cells.add((cx, cy))
            for move in self.solution_path:
                if move == 'N': 
                    cy -= 1
                elif move == 'S':
                    cy += 1
                elif move == 'E':
                    cx += 1
                elif move == 'W':
                    cx -= 1
                path_cells.add((cx, cy))
        sys.stdout.write("\033[H\033[J")
        canvas_height = self.height * 2 + 1
        canvas_width = self.width * 2 + 1

        canvas = [[WALL for _ in range(canvas_width)]
                  for _ in range(canvas_height)]
        for y in range(self.height):
            for x in range(self.width):
                cy = y * 2 + 1
                cx = x * 2 + 1

                if (x,y) in path_cells:
                    canvas[cy][cx] = f"{PATH_COLOR}██{RESET}"
                else:
                    canvas[cy][cx] = SPACE

                cell = self.grid[y][x]

                if not (cell & self.N):
                    canvas[cy - 1][cx] = SPACE
                if not (cell & self.S):
                    canvas[cy + 1][cx] = SPACE
                if not (cell & self.W):
                    canvas[cy][cx - 1] = SPACE
                if not (cell & self.E):
                    canvas[cy][cx + 1] = SPACE
        for row in canvas:
            print("".join(row))
        sys.stdout.flush()
    def save_into_file(self):
        file_name = self.config.get("OUTPUT_FILE", "maze.txt")

        try:
            with open(file_name, "w") as f:
                for row in self.grid:
                    f.write("".join(hex(cell)[2:].upper() for cell in row) + "\n")
                f.write("\n")

                f.write(f"{self.entry[0]}, {self.entry[1]}\n")
                exitv = self.config.get("EXIT", f"{self.width - 1}, {self.height -1}")
                f.write(f"{exitv}\n")
                solution = getattr(self, "solution_path", "")
                f.write(f"{solution}\n")
        except Exception as e:
            print(f"Error saving file: {e}")
# from solve_maze import s
from maze_generator import MazeGenerator
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("please add the config file")
        sys.exit(1)
    config = parsing(sys.argv[1])
    maze = Maze(config)
    generator = MazeGenerator(
        maze.width,maze.height,
        maze.entry,maze.config.get("EXIT", f"{maze.width - 1}, {maze.height -1}"),
        True,
        42
    )
    generator.generate_maze()
    maze.grid = generator.grid
    maze.solution_path = generator.solve_maze()
    print(maze.solution_path)
    color_mode = 0
    show_path = False
    while True:
        print("1 . Re-generatre a new maze")
        print("2 . SHOW/HIDE path from entry to exit")
        print("3 . Rotate maze colors")
        print("4 . Quit")
        choice = int(input("Choice? (1-4):"))
        if choice == 1:
            # maze.grid = MazeGenerator.generate_maze(config)
            maze.display(color_mode = 0)
        elif choice == 2:
            
            show_path = not show_path
            maze.display(show_path, color_mode)
        elif choice == 3:
            maze.display(color_mode = 1)
        elif choice == 4:
            sys.exit(0)

    # myconfig = parsing(config)
    # for i, j in myconfig.items():
    #     print(f"{i} = {j}")
    # maze = Maze(myconfig)
    # print(maze.grid[0][0])
    # maze
