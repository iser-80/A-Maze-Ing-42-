import random
from collections import deque
from typing import Any
import time


class MazeGenerator:
    """
        class, responsable about the creation and solving a maze
    """
    def __init__(
        self,
        width: int,
        height: int,
        entry: list[Any],
        exitt: list[Any],
        is_perfect: bool,
        seed: int | None,
    ) -> None:
        """
            class initiaizer

            Args:
                width -> int: width of the maze
                height -> int: height of the maze
                entry -> list: the coordinates of the start position
                exitt -> list: the coordinates of the exit position
                is_perfect -> bool: describle if the maze should has
                    a perfect solution
                seed -> int: acts as the dna of the maze
        """
        self.width: int = width
        self.height: int = height
        self.entry: list = entry
        self.blocked: set = set()
        if isinstance(exitt, str):
            self.exitt: list = [int(x) for x in exitt.split(",")]
        else:
            self.exitt = exitt
        self.is_perfect: bool = is_perfect
        self.seed = seed

        self.visited: set = set()
        self.grid: list[list] = [
            [15 for _ in range(self.width)] for _ in range(self.height)
        ]

    def break_wall(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
            class methode, break a wall of cell in the maze

            Args:
                x1, y1, x2, y2 -> int: coordinates
        """
        dx = x2 - x1
        dy = y2 - y1

        if dy == -1:
            self.grid[y1][x1] -= 1
            self.grid[y2][x2] -= 4
        elif dx == 1:
            self.grid[y1][x1] -= 2
            self.grid[y2][x2] -= 8
        elif dy == 1:
            self.grid[y1][x1] -= 4
            self.grid[y2][x2] -= 1
        elif dx == -1:
            self.grid[y1][x1] -= 8
            self.grid[y2][x2] -= 2

    def generate_42_seed(self) -> None:
        """
            class methode, create the 42 seed in the middle
                of the maze if valid
        """
        try:
            if self.width >= 18 and self.height >= 15:
                ox = (self.width - 7) // 2
                oy = (self.height - 5) // 2

                segments = [
                    # The "4"
                    (0, 0, 0, 1),
                    (0, 1, 0, 2),
                    (0, 2, 1, 2),
                    (1, 2, 2, 2),
                    (2, 2, 2, 3),
                    (2, 3, 2, 4),
                    # The "2"
                    (4, 0, 5, 0),
                    (5, 0, 6, 0),
                    (6, 0, 6, 1),
                    (6, 1, 6, 2),
                    (6, 2, 5, 2),
                    (5, 2, 4, 2),
                    (4, 2, 4, 3),
                    (4, 3, 4, 4),
                    (4, 4, 5, 4),
                    (5, 4, 6, 4),
                ]

                for x1, y1, x2, y2 in segments:
                    rx1, ry1 = x1 + ox, y1 + oy
                    rx2, ry2 = x2 + ox, y2 + oy

                    self.break_wall(rx1, ry1, rx2, ry2)
                    self.blocked.add((rx1, ry1))
                    self.blocked.add((rx2, ry2))
        except Exception as e:
            print(f"Error: An unexpected error occured {e}")

    def has_multiple_solutions(self) -> bool:
        """
            helper funciton, check if the maze has more than on solution path

            Return:
                bool
        """
        start = tuple(self.entry)
        end = tuple(self.exitt)

        directions = [
            (0, -1, 1),
            (1, 0, 2),
            (0, 1, 4),
            (-1, 0, 8),
        ]

        count = 0
        visited = set()

        def dfs(current: tuple) -> Any:
            """
                helper funtion, track back the solution path

                Args:
                    current -> tuple: the current position coordinates

                Return:
                    bool: if the path solutions is more than 2
            """
            nonlocal count
            if count >= 2:
                return
            if current == end:
                count += 1
                return

            x, y = current
            visited.add(current)

            for dx, dy, bit in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not (self.grid[y][x] & bit) and (nx, ny) not in visited:
                        dfs((nx, ny))

            visited.remove(current)

        dfs(start)
        return count >= 2

    def generate_maze(self, maze: Any | None, animate: bool = False) -> None:
        """
            class methode generate a random maze

            Args:
                maze -> instance(Maze): instance has the nessecerly
                    data for the maze generation
                animate -> bool: define if the animation should execute or not
        """
        self.visited = set()
        self.grid = [
            [15 for _ in range(self.width)]
            for _ in range(self.height)]
        x, y = self.entry

        stack = [(x, y)]
        directions = [(0, -1, 1), (1, 0, 2), (0, 1, 4), (-1, 0, 8)]

        self.visited.add((x, y))
        self.generate_42_seed()

        random.seed(self.seed) if self.seed is not None else random.seed()

        while stack:
            current_x, current_y = stack[-1]
            unvisited_cells = []
            for dir_x, dir_y, bit in directions:
                nx, ny = current_x + dir_x, current_y + dir_y
                if (0 <= nx < self.width and 0 <= ny < self.height and
                        (nx, ny) not in self.visited and
                        (nx, ny) not in self.blocked):
                    unvisited_cells.append((nx, ny, bit))

            if unvisited_cells:
                nx, ny, bit = random.choice(unvisited_cells)
                self.break_wall(current_x, current_y, nx, ny)
                self.visited.add((nx, ny))
                stack.append((nx, ny))
                if animate and maze:
                    maze.grid = self.grid
                    maze.display()
                    time.sleep(0.01)
            else:
                stack.pop()

        if not self.is_perfect:
            extra_walls_to_break = (self.width * self.height) // 10
            broken = 0
            while broken < extra_walls_to_break:
                rx = random.randrange(1, self.width - 1)
                ry = random.randrange(1, self.height - 1)
                dx, dy, bit = random.choice(directions)
                nx, ny = rx + dx, ry + dy

                if (rx, ry) in self.blocked or (nx, ny) in self.blocked:
                    continue

                if self.grid[ry][rx] & bit:
                    self.break_wall(rx, ry, nx, ny)
                    broken += 1
        # for x, y in self.blocked:
        #     self.grid[y][x] = 15

    @staticmethod
    def reconstruct_path(
        paths: dict[tuple[int, int], Any],
        start: tuple,
        end: tuple,
    ) -> str:
        """
            static method, reconstruct the solution path into a string

            Args:
                path -> dict[]: a list of coordinats
                    (define the path of the solution)
                start -> tuple: the start position
                end -> tuple: the exit position

            Return:
                (string) -> str: converted string of the path list solution
        """
        current = end
        path_letter = []

        while current != start:
            (prev_x, prev_y), dir_char = paths[current]
            path_letter.append(dir_char)
            current = (prev_x, prev_y)

        return "".join(reversed(path_letter))

    def solve_maze(self) -> str:
        """
            class methode, solve the maze with bfs algo

            Return:
                (path) -> list: list of coordinate positions that form
                    the solution path
        """
        width = len(self.grid[0])
        height = len(self.grid)
        start = tuple(self.entry)
        end = tuple(self.exitt)

        directions = [
            (0, -1, 1, "N"),
            (1, 0, 2, "E"),
            (0, 1, 4, "S"),
            (-1, 0, 8, "W"),
        ]
        queue = deque([start])
        paths: dict[tuple[
            int, int], tuple[tuple[int, int], str] | None] = {start: None}

        while queue:
            cur_x, cur_y = queue.popleft()
            if (cur_x, cur_y) == end:
                return MazeGenerator.reconstruct_path(paths, start, end)

            for dir_x, dir_y, bit, char in directions:
                nx_x, nx_y = cur_x + dir_x, cur_y + dir_y
                if 0 <= nx_x < width and 0 <= nx_y < height:
                    if (
                        not (self.grid[cur_y][cur_x] & bit)
                        and (nx_x, nx_y) not in paths
                        and (nx_x, nx_y) not in self.blocked
                    ):
                        paths[(nx_x, nx_y)] = ((cur_x, cur_y), char)
                        queue.append((nx_x, nx_y))
        return "path not found"
