from Configs import cfg_scope
from Save_Outputs.Save_Output import myprint, outputs
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




def Set_Scope_Parameters(oscilloscope):
    '''
    Note: I don't now exactly why, but sometimes an error will occour in this part of the code. It's a runtime error. I THINK it's something to
    do with a problem on the communication between computer and oscilloscope.
    '''
    try_set = True
    counter = 0
    sleep(3)

    while try_set == True:
        sleep(1)
        
        try:
            
            #oscilloscope.write('ACQuire:STATE RUN')
            #print('\nState: RUN')
            
            oscilloscope.write(f'SELECT:{cfg_scope.channel} ON')
            #print(f'\n{cfg_scope.channel} ON')
            
            oscilloscope.write(f'DATa:SOUrce {cfg_scope.channel}') 
            #print(f'')
            
            oscilloscope.write(f'DATa:ENCdg {cfg_scope.encode_format}') 
            #print(f'Encode Format: {cfg_scope.encode_format}')
            
            oscilloscope.write(f'DATa:WIDth {cfg_scope.width}') 
            #print(f'Data Width: {cfg_scope.width}')
            
            oscilloscope.write(f'{cfg_scope.channel}:SCAle {cfg_scope.channel_scale}')
            #print(f'{cfg_scope.channel} scale: {cfg_scope.channel_scale}')
            
            oscilloscope.write(f'{cfg_scope.channel}:POSition {cfg_scope.channel_position}')
            #print(f'{cfg_scope.channel} position: {cfg_scope.channel_position}')
            
            oscilloscope.write(f'{cfg_scope.channel}:PRObe {cfg_scope.channel_probe}')
            #print(f'{cfg_scope.channel} probe: {cfg_scope.channel_probe}')
            
            oscilloscope.write(f'TRIGger:MAIn:LEVel {cfg_scope.trigger}')
            #print(f'Trigger: {cfg_scope.trigger}')
            
            oscilloscope.write(f'HORizontal:MAIn:SCAle {cfg_scope.horizontal_scale}')
            #print(f'Horizontal scale: {cfg_scope.horizontal_scale}')
            
            oscilloscope.write(f'HORizontal:MAIn:POSition {cfg_scope.horizontal_position_1};') 
            #print(f'Horizontal Position: {cfg_scope.horizontal_position_1}')
            
            oscilloscope.write(f'HORizontal:MAIn:POSition {cfg_scope.horizontal_position_2};') 
            #print(f'Horizontal Position: {cfg_scope.horizontal_position_2}')
            
            oscilloscope.write(f'DISplay:PERSistence {cfg_scope.persistence}') 
            #print(f'Persistence: {cfg_scope.persistence}')
            
            oscilloscope.write(f'TRIGGER:MAIN:EDGE:SLOPE {cfg_scope.slope}') 
            #print(f'Slope: {cfg_scope.slope}')
            
            try_set = False

            myprint(f'\n\nOscilloscope informations: LOADED SUCESSFULLY after {counter} attempt(s). Check config file for more details.\n')
            myprint( f'\nSCOPE INFOs:\n{oscilloscope.query("WFMPre?")}\n' ) #Command to transfer waveform preamble information.

            
        except:
            
            counter += 1
            myprint('FAILED TO WRITE scope parameters.')

            if counter >= 3:
                myprint('FAILED TO WRITE scope parameters, even after three attempts.\nPlease, check connection with the oscilloscope and try again.')
                raise