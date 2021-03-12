from time import sleep
import os
import subprocess



def SaveOutput(file='test_file'): #python file on same directory
    with open("output.txt", "w+") as output:
        subprocess.call(["python", f"./{file}.py"], stdout=output)



def ReadOutput(file='output.txt'):
    with open(file, "r") as f:
        contend = f.read()
    return(contend)



def Create_Folder(name):
    os.mkdir(path=name)



outputs = []
def myprint(message):
    global outputs
    print(message)
    outputs.append(message)
#myprint('banana')
#open("output.txt", "w").write("\n".join(outputs))