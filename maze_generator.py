import random
from collections import deque

class MazeGenerator:
    def __init__(self, width, height, entry, exitt, is_perfect, seed):
        self.width = width
        self.height = height
        self.entry = entry
        self.exitt = exitt
        self.is_perfect = is_perfect
        self.seed = seed

        self.grid = [[15 for _ in range(self.width)] for _ in range(self.height)]
        self.visited = set()


    def break_wall(self, x1, y1, x2, y2):
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

    
    def generate_42_seed(self):
        try:
            if self.width >= 18 and self.height >= 15:
                ox = (self.width - 7) // 2
                oy = (self.height - 5) // 2

                segments = [
                    # The "4"
                    (0,0, 0,1), (0,1, 0,2),
                    (0,2, 1,2), (1,2, 2,2),
                    (2,2, 2,3), (2,2, 2,4),
                    
                    # The "2"
                    (4,0, 5,0), (5,0, 6,0),
                    (6,0, 6,1), (6,1, 6,2),
                    (6,2, 5,2), (5,2, 4,2),
                    (4,2, 4,3), (4,3, 4,4),
                    (4,4, 5,4), (5,4, 6,4)
                ]

                for x1, y1, x2, y2 in segments:
                    rx1, ry1 = x1 + ox, y1 + oy
                    rx2, ry2 = x2 + ox, y2 + oy
                    
                    #break_wall(grid, rx1, ry1, rx2, ry2)
                    self.visited.add((rx1, ry1))
                    self.visited.add((rx2, ry2))
        except Exception as e:
            print(f"Error: An unexpected error occured {e}")

    
    def generate_maze(self):
        try:
            x, y = self.entry

            stack = [(x, y)]
            directions = [
                (0, -1, 1),
                (1, 0, 2),
                (0, 1, 4),
                (-1, 0, 8),
            ]
            self.visited.add((x, y))
            self.generate_42_seed()

            while stack:
                unvisited_cells = []
                current_x, current_y = stack[-1]
                for dir_x, dir_y, bit in directions:
                    nx_x, nx_y = current_x + dir_x, current_y + dir_y
                    if 0 <= nx_x < self.width and 0 <= nx_y < self.height and (nx_x, nx_y) not in self.visited:
                        unvisited_cells.append((nx_x, nx_y, bit))
                if unvisited_cells:
                    nx_x, nx_y, bit = random.choice(unvisited_cells)
                    self.break_wall(current_x, current_y, nx_x, nx_y)
                    self.visited.add((nx_x, nx_y))
                    stack.append((nx_x, nx_y))
                else:
                    stack.pop()

            if not self.is_perfect:
                for _ in range(10):
                    random_x = random.randrange(0, self.width)
                    random_y = random.randrange(0, self.height)
                    possible_walls = []

                    for dir_x, dir_y, bit in directions:
                        nx, ny = random_x + dir_x, random_y + dir_y
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if self.grid[random_y][random_x] & bit:
                                possible_walls.append((nx, ny, bit))
                    
                    if possible_walls:
                        target_x, target_y, bit = random.choice(possible_walls)
                        self.break_wall(random_x, random_y, target_x, target_y)
        except Exception as e:
            print(f"Error: an unexpected error occured {e}")

    @staticmethod
    def reconstruct_path(paths, start, end):
        current = end
        path_letter = []

        while current != start:
            (prev_x, prev_y), dir_char = paths[current]
            path_letter.append(dir_char)
            current = (prev_x, prev_y)

        return "".join(reversed(path_letter))

    def solve_maze(self):
        width = len(self.grid[0])
        height = len(self.grid)
        start = tuple(self.entry)
        end = tuple(self.exitt)

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
                return MazeGenerator.reconstruct_path(paths, start, end)
            
            for dir_x, dir_y, bit, char in directions:
                nx_x, nx_y = cur_x + dir_x, cur_y + dir_y
                if 0 <= nx_x < width and 0 <= nx_y < height:
                    if not (self.grid[cur_y][cur_x] & bit) and (nx_x, nx_y) not in paths:
                        paths[(nx_x, nx_y)] = ((cur_x, cur_y), char)
                        queue.append((nx_x, nx_y))

        return "path not found"