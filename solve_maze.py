from collections import deque

def export_maze(config, grid, path_string=""):
    output_file = config.get("OUTPUT_FILE", "maze.txt")
    
    with open(output_file, "w") as f:
        # Phase 1: The Hex Grid
        for row in grid:
            hex_row = "".join([format(cell, 'x').upper() for cell in row])
            f.write(hex_row + "\n")
        
        f.write("\n")
        entry = config["ENTRY"]
        exit_ = config["EXIT"]
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_[0]},{exit_[1]}\n")
        
        f.write(path_string + "\n")
        print(f"Successfully exported maze to {output_file}")
