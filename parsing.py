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
						config[key] = value
					elif key in ["ENTRY", "EXIT"]:
						config[key] = [int(item) for item in value.split(",")]
					elif key == "PERFECT":
						config[key] = value.lower() == "true"
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
		entry = config["ENTRY"]
		exitt = config["EXIT"]
		width = config["WIDTH"]
		height = config["HEIGHT"]
		perfect = config["PERFECT"]

		if width <= 0 or height <= 0:
			print("Error: Width and height must be positive")
			return False
		if not 0 < entry[0] <= width and 0 < entry[1] <= height:
			print("Error: Invalid entry postion range")
			return False
		if not 0 < exitt[0] <= width and 0 < exitt[1] <= height:
			print("Error: Invalid exit postion range")
			return False
		if entry[0] == exitt[0] and entry[1] == exitt[1]:
			print("Error: entry postion must be diffrent than the exit")
			return False
		if width < 5 or height < 3:
            print("Error: 42 pattern can't be omitted in less than 5x3")
            return False

		return True
	except ValueError as e:
		print(f"Error: Invalid data input {e}")
	except Exception as e:
		print(f"Error: An unexpected error occured {e}")
