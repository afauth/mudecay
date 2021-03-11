import configs.cfg_scope as config
from send_email import Send_Email
import os
import re
import pyvisa
import numpy as np
import pandas as pd
from time import time, ctime, sleep
from datetime import timedelta
from scipy.signal import find_peaks


"""
"""

#                           Funções a serem utilizadas
#==========================================================================================================
'''
    For Y format, the time (absolute coordinate) of a point, relative to the trigger, can
    be calculated using the following formula. N ranges from 0 to 2499.
        Xn = XZEro + XINcr (n - PT_OFf)
    For Y format, the magnitude (usually voltage, relative to ground) (absolute
    coordinate) of a point can be calculated:
        Yn = YZEro + YMUIty (yn - YOFf)
'''
def substr_to_number(string): #ex.: 
    return(   float(  re.split(' |\n', string)[0]  )   )

def x_to_volts(x_zero , x_incr , n_ranges , pt_off):
    return( x_zero + x_incr*(n_ranges - pt_off) )

def y_to_volts(y_zero , y_mult , y_n , y_off):
    return(  y_zero + y_mult*(y_n - y_off)  )

def y_to_units(y_zero , y_mult , y_volt , y_off):
    return(  (y_volt - y_zero)/y_mult + y_off  )

def height_in_volts(df_conversion, height_in_units):
    y_zero = df_conversion['value']['Y_zero']
    y_mult = df_conversion['value']['Y_mult']
    y_off  = df_conversion['value']['Y_off' ]
    return(  y_to_volts(y_zero=y_zero, y_mult=y_mult, y_n=height_in_units, y_off=y_off)  )

def height_in_units(df_conversion, height_in_volts):
    y_zero = df_conversion['value']['Y_zero']
    y_mult = df_conversion['value']['Y_mult']
    y_off  = df_conversion['value']['Y_off' ]
    return(  y_to_units(y_zero=y_zero, y_mult=y_mult, y_volt=height_in_volts, y_off=y_off)  )

def Acquisition_Waveform( oscilloscope , necessarySamples , height=0 , min_peaks=2 , oscilloscope_resolution=2500 , numberBins=100, track_progress=False ):
    sleep(3)

    waveformList = pd.DataFrame()
    counter = 1
    
    while waveformList.shape[1] < necessarySamples:

        tempList = []
        print(f'Try number {counter}')

        try:
            tempList = oscilloscope.query_ascii_values('curve?')
        except:
            print('error')


        event = pd.Series(tempList)
        peaks, _ = find_peaks(-event, height=-height)

        if len(peaks) >= min_peaks:
            waveformList[f'{counter-1}'] = event

        counter += 1

    return(waveformList)

def Scope_Set_Parameters(oscilloscope):
    '''
    Note: I don't now exactly why, but sometimes an error will occour in this part of the code. It's a runtime error. I THINK it's something to
    do with a problem on the communication between computer and oscilloscope.
    '''
    try:
        
        #oscilloscope.write('ACQuire:STATE RUN')
        #print('\nState: RUN')
        
        oscilloscope.write(f'SELECT:{config.channel} ON')
        #print(f'\n{config.channel} ON')
        
        oscilloscope.write(f'DATa:SOUrce {config.channel}') 
        #print(f'')
        
        oscilloscope.write(f'DATa:ENCdg {config.encode_format}') 
        #print(f'Encode Format: {config.encode_format}')
        
        oscilloscope.write(f'DATa:WIDth {config.width}') 
        #print(f'Data Width: {config.width}')
        
        oscilloscope.write(f'{config.channel}:SCAle {config.channel_scale}')
        #print(f'{config.channel} scale: {config.channel_scale}')
        
        oscilloscope.write(f'{config.channel}:POSition {config.channel_position}')
        #print(f'{config.channel} position: {config.channel_position}')
        
        oscilloscope.write(f'{config.channel}:PRObe {config.channel_probe}')
        #print(f'{config.channel} probe: {config.channel_probe}')
        
        oscilloscope.write(f'TRIGger:MAIn:LEVel {config.trigger}')
        #print(f'Trigger: {config.trigger}')
        
        oscilloscope.write(f'HORizontal:MAIn:SCAle {config.horizontal_scale}')
        #print(f'Horizontal scale: {config.horizontal_scale}')
        
        oscilloscope.write(f'HORizontal:MAIn:POSition {config.horizontal_position_1};') 
        #print(f'Horizontal Position: {config.horizontal_position_1}')
        
        oscilloscope.write(f'HORizontal:MAIn:POSition {config.horizontal_position_2};') 
        #print(f'Horizontal Position: {config.horizontal_position_2}')
        
        oscilloscope.write(f'DISplay:PERSistence {config.persistence}') 
        #print(f'Persistence: {config.persistence}')
        
        oscilloscope.write(f'TRIGGER:MAIN:EDGE:SLOPE {config.slope}') 
        #print(f'Slope: {config.slope}')
        
        print(f'Oscilloscope informations: LOADED SUCESSFULLY. Check config file for more details.\n')
        #print( f'\nSCOPE INFOs:\n{oscilloscope.query("WFMPre?")}\n' ) #Command to transfer waveform preamble information.
    except:
        print('FAILED TO WRITE scope parameters.\nPlease, check connection with the oscilloscope and try again.')
        raise

