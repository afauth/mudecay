from acquisition.Configs import cfg_scope #import config file
from acquisition.SaveOutputs.Save_Output import myprint, outputs #import function "myprint" and variable "outputs"

import os
import pandas as pd
import numpy as np
import pyvisa
from time import time, sleep
from datetime import timedelta
from scipy.signal import find_peaks



# def Acquisition_Waveform( oscilloscope , necessarySamples , height=0 , min_peaks=2 , oscilloscope_resolution=2500 , numberBins=100, track_progress=False ):
#     '''
#     oscilloscope:
#     necessarySamples:
#     height:
#     min_peaks:
#     oscilloscope_resolution:
#     numberBins:
#     track_progress:
#     '''
#     sleep(3)

#     waveformList = pd.DataFrame()
#     timeList = []
#     counter = 1

#     while waveformList.shape[1] < necessarySamples:
        
#         total_events = waveformList.shape[1]
#         temp_df  = pd.DataFrame()
#         tempTime = [] 
#         sample   = min(100, 10*necessarySamples)
#         myprint(f'   Run {counter}. {100*round(total_events/necessarySamples , 1)}%. ({total_events}/{necessarySamples}).')

#         '''Acquisition of random samples'''
#         for i in range( sample ):
#             try:
#                 event = oscilloscope.query_ascii_values('curve?') #list
#             except:
#                 myprint('error')
#             else:
#                 temp_df[f'{i}'] = event
#                 time_instant = time()
#                 tempTime.append(time_instant)

#         '''Analysis of the sample: find waveform if len(peaks) >= min_peaks and save'''
#         for i in range( temp_df.shape[1] ):
#             event = temp_df[ temp_df.columns[i] ]
#             peaks, _ = find_peaks(-1*event, height=-1*height)
#             if len(peaks) >= min_peaks:
#                 waveformList[f'{counter}_{i}'] = event # counter_i will guarantee that the names on the df will not be replaced
#                 timeList.append( tempTime[i] )

#         '''If not finished yet, try again'''
#         counter += 1

#     '''Add correct label to the columns and add the time column'''
#     waveformList.columns = [ ('event_'+str(i)) for i in range(waveformList.shape[1]) ]
#     df = waveformList.T #This command is only to add the timeList as a line in an easy way. This undone later
#     df.insert( 0, 'time_epoch', np.array(timeList) )

#     return(df.T)



#=====================================================================================================
def read_waveforms_csv(files, file_name, path, tag=''):
    """
    This function reads all the step-DataFrames and concatenates them in a single one. 
    While this process occours, all the step-DataFrames are deleted, in the end, 
    the whole waveform-DataFrame is saved.

    Parameters
    ----------
    files: list
        The list that contains all the names(paths) of the step-DataFrames files.
    file_name: string
        It's the name of the file to be saved in the end, the one which contains all the waveforms. 
        It's not a path, but only a single string like '1134564322.34793'. The intention is to save the file_name
        as the time instant of the start of the acquisition.
    path: string
        Path to the folder where the csv files are stored.
    tag: string, Default ''
        A tag to put on the end of the file name. The default is the same as no tag.
    """

    myprint('\nReading and assembling the csv files.')

    waveforms = []

    for i in range( len(files) ):
        df = pd.read_csv(files[i])
        # os.remove(path=files[i]) # delete the partial files
        waveforms.append(df)

    Waveforms_df = pd.concat(waveforms, axis=1)
    Waveforms_df.columns = [ ('event_'+str(i)) for i in range(Waveforms_df.shape[1]) ]
    Waveforms_df.to_csv(f'{path}/{file_name}_{Waveforms_df.shape[1]}-events_{tag}.csv')

    return(Waveforms_df)



