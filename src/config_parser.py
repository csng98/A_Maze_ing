from typing import Dict, List


def parse_config(filename: str) -> Dict[str, str]:
    """
    Parses the configuration file and returns a dictionary with the settings.
    Handles errors using try/except blocks.
    """
    config: Dict[str, str] = {}
    
    try:
        config_file = open(filename, "r")
        line: str = config_file.readline()
        
        while line != "":
            clean_line: str = line.strip()
            
            # Ignoramos comentarios y lineas vacias
            if clean_line != "" and clean_line[0] != "#":
                parts: List[str] = clean_line.split("=")
                
                if len(parts) == 2:
                    key: str = parts[0].strip()
                    value: str = parts[1].strip()
                    config[key] = value
                    
            line = config_file.readline()
            
        config_file.close()
    except Exception:
        print("Error: Could not read or find the config file.")
        return {}
        
    try:
        # Comprobamos que el archivo tenga TODO lo necesario
        required = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE"]
        i: int = 0
        while i < len(required):
            if required[i] not in config:
                raise ValueError(f"Missing required key: {required[i]}")
            i += 1

        width: int = int(config["WIDTH"])
        height: int = int(config["HEIGHT"])

        if width < 0 or height < 0:
            raise ValueError ("Width and height must be non-negative integers")
        
        exits: List[str] = config["EXIT"].split(',')
        entries: List[str] = config["ENTRY"].split(',')

        exits: int = int(exits[0]), int(exits[1])
        entries: int = int(entries[0]), int(entries[1])

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
            
        return config

    except Exception as e:
        print(f"Error: Invalid configuration data. ({str(e)})")
        return {}
