import parsing
from maze_generator import MazeGenerator
import solve_maze


if __name__ == "__main__":
	config = parsing.parse_data("test.txt")

	if config and parsing.validate_config_data(config):
		maze = MazeGenerator(
			width = config["WIDTH"],
			height = config["HEIGHT"],
			entry = config["ENTRY"],
			exitt = config["EXIT"],
			is_perfect = config["PERFECT"],
			seed = config["SEED"]
		)

		maze.generate_maze()
		solved_maze = maze.solve_maze()

		print(solved_maze)
		solve_maze.export_maze(config, maze.grid, path_string="")