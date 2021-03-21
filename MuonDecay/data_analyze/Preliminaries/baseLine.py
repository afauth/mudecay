import pandas as pd


#=====================================================================================================
def BaseLine_Sample(waveform, peak, random_left):
    '''
    waveform: column of the waveforms DataFrame.
    peak: correspondent first peak x-coordinate of the waveform.  
    random_left: specified number that tells how much to displace to left before start to retrieve the sample.
    '''
    x_start_pulse_0 = peak - random_left
    
    if x_start_pulse_0 < 0:
        raise('The displacement of the x-coordinate brought the index to somewhere outside the waveform.\nPlease, check the event or try another value of displacement.')

    sample = waveform.iloc[:x_start_pulse_0]

    return(sample)



#=====================================================================================================
def baseLine(waveforms, peaks, random_left=10):
    '''
    waveforms: waveforms DataFrame.
    peaks: peaks DataFrame returned by the Find_Peaks_Waveforms function.  
    random_left: specified number that tells how much to displace to left before start to retrieve the sample.
    '''  

    baseLines = []
    peaks_X0 = peaks[ peaks.columns[0] ]
    
    for i in range( len(waveforms.shape[1]) ):
        event = waveforms[ waveforms.columns[i] ]
        peak  = peaks_X0[i]
        baseLines.append( BaseLine_Sample(waveform=event, peak=peak, random_left=random_left) )
    
    baseLines = pd.concat(baseLines)
    
    return( baseLines.mean() )





# def baseLine(df, height, VA_1):
    
#     baseLines = [] # será uma lista de series
#     for i in range( df.shape[1] ):
#         evento = df[ df.columns[i] ]
#         baseLines.append( baseLine_sample(evento, height, VA_1 = VA_1) )
#     baseLines = pd.concat(baseLines)

#     return(baseLines) #retorna uma Series com os dados de base line



    # def baseLine_sample(series, height, VA_1): # recebe uma series do pandas
#     '''
#     Definimos essa função que retorna uma sample da base line da waveform.
#     Retorna uma amostra da waveform para determinar o valor estatístico dela
#     '''
#     _ = peak_finder(series, height = height)
    
#     '''Pega todos os elementos até o início do primeiro pulso; intervalo exclusivo à direita'''
    
#     if len(_) != 0: # pode acontecer de que o peak_finder não 
#         x_inicio_pulso_0 = _[0] - VA_1 # definido arbitrariamente    
#         sample  = series.iloc[:x_inicio_pulso_0]
#     else:
#         sample = None

#     return( sample ) # este elemento é uma Series