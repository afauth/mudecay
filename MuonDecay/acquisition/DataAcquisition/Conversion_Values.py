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

    temp   = re.split( 'mode";' , scope_infos )[1]
    temp   = re.split( ';"Volts"' , temp )[0]
    values = re.split( ';', temp )

    y_mult = float(values[-3])
    y_zero = float(values[-2])
    y_off  = float(values[-1])

    df = pd.DataFrame(data=[y_zero, y_mult, y_off])
    df.columns = ['values']
    df.index = ['y_zero', 'y_mult', 'y_off']

    return(df.T)



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


def Find_Conversion_Parameters(oscilloscope):
    _ = [ 
        substr_to_number( oscilloscope.query('WFMPre:XZEro?')  ),
        substr_to_number( oscilloscope.query('WFMPre:XINcr?')  ),
        substr_to_number( oscilloscope.query('WFMPre:PT_OFf?') ),
        substr_to_number( oscilloscope.query('WFMPre:YZEro?')  ),
        substr_to_number( oscilloscope.query('WFMPre:YMUlt?')  ),
        substr_to_number( oscilloscope.query('WFMPre:YOFf?')   )
        ]
    df = pd.DataFrame( 
        data=_ ,
        index=['X_zero' , 'X_incr' , 'Pt_off' , 'Y_zero' , 'Y_mult' , 'Y_off'] , 
        columns=['value'] 
                    )
    return(df)
