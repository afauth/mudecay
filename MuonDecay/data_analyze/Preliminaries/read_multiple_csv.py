import os
import pandas as pd


#=====================================================================================================
def csv_files(path):

    files = os.listdir(path)

    for i in range( len(files) ):
        file = files[i]
        if 'csv' not in file:
            files.pop(i)

    return(files)


#=====================================================================================================
def concat_multiple_csv(path, csv_files):

    waveforms = pd.DataFrame()

    for i in range( len(csv_files) ):
        file = csv_files[i]
        df = pd.read_csv(f"{path}{file}", index_col=0)
        waveforms = pd.concat([waveforms, df], axis=1)

    waveforms.columns = [ ('event_'+str(i)) for i in range(waveforms.shape[1]) ]

    waveforms.to_csv(f"{path}{waveforms.shape[1]}_events.csv")
