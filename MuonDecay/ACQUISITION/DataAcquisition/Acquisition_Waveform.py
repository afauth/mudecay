from ACQUISITION.Configs import cfg_scope #import config file
from ACQUISITION.SaveOutputs.Save_Output import myprint, outputs #import function "myprint" and variable "outputs"
import pandas as pd
import numpy as np
import pyvisa
from time import time, sleep
from datetime import timedelta
from scipy.signal import find_peaks



def Acquisition_Waveform( oscilloscope , necessarySamples , height=0 , min_peaks=2 , oscilloscope_resolution=2500 , numberBins=100, track_progress=False ):
    sleep(3)

    waveformList = pd.DataFrame()
    timeList = []
    counter = 1

    while waveformList.shape[1] < necessarySamples:
        
        #start = time()

        '''Acquisition of random samples'''
        myprint(f'Try number {counter}')
        temp_df  = pd.DataFrame()
        tempTime = [] 
        sample   = min(1000, 10*necessarySamples)
        for i in range( sample ):
            try:
                event           = oscilloscope.query_ascii_values('curve?') #list
                temp_df[f'{i}'] = event
                time_instant = time()
                tempTime.append(time_instant)
            except:
                myprint('error')

        '''Analysis of the sample: find waveform if len(peaks) >= min_peaks and save'''
        for i in range( temp_df.shape[1] ):
            event = temp_df[ temp_df.columns[i] ]
            peaks, _ = find_peaks(-1*event, height=-1*height)
            if len(peaks) >= min_peaks:
                waveformList[f'{i}'] = event
                timeList.append( tempTime[i] )
        
        #finish = time()
        #print(f'Elapsed time: {timedelta(seconds=finish-start)}')

        '''If not finished yet, try again'''
        counter += 1

    # Add correct label to the columns and add the time column
    waveformList.columns = [ ('event_'+str(i)) for i in range(waveformList.shape[1]) ]
    df = waveformList.T #This command is only to add the timeList as a line in an easy way. This undone later
    df.insert( 0, 'time_epoch', np.array(timeList) )

    return(df.T)