# def Find_Conversion_Parameters(oscilloscope):
#     _ = [ 
#         substr_to_number( oscilloscope.query('WFMPre:XZEro?')  ),
#         substr_to_number( oscilloscope.query('WFMPre:XINcr?')  ),
#         substr_to_number( oscilloscope.query('WFMPre:PT_OFf?') ),
#         substr_to_number( oscilloscope.query('WFMPre:YZEro?')  ),
#         substr_to_number( oscilloscope.query('WFMPre:YMUlt?')  ),
#         substr_to_number( oscilloscope.query('WFMPre:YOFf?')   )
#         ]
#     df = pd.DataFrame( data=_ , index=['X_zero' , 'X_incr' , 'Pt_off' , 'Y_zero' , 'Y_mult' , 'Y_off'] , columns=['value'] )
#     return(df)

def Save_Waveform_csv(waveform, folder_name, tagger=''):

    #print( '\nSaving Data Frame and conversion parameters to .csv files...\n' )

    path_folder = f'data/{folder_name}'
    os.mkdir(path_folder)

    #file_name = f'data/{time_finish}_{config.necessarySamples}-samples_{config.min_peaks}-peaks_waveforms.csv'
    file_name = f'{path_folder}/{waveform.shape[1]}-samples_{config.min_peaks}-peaks_waveforms_{tagger}.csv'

    waveform.to_csv( path_or_buf=file_name, header=True, index=True ) 
    


#                           Call oscilloscope and set the parameters
#==========================================================================================================
rm = pyvisa.ResourceManager()                 # Calling PyVisa library
scope = rm.open_resource(str(config.ScopeID)) # Connecting via USB
Scope_Set_Parameters(oscilloscope=scope)


#                           Start time
#========================================================================================================== 
time_start = time()
print( f'\nStarting acquisition... Local time: {ctime(time_start)} \n'  ) # Print da hora local marcada no computador


#                           Print preamble of informations
#==========================================================================================================
print(f'\nNumber of requested samples: {config.necessarySamples}')
print(f'Minimal number of peaks: {config.min_peaks}')
print(f'Progress tracker is {"ON" if config.track_progress == True else "OFF"}')
if config.email_me == True:
    print(f'An email will be sent when acquisition is over or in case of error.\n')
else:
    print('No email.\n')


#                           RUN ACQUISITION
#==========================================================================================================
try:
    #df_conversion = Find_Conversion_Parameters(oscilloscope=scope)
    #height = height_in_units(df_conversion=df_conversion, height_in_volts=config.trigger)
    #print(height)
    waveform = Acquisition_Waveform(
                oscilloscope=scope,
                necessarySamples=config.necessarySamples,
                height=0,
                min_peaks=config.min_peaks, 
                oscilloscope_resolution=config.scopeResolution,
                numberBins=config.numberBins,
                track_progress=config.track_progress
                            )

    time_finish = time() # Get finish time
    print( f'\nFinishing acquisition... Local time: {ctime(time_finish)}\nAfter {str(timedelta(seconds=time_finish - time_start))}'  ) # Print da hora local marcada no computador

    Save_Waveform_csv(waveform=waveform, folder_name=time_start, tagger='')
    #df_conversion.to_csv( path_or_buf=f'data/{time_start}/conversion-values.csv', header=True, index=True )

    if config.email_me == True:
        subject = f'[MuDecay] Acquisition Finished succesfully'
        msg = f'Acquisition finished! Check the .csv file.\nNumber of samples: {config.necessarySamples}.\nNumber min of peaks: {config.min_peaks} \n\nLocal time: {ctime(time())}\nAfter {str(timedelta(seconds=time_finish - time_start))}'
        Send_Email(subject=subject, msg=msg)

except:
    if config.email_me == True:
        subject = f'[MuDecay] Error on acquisition'
        msg = f'An unexpected error occoured.\n\nPlease, re-check the acquisition and try again.\nLocal time: {ctime(time())}\nAfter {str(timedelta(seconds=time_finish - time_start))}'
        Send_Email(subject=subject, msg=msg)
    print('\nUnexpected error. Please, re-check parameters and oscilloscope connection and try again.\n')
    raise

#                          END
#==========================================================================================================
print('\nEND\n\n')