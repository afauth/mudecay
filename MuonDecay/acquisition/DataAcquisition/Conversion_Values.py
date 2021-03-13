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