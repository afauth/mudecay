# '''
#         Add time in units. 
#             Note: this "time" is actually the "delta_t" in convenient units where the "zero" is the time after triggering the threshold.
#             Note 2: on the df, we can create a column with empty/None/NaN values and the fill only the spaces that interest. 
#         That's because the first row will not be converted to a number/ time instant
#     '''

# aux    = df.index[1:].to_numpy().astype(float) #the first index is a name, so cannot be a converted to a number
    
# df['time_units'] = np.NaN
# df['time_units'].iloc[1:] = translada_x_n(x_zero=XZEro, x_incr=XINcr, n_ranges=aux, pt_off=PT_OFf)

# '''
#         Correcting y-values on the waveform. It's made in relation to the formula shown on the "Programmer's Manual"
#     '''

# waveformsList_units = translada_y_n(y_zero=YZEro, y_mult=YMUlt, y_n=waveformsList, y_off=YOFf) #The values are now in the units show on the preamble

import pandas as pd

def translada_x_n(x_zero , x_incr , n_ranges , pt_off):
    return( x_zero + x_incr*(n_ranges - pt_off) )

def translada_y_n(y_zero , y_mult , y_n , y_off):
    return( y_zero + y_mult*(y_n - y_off) )

df = pd.DataFrame( data=[1,2,3,4,5] )
print(df)