import pandas as pd
import os



#=====================================================================================================
def concat_csv(path='../documents/data/1619297657.0683234/', tag='file_', sep='/'):

    files = os.listdir(path)

    csv_files = []
    for file in files:
        if (tag in file) and ('csv' in file):
            csv_files.append(file)

    if len(csv_files) <= 0:
        raise ValueError('The folder as not any partial csv files to assemble. Please, check the path or the tag of the file.') 

    waveforms = pd.DataFrame()

    for i in range( len(csv_files) ):

        file = csv_files[i]
        df = pd.read_csv(path+sep+file, index_col=0)
        waveforms = pd.concat([waveforms, df], axis=1)
        waveforms.columns = ['event_'+str(i) for i in range(waveforms.shape[1])]

    return(waveforms)


# #=====================================================================================================
# def csv_files(path):

#     files = os.listdir(path)

#     for i in range( len(files) ):
#         file = files[i]
#         if 'csv' not in file:
#             files.pop(i)

#     return(files)


# #=====================================================================================================
# def concat_multiple_csv(path, csv_files):

#     waveforms = pd.DataFrame()

#     for i in range( len(csv_files) ):
#         file = csv_files[i]
#         df = pd.read_csv(f"{path}{file}", index_col=0)
#         waveforms = pd.concat([waveforms, df], axis=1)

#     waveforms.columns = [ ('event_'+str(i)) for i in range(waveforms.shape[1]) ]

#     return(waveforms)
