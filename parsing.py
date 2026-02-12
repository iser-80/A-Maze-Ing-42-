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

def validate_config_data(config)
{
	try:
		width = config["WIDTH"]
	
	except ValueError as e:
		print(f"Error: Invalid data input {e}")
}


test = parse_data("test.txt")
print(test)