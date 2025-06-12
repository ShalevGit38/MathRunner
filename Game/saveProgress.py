
def load(var):
    with open("gameSave.txt", 'r') as file:
        for line in file.readlines():
            lineVar = line.split("=")[0].replace(" ", "")
            lineValue = line.split("=")[-1].replace("\n", "")
            if lineVar == var:
                return lineValue

def save(var, value):
    with open("gameSave.txt", 'r') as file:
        lines = file.readlines()
        
    for line in lines:
        if line.split("=")[0].replace(" ", "") == var:
            lines[lines.index(line)] = f"{var}={value}\n"
    
    with open("gameSave.txt", 'w') as file:
        file.writelines(lines)


    