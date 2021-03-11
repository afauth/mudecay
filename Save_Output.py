import subprocess

def SaveOutput(file='test_file'): #python file on same directory
    with open("output.txt", "w+") as output:
        subprocess.call(["python", f"./{file}.py"], stdout=output)

def ReadOutput(file='output.txt'):
    with open(file, "r") as f:
        contend = f.read()
    return(contend)