#=====================================================================================================
def run_acquisition( oscilloscope , samples=100 , height=0 , min_peaks=2 ):
    """
    This function serves to the purpose of retrieving a useful sample with given lenght. 
    Operation:
        - wait 2 seconds
        - define DataFrame and list to be filled after
        - while loop:
            -- retrieve a sample with lenght = min(100, 10*samples); neither too small nor too big
            -- analyze this sample with respect to the peaks
            -- store the useful events on the DataFrame and the times on the respective list
            -- repeat until get enought events
        - after filling all the requested samples, append the times to the DataFrame, change columns names, 
        details etc.
        - finish
        - returns the DataFrame containing the times and the waveforms (on the columns)

    Parameters
    ----------
    oscilloscope: instrument object
        Called by the pyvisa library.
    samples: int, default 100
        The number of samples to retrieve. 'samples' is the total amount of 'good samples', i.e.,
        the total amount of samples that pass on the min_peaks tests. Do not confuse with the rnd_sample.
    height: int, default 0
        The height value to find the peaks on the waveform. It's called by scipy, on the find_peaks function
    min_peaks: int, default 2
        'Quality test' for the waveform. If it contains at least the minimal peaks, it's a 'good sample'.
    """

    sleep(2)

    waveformList = pd.DataFrame()
    timeList = []
    counter = 1

    while waveformList.shape[1] < samples:
        
        total_events = waveformList.shape[1]
        temp_df  = pd.DataFrame()
        tempTime = [] 
        rnd_sample = min(100, 10*samples)
        myprint(f'   Run {counter}. {100*round(total_events/samples , 1)}%. ({total_events}/{samples}).')

        '''Acquisition of random samples'''
        for i in range( rnd_sample ):
            try:
                event = oscilloscope.query_ascii_values('curve?') #list
            except:
                myprint('error')
            else:
                temp_df[f'{i}'] = event
                time_instant = time()
                tempTime.append(time_instant)

        '''Analysis of the rnd_sample: find waveform if len(peaks) >= min_peaks and save'''
        for i in range( temp_df.shape[1] ):

            event = temp_df[ temp_df.columns[i] ]
            peaks, _ = find_peaks(-1*event, height=-1*height)

            if len(peaks) >= min_peaks:
                waveformList[f'{counter}_{i}'] = event # counter_i will guarantee that the names on the df will not be replaced
                timeList.append( tempTime[i] )

        '''If not finished yet, try again'''
        counter += 1

    '''Add correct label to the columns and add the time column'''
    waveformList.columns = [ ('event_'+str(i)) for i in range(waveformList.shape[1]) ]
    df = waveformList.T #This command is only to add the timeList as a line in an easy way. This undone later
    df.insert( 0, 'time_epoch', np.array(timeList) )

    return(df.T)
    


#=====================================================================================================
def Acquisition_Waveform( oscilloscope , necessarySamples , path , file_name , height=0 , min_peaks=2 ):
    """
    This function is built to run the "run_acquisition" function multiple times. Sometimes, a random error 
    may occour (like a problem on the communication between the oscilloscope, a sudden blackout etc.) 
    and this process is here to avoid losing all the data collected if the number of "necessarySamples" is 
    too big. It saves the "steps" DataFrames as csv files and then read all of them in the end.
    Finally, it saves the total-DataFrame and returns it.

    Parameters
    ----------
    oscilloscope: instrument object
        Called by the pyvisa library.
    necessarySamples: int
        .
    path: string
        Path to save the csv files.
    file_name: string
        .
    height: int, default 0
        .
    min_peaks: int, default 2
        .
    """

    acquired_samples = 0    # Total amount of samples collected
    saved_csv = 1           # Total of saved csv files 
    files = []              # File names

    while acquired_samples < necessarySamples:

        myprint(f'Try number {saved_csv}. {round(100*acquired_samples/necessarySamples,2)}% ({acquired_samples}/{necessarySamples}).')

        waveforms = run_acquisition(
                oscilloscope=oscilloscope,
                samples=min(100, necessarySamples),
                height=height,
                min_peaks=min_peaks
                )

        file = f'{path}/file_{saved_csv}.csv'
        waveforms.to_csv(file) # save the partial waveforms DataFrame
        files.append(file)     # add the name to the list

        acquired_samples += waveforms.shape[1]
        saved_csv += 1
    
    '''Assemble all the files in only one'''
    # waveforms = read_waveforms_csv(files=files, file_name=file_name, path=path, tag=f'{min_peaks}-events')

    # return(waveforms)
