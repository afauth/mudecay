import pandas as pd
import numpy as np



#=====================================================================================================
def integral_rectangle(y_data, dx):
    '''
    y_data: the y-values to sum
    dx: the interval between the y-values

    Integral = sum(y*dx) ~= sum(y)*dx
    '''

    integral = sum(y_data)*dx
    
    return(integral)



#=====================================================================================================
def integral_rectangle_df(waveforms, dx=1):
    '''
    waveforms: the waveforms collection DataFrame
    dx: the interval between the y-values
    '''

    Integrals = []

    for i in range( waveforms.shape[1] ):
        event = waveforms[ waveforms.columns[i] ]
        integral = integral_rectangle(y_data=event, dx=dx)
        Integrals.append(integral)

    return( pd.DataFrame(Integrals) )
