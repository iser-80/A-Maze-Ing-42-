def read_map(filename):
    config = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    if key in ["WIDTH", "HEIGHT"]:
                        config[key] = int(value)
                    elif key == "PERFECT":
                        config[key] = value.lower() == "true"
                    elif key in ["ENTRY", "EXIT"]:
                        config[key] = [int(i) for i in value.split(",")]
                    else:
                        config[key] = value
        return config
    
    except FileNotFoundError:
        print("Error: map file not found")
        return None
    except ValueError as e:
        print(f"Error: Invalid data in config.txt ({e})")
        return None


def validate_config(config):
    try:
        entry_x, entry_y = config["ENTRY"]
        exit_x, exit_y = config["EXIT"]
        width = config["WIDTH"]
        height = config["HEIGHT"]

        if width <= 0 or height <= 0:
            print("Error: width and height must be positive")
            return False
        
        if not (0 <= entry_x < width and 0 <= entry_y < height):
            print("Error: invalid entry, must be in range of width in height")
            return False
    
        if not (0 <= exit_x <= width and 0 <= exit_y <= height):
            print("Error: invalid exit, must be in range of width in height")
            return False
    
        if entry_x == exit_x and entry_y == exit_y:
            print("Error: entry and exit must be diffrent")
            return False
        
        if width < 5 or height < 3:
            print("Error: 42 pattern can't be omitted in less than 5x3")
            return False

        return True
    except Exception as e:
        print(f"An unexpected error occured: {e}")
        return None


# TESTING
test = read_map("test.txt")
if validate_config(test):
    print(test)
    
