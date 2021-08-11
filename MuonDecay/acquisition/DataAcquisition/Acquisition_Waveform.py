from configs import cfg_scope #import config file
from acquisition.SaveOutputs.Save_Output import myprint, outputs #import function "myprint" and variable "outputs"
from acquisition.DataAcquisition.Conversion_Values import convert_y_to_mV, units_conversion_parameters
from acquisition.DataAcquisition.Set_Scope_Parameters import check_parameters

import pandas as pd
import numpy as np
from time import time, sleep
from datetime import timedelta
from scipy.signal import find_peaks, waveforms



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
def trigger_slope_value(config='FALL'):

    cfg_uppercase = config.upper()

    if cfg_uppercase == 'FALL':
        slope = -1
    elif cfg_uppercase == 'RISE':
        slope = 1
    else:
        raise ('Trigger Slope Error: could not determine the slope of the config file. It must be \"FALL\" or \"RISE\"')

    return(slope)



#=====================================================================================================
def get_rnd_sample(oscilloscope, rnd_sample, converter):

    # '''Retrieve the conversion parameters from the oscilloscope'''
    # converter = units_conversion_parameters(oscilloscope=oscilloscope)

    '''Create objects to fill'''
    df_data   = pd.DataFrame() 
    time_data = []
    errors    = 0 

    '''Acquisition of random samples'''
    for i in range( rnd_sample ):
        try:
            event = oscilloscope.query_ascii_values('curve?') #list
        except:
            errors += 1
        else:
            df_data[f'{i}'] = event
            time_instant = time()
            time_data.append(time_instant)

    df_data = convert_y_to_mV(df_data, converter) #convert all DataFrame to mV

    myprint(f'          Events: {rnd_sample - errors}; Errors {errors}')

    return(df_data, time_data)



#=====================================================================================================
def analyze_rnd_sample(df_data, time_data, trigger, trigger_slope=-1, counter=1, min_peaks=2, min_separation=10):

    # trigger_slope = trigger_slope_value(trigger_slope)

    waveforms_analyzed = pd.DataFrame()
    time_analyzed = []
    discarded = 0

    '''Analysis of the rnd_sample: find waveform if len(peaks) >= min_peaks and save'''
    for i in range( df_data.shape[1] ):

        event = df_data[ df_data.columns[i] ]
        peaks, _ = find_peaks(trigger_slope*event, height=trigger_slope*trigger)

        if (min_peaks > 2) and (len(peaks) >= min_peaks):
            waveforms_analyzed[f'{counter}_{i}'] = event 
            time_analyzed.append( time_data[i] )

        # Muon decay
        elif (min_peaks == 2) and (len(peaks) == min_peaks) and (peaks[1] - peaks[0] >= min_separation):
            waveforms_analyzed[f'{counter}_{i}'] = event # counter_i will guarantee that the names on the df will not be replaced
            time_analyzed.append( time_data[i] )

        # Single Muon
        elif (min_peaks == 1) and (len(peaks) == min_peaks): # there's no separation when there's only 1 or none peaks
            waveforms_analyzed[f'{counter}_{i}'] = event # counter_i will guarantee that the names on the df will not be replaced
            time_analyzed.append( time_data[i] )
        
        elif (min_peaks == 0) and (len(peaks) >= min_peaks): 
            waveforms_analyzed[f'{counter}_{i}'] = event 
            time_analyzed.append( time_data[i] )
        
        else:
            discarded += 1
    
    myprint(f'          Collected {df_data.shape[1] - discarded} events; {discarded} removed')

    return(waveforms_analyzed, time_analyzed)



#=====================================================================================================
def run_acquisition( oscilloscope, converter, trigger, trigger_slope=-1, samples=100, rnd_sample=1000, min_peaks=2, min_separation=10 ):
    """
    This function serves to the purpose of retrieving a useful sample with given lenght. 
    Operation:
        - wait
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
    rnd_samples: int, default 1000
        The number of samples with random goodness, i.e., the samples may be good, but may be not. 
        After collecting, they will be analyzed and stored, if they are good, as specified.
    height: int
        The height value to find the peaks on the waveform. It's called by scipy, on the find_peaks function
    min_peaks: int, default 2
        'Quality test' for the waveform. If it contains at least the minimal peaks, it's a 'good sample'.
    """

    sleep(1)

    waveforms_storage = pd.DataFrame()
    time_storage = []
    counter = 1

    while waveforms_storage.shape[1] < samples:
        
        total_events = waveforms_storage.shape[1]
        temp_df   = pd.DataFrame()
        temp_time = [] 
        myprint(f'      Run {counter}. {round(100*total_events/samples , 1)}%. ({total_events}/{samples}).')

        temp_df, temp_time = get_rnd_sample(
            oscilloscope=oscilloscope, 
            rnd_sample=rnd_sample,
            converter=converter
            )

        waveforms_analyzed, time_analyzed = analyze_rnd_sample(
            df_data=temp_df, 
            time_data=temp_time, 
            counter=counter, 
            min_peaks=min_peaks, 
            min_separation=min_separation, 
            trigger=trigger, 
            trigger_slope=trigger_slope
            )
        
        waveforms_storage = pd.concat( [waveforms_storage,waveforms_analyzed], axis=1 )
        time_storage.extend(time_analyzed)

        '''If not finished yet, try again'''
        counter += 1

    '''Add correct label to the columns and add the time column'''
    waveforms_storage.columns = [ ('event_'+str(i)) for i in range(waveforms_storage.shape[1]) ]
    # waveformList.index = [i for i in range(waveformList.shape[0])]
    df = waveforms_storage.T #This command is only to add the time_storage as a line in an easy way. This is undone later
    df.insert( 0, 'time_epoch', np.array(time_storage) )

    return(df)



