from typing import Dict, List


def parse_config(filename: str) -> Dict[str, str]:
    """
    Parses the configuration file and returns a dictionary with the settings.
    Handles errors using try/except blocks.
    """
    config: Dict[str, str] = {}

    try:
        with open(filename, "r") as config_file:
            line: str = config_file.readline()

            while line != "":
                clean_line: str = line.rstrip("\r\n")

                if clean_line != "" and clean_line[0] != "#":
                    parts: List[str] = clean_line.split("=")

                    if len(parts) == 2:
                        key: str = parts[0]
                        value: str = parts[1]

                        if " " in key or " " in value:
                            raise ValueError(f"Spaces are not allowed in "
                                             f"configuration lines: "
                                             f"{clean_line}")

                        config[key] = value
                    else:
                        raise ValueError(
                            f"Invalid config format in line: {clean_line}")
                line = config_file.readline()
    except ValueError as e:
        print(f"Config Error: {e}")
        return {}
    except Exception:
        print("Error: Could not read or find the config file.")
        return {}

    try:
        required = ["WIDTH", "HEIGHT", "ENTRY",
                    "EXIT", "OUTPUT_FILE"]
        i: int = 0
        while i < len(required):
            if required[i] not in config:
                raise ValueError(f"Missing required key: {required[i]}")
            i += 1

        width: int = int(config["WIDTH"])
        height: int = int(config["HEIGHT"])

        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be non-negative integers")
        if width > 30 or height > 30:
            raise ValueError("Width and height must be less than 30 cells")

        for key_name in ["ENTRY", "EXIT"]:
            val = config[key_name]
            if val.count(',') != 1 or not val.replace(',', '').isdigit():
                raise ValueError(f"{key_name} must be strictly"
                                 f" in 'number,number'"
                                 f" format with no spaces or extra characters")

        exits: tuple[int, int] = (
            int(config["EXIT"].split(',')[0]),
            int(config["EXIT"].split(',')[1]))
        entries: tuple[int, int] = (
            int(config["ENTRY"].split(',')[0]),
            int(config["ENTRY"].split(',')[1]))

        if exits[0] == entries[0] and exits[1] == entries[1]:
            raise ValueError("Entry and exit cannot be the same cell")
        if entries[0] < 0 or entries[1] < 0:
            raise ValueError("Entry coordinates must be non-negative integers")
        if exits[0] < 0 or exits[1] < 0:
            raise ValueError("Exit coordinates must be non-negative integers")
        if len(exits) != 2 or len(entries) != 2:
            raise ValueError("Invalid ENTRY or EXIT format")
        if exits[0] >= width or exits[1] >= height:
            raise ValueError("Exit coordinates are out of bounds")
        if entries[0] >= width or entries[1] >= height:
            raise ValueError("Entry coordinates are out of bounds")

        # is_perfect: str = config["PERFECT"]

        # if is_perfect != "True" and is_perfect != "False":
        #     raise ValueError("PERFECT key must be  a boolean")

        if "SEED" in config:
            if not config["SEED"].isdigit():
                del config["SEED"]
                raise ValueError("Warning: SEED is not a valid number.")

        return config

    except Exception as e:
        print(f"Error: Invalid configuration data. ({str(e)})")
        return {}
