def add(filename:str):
    with open("modules/logs/" + filename, "r") as file:
        current = file.read()
        if len(current) == 0:
            current:int = 0
            
    with open("modules/logs/" + filename, "w") as file:
        data = int(current) + 1
        file.write(str(data))

def write(filename:str, data:int):
    with open("modules/logs/" + filename, "a") as file:
        file.write(data)

def read(filename:str) -> str:
    with open("modules/logs/" + filename, "r") as file:
        return file.read()