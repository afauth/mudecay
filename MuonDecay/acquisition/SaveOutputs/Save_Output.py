#from time import sleep
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



def Acquisition_Type(min_peaks):
    if min_peaks == 1:
        acquisition = 'single_muon'
    elif min_peaks == 2: 
        acquisition = 'muon_decay'
    else:
        acquisition = 'other'
    return(acquisition)



outputs = []
def myprint(message):
    global outputs
    print(message)
    outputs.append(message)
