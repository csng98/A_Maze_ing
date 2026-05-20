import os
from typing import Dict, List

def parse_info(config: Dict[str, str]) -> Dict[str, str]:
    # Primero nos aseguramos de que el diccionario tenga las claves necesarias
    if "WIDTH" not in config or "HEIGHT" not in config or "EXIT" not in config:
        print("Error: Missing configuration data")
        return {} # Devolvemos un diccionario vacío para avisar del fallo

    width: int = int(config["WIDTH"])
    height: int = int(config["HEIGHT"])
    goal: str = config["EXIT"]
    
    exits: List[str] = goal.split(',')
    
    # Comprobamos que el split nos haya dado exactamente dos valores
    if len(exits) == 2:
        exit_c: int = int(exits[0])
        exit_r: int = int(exits[1])
        
        # Nuestro GPS: ¿Las coordenadas están dentro del mapa?
        if exit_c <= width and exit_r <= height:
            return config
        else:
            print("Error: Wrong size for the exit")
            return {}
    else:
        print("Error: Invalid EXIT format")
        return {}

def parse_config(filename: str) -> Dict[str, str]:
    # Diccionario donde guardaremos los datos limpios
    config: Dict[str, str] = {}
    
    # Al estilo clásico: comprobamos si el archivo existe antes de tocarlo
    # Así nos ahorramos usar bloques try/except
    if not os.path.exists(filename):
        print("Error: Config file not found.")
        return config
        
    config_file = open(filename, "r")
    line: str = config_file.readline()
    
    # Usamos while para leer línea por línea hasta el final
    while line != "":
        clean_line: str = line.strip()
        
        # Ignoramos líneas vacías o que empiezan por '#' (comentarios)
        if clean_line != "" and clean_line[0] != "#":
            parts: List[str] = clean_line.split("=")
            
            # Solo procesamos si hay una clave y un valor exactos
            if len(parts) == 2:
                key: str = parts[0].strip()
                value: str = parts[1].strip()
                config[key] = value
                
        # Avanzamos a la siguiente línea
        line = config_file.readline()
        
    config_file.close()
    
    # Pasamos el diccionario por nuestro filtro de seguridad
    validated_config: Dict[str, str] = parse_info(config)
    
    # Si todo fue bien, devolverá el config lleno. 
    # Si hubo un error en parse_info, devolverá {} e invalidará la partida.
    return validated_config