#=====================================================================================================
def Acquisition_Waveform( oscilloscope, necessarySamples, path, samples=100, rnd_sample=1_000, min_peaks=2, min_separation=10 ):
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
    samples: int, default 100
        Basically, the number of good samples to save per csv file.
    rnd_sample: int, default 1000
        Parameter required for the "run_acquisition" function.  
    file_name: string
        .
    height: int
        .
    min_peaks: int, default 2
        .
    min_separation: int, default 10
    """

    trigger_value, trigger_slope, y_scale = check_parameters(oscilloscope=oscilloscope)

    trigger_slope_number = trigger_slope_value(trigger_slope)

    # '''Retrieve the conversion parameters from the oscilloscope'''
    converter = units_conversion_parameters(oscilloscope=oscilloscope)

    acquired_samples = 0    # Total amount of samples collected
    saved_csv = 1           # Total of saved csv files 
    files = []              # File names

    while acquired_samples < necessarySamples:

        myprint(f'Try number {saved_csv}. {round(100*acquired_samples/necessarySamples,2)}% ({acquired_samples}/{necessarySamples}).')

        waveforms = run_acquisition(
                oscilloscope=oscilloscope,
                samples=samples,
                rnd_sample=rnd_sample,
                min_peaks=min_peaks,
                min_separation=min_separation,
                trigger=trigger_value,
                trigger_slope=trigger_slope_number,
                converter=converter
                )

        file = f'{path}/file_{saved_csv}.csv'
        waveforms.to_csv(file) # save the partial waveforms DataFrame
        files.append(file)     # add the name to the list

        acquired_samples += waveforms.shape[0]
        saved_csv += 1

    print_scope_config(trigger_value, trigger_slope, y_scale)



#=====================================================================================================
def print_scope_config(trigger_value, trigger_slope=cfg_scope.slope, y_scale=cfg_scope.channel_scale):

    '''
    Parameters for the acquisition
    '''
    myprint(f'\nAcquisition parameters:')
    myprint(f'  Necessary samples: {cfg_scope.necessarySamples}')
    myprint(f'  Samples per csv: {cfg_scope.samples}')
    myprint(f'  Random samples: {cfg_scope.random_samples}')
    myprint(f'  Minimal number of peaks: {cfg_scope.min_peaks}')
    myprint(f'  Minimal separation: {cfg_scope.min_separation}')
    myprint(f'  Email-me: {cfg_scope.email_me}')
    
    '''
    Parameters to set on the oscilloscope
    '''
    myprint(f'Ocilloscope parameters:')
    myprint(f'  Oscilloscope: {cfg_scope.ScopeID}')
    myprint(f'  Channel: {cfg_scope.channel}')
    myprint(f'  Encode Format: {cfg_scope.encode_format}')
    myprint(f'  Channel width: {cfg_scope.width}')
    myprint(f'  Channel position: {cfg_scope.channel_position}')
    myprint(f'  Probe: {cfg_scope.channel_probe}')
    myprint(f'  Persistence: {cfg_scope.persistence}')
    myprint(f'  Scope Resolution: {cfg_scope.scopeResolution}')
    myprint(f'  Horizontal scale: {10E6*cfg_scope.horizontal_scale} micro-sec')
    myprint(f'  Horizontal position: {10E6*cfg_scope.horizontal_position_2} micro-sec')

    '''
    Special parameters for the acquisition
    '''
    myprint(f'  Ch1 scale (y_scale): {y_scale}')
    myprint(f'  Trigger value: {trigger_value} mV')
    myprint(f'  Trigger slope: {trigger_slope}\n')


