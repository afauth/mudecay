import re
import os
import pandas as pd

from acquisition.DataAcquisition.Acquisition_Waveform import trigger_slope_value



#=====================================================================================================
def retrieve_y_to_volts(path, file='output.txt', sep='/'):
    """
    This function is built to [...]

    Parameters
    ----------
    path: string
        .
    file: string, default = 'output.txt'
        .
    """

    '''
    y_volts = y_zero + y_mult*(y_n - y_off)
    
    SCOPE INFOs:
    1;8;ASC;RP;MSB;2500;"Ch1, DC coupling, 1.0E-2 V/div, 1.0E-6 s/div, 2500 points, Sample mode";Y;4.0E-9;0;-4.0E-7;"s";4.0E-4;0.0E0;5.0E1;"Volts"
    '''

    with open(path+sep+file, 'r') as f:
        output = f.read()

    temp   = re.split( 'mode";' , output )[1]
    temp   = re.split( ';"Volts"' , temp )[0]
    values = re.split( ';', temp )

    y_mult = float(values[-3])
    y_zero = float(values[-2])
    y_off  = float(values[-1])

    df = pd.DataFrame(data=[y_zero, y_mult, y_off])
    df.columns = ['values']
    df.index = ['y_zero', 'y_mult', 'y_off']

    return(df.T)



#                          .
#==========================================================================================================
def convert_y_to_volts(value, converter_df):
    """
    This function is built to [...]

    Parameters
    ----------

    """
    '''
    y_volts = y_zero + y_mult*(y_n - y_off)
    '''


    value_in_volts = converter_df['y_zero'][0] + converter_df['y_mult'][0]*(value - converter_df['y_off'][0])
    value_in_volts *= 1_000 # mV

    return(value_in_volts)



#=====================================================================================================
def trigger_acquisition(path='documents/data/1619314826.6753685/', file='output.txt', sep='/'):
    """
    This function is built to retrieve the value used on the acquisition. It reads the trigger through the 
    output file.

    Parameters
    ----------
    path: string
        .
    file: string, default: 'output.txt'
        .
    sep: string, default: '/'
    """

    '''
    Example:
    Trigger value: -40.0 mV
    '''

    with open(path+sep+file, 'r') as f:
        output = f.read()
    
    temp    = re.split( 'Trigger value: ' , output )[1]
    trigger = float(re.split( ' mV' , temp )[0])

    temp    = re.split( 'Trigger slope: ' , output )[1]
    slope   = re.split( '\n' , temp )[0] #'FALL' or 'RISE'

    return( trigger, slope )


