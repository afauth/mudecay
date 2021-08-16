import re
import pyvisa
import pandas as pd


'''
    For Y format, the time (absolute coordinate) of a point, relative to the trigger, can
    be calculated using the following formula. N ranges from 0 to 2499.
        Xn = XZEro + XINcr (n - PT_OFf)
    For Y format, the magnitude (usually voltage, relative to ground) (absolute
    coordinate) of a point can be calculated:
        Yn = YZEro + YMUIty (yn - YOFf)
'''

def units_conversion_parameters(oscilloscope):

    scope_infos = oscilloscope.query("WFMPre?")

    # temp   = re.split( 'mode";' , scope_infos )[1]
    # temp   = re.split( ';"Volts"' , temp )[0]
    # values = re.split( ';', temp )

    temp = re.split('XUNIT "s";|YUNIT "Volts"\n', scope_infos)[1]
    values = re.split('YMULT |YZERO |YOFF', temp)

    y_mult = float(values[-3])
    y_zero = float(values[-2])
    y_off  = float(values[-1])

    df = pd.DataFrame(data=[y_zero, y_mult, y_off])
    df.columns = ['values']
    df.index = ['y_zero', 'y_mult', 'y_off']

    return(df.T)



def convert_y_to_mV(value_in_units, converter_df):
    """
    This function is built to [...]

    Parameters
    ----------

    """
    '''
    y_n = y_off + (y_volts - y_zero) / y_mult
    '''

    value_in_volts = converter_df['y_zero'][0] + converter_df['y_mult'][0]*(value_in_units - converter_df['y_off'][0])
    value_in_mV = 1_000*value_in_volts # mV

    return(value_in_mV)



def convert_y_to_units(value_in_volts, converter_df):
    """
    This function is built to [...]

    Parameters
    ----------

    """
    '''
    y_n = y_off + (y_volts - y_zero) / y_mult
    '''

    if converter_df['y_mult'][0] == 0:
        raise ValueError('y_mult must not be zero')

    value_in_units = converter_df['y_off'][0] + (value_in_volts - converter_df['y_zero'][0]) / converter_df['y_mult'][0]

    return(value_in_units)


