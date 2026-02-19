*This project has been created as partof the 42 curriculum by maiss and ierrafiy*

# Description

a-maze-ing is a terminal based maze generation written in python
the program generates random mazes with the option of generating maze bease on seed that can be reproduciable
it support colored and animated generation, path solving from entry to exit, and saving the maze into a file 

# Instructions
clone the repo and install the package locally
`bash`
`pip install .`
`a-maze-ing config.txt`

# Algorithem Used
Depth-First Search (DFS) — Maze generation
Breadth-First Search (BFS) — Path solving

- The configuration file allows you to define:

    - Maze dimensions (WIDTH, HEIGHT)

    - Entry and exit coordinates

    - Seed value (optional)

    - Perfect / imperfect maze generation

    - Display options (colors, animation, path visibility)

# Resources
https://www.geeksforgeeks.org/python/print-colors-python-terminal/
https://ansi.tools/?s=%255C033%255B92m
https://www.geeksforgeeks.org/python/python-program-for-depth-first-search-or-dfs-for-a-graph/
https://en.wikipedia.org/wiki/Breadth-first_search
https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/

