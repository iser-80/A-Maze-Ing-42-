import time
import os
import sys
from typing import Any


def parsing(file_name: str) -> dict:
    """
        function, parse data from a given file to a return dictionary config

        Args:
            file_name: file: text file with random maze data

        Return:
            config -> dict: contained parsed data from the file_name
    """
    if not os.path.isfile(file_name):
        print(f"Error the config file {file_name} was not found")
        sys.exit(1)
    config = {}
    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    return config


class Maze:
    """
        class, helps the generated maze with it's display and export
    """
    N, E, S, W = 1, 2, 4, 8

    def __init__(self, config: dict[Any, Any]) -> None:
        """
            class initializer, takes config as the only assigned attibute

            Args:
                config -> dict: group the parsed data from the extern file
        """
        self.config = config
        self.solution_path = ""
        self.width = int(config.get("WIDTH", 10))
        self.height = int(config.get("HEIGHT", 10))
        entry = config.get("ENTRY", "0,0")
        exitt = config.get("EXIT", "5, 5")
        self.entry = [int(x) for x in entry.split(",")]
        self.exitt = [int(x) for x in exitt.split(",")]
        self.grid = [
            [15 for _ in range(self.width)]
            for _ in range(self.height)]
        self.pattern_42: set = set()
        print(f"Maze created {self.width}x{self.height}")

    def display(self, show_path: bool = False, color_mode: int = 0) -> None:
        """
            function, transform the grid into a colorized map (maze)

            Args:
                show_path -> bool: determine if the path showen
                color_mode -> int: define a specific color of the maze
        """
        colors = [
            "\033[31m",
            "\033[32m",
            "\033[33m",
            "\033[34m",
            "\033[35m",
            "\033[36m",
            "\033[37m",
        ]
        BLOCK = "▒"
        RESET = "\033[0m"
        PATTERN_COLOR = "\033[1;93m"
        PATH_COLOR = "\033[96m"

        if color_mode == 0:
            wall_color = "\033[37m"
        elif color_mode == 1:
            wall_color = "\033[31m"
        elif color_mode == 2:
            color = int(time.time() * 5) % len(colors)
            wall_color = colors[color]
        else:
            wall_color = "\033[34m"

        WALL = f"{wall_color}{BLOCK * 2}{RESET}"
        # SPACE = f"\033[30m{BLOCK}{RESET}"
        SPACE = "  "
        path_cells = set()
        if show_path and self.solution_path:
            cx, cy = self.entry
            path_cells.add((cx, cy))
            for move in self.solution_path:
                if move == "N":
                    cy -= 1
                elif move == "S":
                    cy += 1
                elif move == "E":
                    cx += 1
                elif move == "W":
                    cx -= 1
                path_cells.add((cx, cy))
        sys.stdout.write("\033[H\033[J")
        canvas_height = self.height * 2 + 1
        canvas_width = self.width * 2 + 1
        tx, ty = self.entry
        px, py, = self.exitt
        canvas = [
            [WALL for _ in range(canvas_width)]
            for _ in range(canvas_height)]
        # canvas[py][px] = "\033[42m  \033[0m"
        for y in range(self.height):
            for x in range(self.width):
                cy = y * 2 + 1
                cx = x * 2 + 1

                if hasattr(self, "pattern_42") and (x, y) in self.pattern_42:
                    canvas[cy][cx] = f"{PATTERN_COLOR}{BLOCK * 2}{RESET}"
                elif (x, y) in path_cells:
                    canvas[cy][cx] = f"{PATH_COLOR}{BLOCK * 2}{RESET}"
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
        canvas[ty * 2 + 1][tx * 2 + 1] = "\033[41m  \033[0m"
        canvas[py * 2 + 1][px * 2 + 1] = "\033[42m  \033[0m"
        for row in canvas:
            print("".join(row))
        sys.stdout.flush()

    def save_into_file(self) -> None:
        """
            funciton, exports the hex code (the solution of the maze)
            into a .txt file with other attributes

        """
        file_name = self.config.get("OUTPUT_FILE", "maze.txt")

        try:
            with open(file_name, "w") as f:
                for row in self.grid:
                    f.write(
                        "".join(hex(cell)[2:].upper() for cell in row) + "\n")
                f.write("\n")

                f.write(f"{self.entry[0]}" f" {self.entry[1]}\n")
                exitv = self.config.get(
                    "EXIT", f"{self.width - 1}" f" {self.height - 1}"
                )
                f.write(f"{exitv}\n")
                solution = getattr(self, "solution_path", "")
                f.write(f"{solution}\n")
        except Exception as e:
            print(f"Error saving file: {e}")


if __name__ == "__main__":
    from .cli import main

    main()
