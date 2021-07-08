# import pandas as pd


# #=====================================================================================================
# def BaseLine_Sample(waveform, peak, random_left):
#     '''
#     waveform: column of the waveforms DataFrame.
#     peak: correspondent first peak x-coordinate of the waveform.  
#     random_left: specified number that tells how much to displace to left before start to retrieve the sample.
#     '''
#     x_start_pulse_0 = peak - random_left
    
#     if x_start_pulse_0 < 0:
#         raise('The displacement of the x-coordinate brought the index to somewhere outside the waveform.\nPlease, check the event or try another value of displacement.')

#     sample = waveform.iloc[:x_start_pulse_0]

#     return(sample)



# #=====================================================================================================
# def baseLine_df(waveforms, peaks, random_left=10):
#     '''
#     waveforms: waveforms DataFrame.
#     peaks: peaks DataFrame returned by the Find_Peaks_Waveforms function.  
#     random_left: specified number that tells how much to displace to left before start to retrieve the sample.
#     '''  

#     baseLines = []
#     peaks_X0 = peaks[ peaks.columns[0] ]
    
#     for i in range( waveforms.shape[1] ):
#         event = waveforms[ waveforms.columns[i] ]
#         peak  = peaks_X0[i]
#         baseLines.append( BaseLine_Sample(waveform=event, peak=peak, random_left=random_left) )
    
#     baseLines = pd.concat(baseLines)
    
#     return( baseLines.mean() )


