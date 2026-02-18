import sys
from .a_maze_ing import Maze, parsing
from .maze_generator import MazeGenerator
def main():
    if len(sys.argv) != 2:
        print("please add the config file")
        sys.exit(1)
    config = parsing(sys.argv[1])
    maze = Maze(config)
    rseed = maze.config.get("SEED", "").strip()
    seed = None if rseed == "" else int(rseed)  
    generator = MazeGenerator(
        maze.width, maze.height,
        maze.entry,
        maze.config.get("EXIT", f"{maze.width - 1}, {maze.height - 1}"),
        True,
        seed
    )
    generator.generate_maze(maze=maze, animate=True)
    maze.grid = generator.grid
    maze.pattern_42 = generator.blocked
    maze.solution_path = generator.solve_maze()
    maze.display()
    color_mode = 0
    show_path = False
    maze.save_into_file()
    while True:
        print("1 . Re-generatre a new maze")
        print("2 . SHOW/HIDE path from entry to exit")
        print("3 . Rotate maze colors")
        print("4 . Save maze")
        print("5. Quit")
        choice = None
        try:
            choice = int(input("Choice? (1-5):"))
        except Exception as e:
            print(e)
        if choice == 1:
            # maze.grid = MazeGenerator.generate_maze(config)
            generator.generate_maze(maze=maze, animate=True)
            maze.grid = generator.grid
            maze.pattern_42 = generator.blocked
            maze.solution_path = generator.solve_maze()
            maze.display(show_path=show_path, color_mode=color_mode)
        elif choice == 2:
            show_path = not show_path
            maze.display(show_path=show_path, color_mode=color_mode)
        elif choice == 3:
            color_mode = (color_mode + 1) % 3
            maze.display(show_path=show_path, color_mode=color_mode)
        elif choice == 4:
            try:
                maze.save_into_file()
                sys.stdout.write("\033[H\033[J")
                print("Maze saved seccufuly")
                sys.exit(0)
            except Exception as e:
                print(f"the maze did not save succusfuly, ERROR {e}")
        elif choice == 5:
            sys.exit(0)