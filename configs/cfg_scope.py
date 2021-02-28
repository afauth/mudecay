'''
    Oscilloscope ID from the TEKTRONIX [...]
'''
ScopeID = 'USB0::0x0699::0x0363::C061073::INSTR'

'''
    Parameters for the acquisition
'''
#number of samples needed to search
necessarySamples  = 10 
#
min_peaks         = 1    
#número de pontos em cada waveform selecionada
scopeResolution   = 2500  
#number of bins to graph
numberBins        = 100   
#
track_progress    = True 
#
email_me          = False

'''
    Parameters to set on the oscilloscope
'''
channel               = 'CH1'    #Sets or queries which waveform will be transferred from the oscilloscope by the queries. 
encode_format         = 'ASCII'  #Sets or queries the format of the waveform data. ASCII, binary etc.
width                 = 1        #Sets the data width to 1 byte per data point for CURVe data.
channel_scale         = 10.0E-3  #
channel_position      = 2        #
channel_probe         = 1        #
trigger               = -30E-3   #
horizontal_scale      = 1.0E-6   #
horizontal_position_1 = 0        #Initial horizontal position 0 default
horizontal_position_2 = 4.6E-6   #Horizontal position with respect to the start of the oscilloscope window
persistence           = 'INF'    #Infinite persistence
slope                 = 'FALL'   #Negative slope