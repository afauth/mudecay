import os
import pandas as pd



def list_files(path="."):
    
    list_files = []

    for _, _, files in os.walk(path):
        for filename in files:
            list_files.append(filename)

    return(list_files)



def Find_Waveforms_Files(files, substring):

    waveforms_files = [string for string in files if substring in string]

    return(waveforms_files)



def Read_Waveforms_Files(waveforms_files, path):

    waveforms = pd.DataFrame()

    for i in range( len(waveforms_files) ):
        df = pd.read_csv(path)





# print(list_files())