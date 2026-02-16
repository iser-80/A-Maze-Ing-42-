def parse_data(file):
    config = {}
    try:
        with open(file, "r") as file_data:
            for line in file_data:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=")
                    key = key.strip()
                    value = value.strip()
                    if key in ["WIDTH", "HEIGHT"]:
                        config[key] = int(value)
                    elif key in ["ENTRY", "EXIT"]:
                        config[key] = [int(item) for item in value.split(",")]
                    elif key == "PERFECT":
                        config[key] = value.lower() == "true"
                    elif key == "SEED":
                        config[key] = int(value)
                    else:
                        config[key] = value
        return config
    except FileNotFoundError:
        print(f"Error: {file} dosen't exist")
        return None
    except ValueError as e:
        print(f"Error: Invalid data processing {e}")
        return None
    except Exception as e:
        print(f"Error: Unexpected error occured {e}")
        return None


def validate_config_data(config):
    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])
        entry_x, entry_y = config["ENTRY"]
        exit_x, exit_y = config["EXIT"]
        seed = config["SEED"]

        if width <= 0 or height <= 0:
            print("Error: Width and height must be positive")
            return False

        if not (0 <= entry_x < width and 0 <= entry_y < height):
            print("Error: Invalid entry position range")
            return False

        if not (0 <= exit_x < width and 0 <= exit_y < height):
            print("Error: Invalid exit position range")
            return False

        if (entry_x, entry_y) == (exit_x, exit_y):
            print("Error: Entry position must be different than the exit")
            return False

        if width < 5 or height < 3:
            print("Error: 42 pattern can't be omitted in less than 5x3")
            return False

        if seed != 42:
            print("Error: the seed should be 42")
            return False

        return True
    except (ValueError, KeyError) as e:
        print(f"Error: Invalid or missing data input: {e}")
        return False
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return False

#def validate_config_data(config):
#	try:
#		entry = config["ENTRY"]
#		exitt = config["EXIT"]
#		width = int(config["WIDTH"])
#		height = int(config["HEIGHT"])
#		perfect = config["PERFECT"]

#		if width <= 0 or height <= 0:
#			print("Error: Width and height must be positive")
#			return False
#		if not (0 < entry[0] <= width) and (0 < entry[1] <= height):
#			print("Error: Invalid entry postion range")
#			return False
#		if not (0 < exitt[0] <= width) and (0 < exitt[1] <= height):
#			print("Error: Invalid exit postion range")
#			return False
#		if (entry[0] == exitt[0]) and (entry[1] == exitt[1]):
#			print("Error: entry postion must be diffrent than the exit")
#			return False
#		if width < 5 or height < 3:
#        	print("Error: 42 pattern can't be omitted in less than 5x3")
#            return False

#		return True
#	except ValueError as e:
#		print(f"Error: Invalid data input {e}")
#	except Exception as e:
#		print(f"Error: An unexpected error occured {e}")
