import time
import os
import sys
from typing import Any


def parsing(file_name: str) -> dict[str, str]:
    """
        Parses a configuration file into a dictionary.
        Handles syntax errors and missing files gracefully.
    """
    if not os.path.isfile(file_name):
        print(f"Error: The configuration file '{file_name}' was not found.")
        sys.exit(1)

    config: dict[str, str] = {}

    try:
        with open(file_name, "r") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    print(f"Error: Syntax error on line"
                          f"{line_num}: '{line}'. Missing '='.")
                    sys.exit(1)

                key, value = line.split("=", 1)
                key = key.strip().lower()
                value = value.strip()

                if not key or not value:
                    print(f"Error: Missing key or value"
                          f"on line {line_num}.")
                    sys.exit(1)

                config[key] = value

    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    return config


def config_checker(config: dict[str, Any]) -> None:
    """
        Validates configuration values.
        Ensures entry/exit are within bounds,
        different from each other,
        and maze dimensions are logical.
    """
    man_keys = ["entry", "exit", "perfect", "width", "height", "output_file"]

    for key in man_keys:
        if key not in config:
            print(f"Error: Missing mandatory key '{key}' in configuration.")
            sys.exit(1)

    try:
        width = int(config["width"])
        height = int(config["height"])
        if width <= 0 or height <= 0:
            print("Error: WIDTH and HEIGHT must be positive integers.")
            sys.exit(1)

        coords_data = {}
        for key in ["entry", "exit"]:
            raw_val = config[key]
            parts = [p.strip() for p in raw_val.split(",")]
            if len(parts) != 2:
                print(f"Error: {key.upper()} must be in 'x,y' format.")
                sys.exit(1)

            x, y = int(parts[0]), int(parts[1])

            if not (0 <= x < width and 0 <= y < height):
                print(f"Error: {key.upper()} ({x},{y})"
                      f"is outside the maze bounds.")
                sys.exit(1)

            coords_data[key] = (x, y)

        if coords_data["entry"] == coords_data["exit"]:
            print("Error: ENTRY and EXIT coordinates must be different.")
            sys.exit(1)

        if config["perfect"].lower() not in ["true", "false"]:
            print("Error: PERFECT must be 'True' or 'False'.")
            sys.exit(1)

        if width < 7 or height < 5:
            print("Warning: Maze size is too small to draw the '42' pattern.")

    except ValueError:
        print("Error: Configuration contains invalid numeric values.")
        sys.exit(1)


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
        try:
            self.config = config
            config_checker(config)
            self.solution_path = ""
            self.width = int(config.get("width", 10))
            self.height = int(config.get("height", 10))
            entry = config.get("entry", "0, 0")
            exitt = config.get("exit", f"{self.width - 1}, {self.height - 1}")
            self.entry = [int(x) for x in entry.split(",") if x is not None]
            self.exitt = [int(x) for x in exitt.split(",") if x is not None]
            self.grid = [
                [15 for _ in range(self.width)]
                for _ in range(self.height)]
            self.pattern_42: set = set()
        except ValueError as e:
            print(f"Error: value error {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: an unexpected error occured {e}")

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
        path_cells = []
        if show_path and self.solution_path:
            cx, cy = self.entry
            path_cells.append((cx, cy))
            for move in self.solution_path:
                if move == "N":
                    cy -= 1
                elif move == "S":
                    cy += 1
                elif move == "E":
                    cx += 1
                elif move == "W":
                    cx -= 1
                path_cells.append((cx, cy))
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
                # elif (x, y) in path_cells:
                #     canvas[cy][cx] = f"{PATH_COLOR}{BLOCK * 2}{RESET}"
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
        i = 0
        tmp = path_cells
        while i + 1 < len(list(tmp)):
            x1, y1 = tmp[i]
            x2, y2 = tmp[i + 1]
            cx = (x1 * 2) + 1
            cy = (y1 * 2) + 1
            g1 = int((((x1 * 2) + 1) + ((x2 * 2) + 1)) / 2)
            g2 = int((((y1 * 2) + 1) + ((y2 * 2) + 1)) / 2)
            canvas[cy][cx] = f"{PATH_COLOR}{BLOCK * 2}{RESET}"
            canvas[g2][g1] = f"{PATH_COLOR}{BLOCK * 2}{RESET}"
            print(canvas[cy][cx])
            print(canvas[g2][g1])
            print("\033[H\033[J", end="")
            for row in canvas:
                print("".join(row))
            print()
            time.sleep(0.1)
            i += 1

    def save_into_file(self) -> None:
        """
            funciton, exports the hex code (the solution of the maze)
            into a .txt file with other attributes

        """
        file_name = self.config.get("output_file", "maze.txt")
        try:
            with open(file_name, "w") as f:
                for row in self.grid:
                    f.write(
                        "".join(hex(cell)[2:].upper() for cell in row) + "\n")

                f.write("\n")

                f.write(f"{self.entry[0]} {self.entry[1]}\n")
                f.write(f"{self.exitt[0]} {self.exitt[1]}\n")

                f.write(f"{self.solution_path}\n")
        except Exception as e:
            print(f"Error saving file: {e}")


# if __name__ == "__main__":
#     from .cli import main

#     main()
