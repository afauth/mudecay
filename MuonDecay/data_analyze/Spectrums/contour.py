import pandas as pd
import numpy as np

# def derivada_x(s): # insira uma series na entrada; o valor retornado está em coordenadas do eixo x
#     '''
#     Encontra as diferenças entre elementos lado-a-lado. Serve para avaliar quando estamos começando ou terminando um pulso.
#     '''
#     VA_derivada_baseLine = 5  #   flutuação/amplitude máxima da base-line;
#                               #   valor arbirtrário para saber se o número em questão está fora da 
#                               # base-line; não é exatamente a derivada
#     _ = []
#     for i in range( len(s) - 1 ): # i = index da series
#         if abs(s[i] - s[i+1]) > VA_derivada_baseLine:
#             _.append(i) 
        
#     return (_) # o valor retornado está em coordenadas do eixo x



# def contorno_limite_derivada(series, VA_1, VA_2, height): # recebe uma Series do pandas para começar
#     '''
#     Define um recorte de onde se deve buscar um pulso e os seus delimitadores
#     VA_1 e VA_2 são variáveis arbitrárias para definir a largura do pulso 
#     '''
#     peak = peak_finder(series, height=height) # encontrar os picos da waveform
    
#     s1 = series[ (peak[0] - VA_1):(peak[0] + VA_2) ] # recortar envolta dos picos
#     s2 = series[ (peak[1] - VA_1):(peak[1] + VA_2) ]
    
#     df1 = pd.DataFrame( dict(s1 = s1) ).reset_index() # cria um Data Frame com os valores do recorte
#     df1.columns = ['time', 's1']                      # renomeia a coluna do data frame
#     df2 = pd.DataFrame( dict(s1 = s2) ).reset_index()
#     df2.columns = ['time', 's2']
    
#     '''
#     Calcular a "derivada" em cada ponto no entorno, para saber os limitantes do pulso
#     Ao terminar, retornar o data frame que contem os valores limitantes do contorno do pulso
#     '''  
#     indexLim_1 = derivada_x( df1['s1'] ) # índices limitantes
#     indexLim_2 = derivada_x( df2['s2'] )
    
#     # redefine os valores para apenas os limitantes do data frame
#     df1 = df1.iloc[    [  indexLim_1[0], indexLim_1[-1]  ]    ] 
#     df2 = df2.iloc[    [  indexLim_2[0], indexLim_2[-1]  ]    ] 
    
#     # print(df2) # series marcada pelas colunas 
    
#     # da Series original, temos agora o contorno do pulso
#     s1 = series[ df1['time'].iloc[0] : df1['time'].iloc[1]+1 ] # soma 1 para incluir o último termo
#     s2 = series[ df2['time'].iloc[0] : df2['time'].iloc[1]+1 ] 
    
#     # print(s2)
    
#     pulsos = s1, s2
    
#     return(pulsos) # retorna os dois contornos, um de cada pulso



def contour_arbitrary(waveform, peak, random_left, random_right):
    '''
    waveform: column of the waveforms DataFrame.
    peak: 
    random_left: specified number that tells how much to displace to left before start to retrieve the sample.
    random_right: idem, but to the right side
    '''

    """
    Peaks order: peak_X0, peak_X1, peak_Y0, peak_Y1. 
    The values of the peaks are not in seconds, but in ADC-Channels.
    """
    peak_X0 = int(peak[0])
    peak_X1 = int(peak[1])

    limits_0 = [ peak_X0-random_left, peak_X0+random_right ]
    limits_1 = [ peak_X1-random_left, peak_X1+random_right ] 

    pulse_0 = waveform.iloc[ limits_0[0]:limits_0[1] ].to_list()
    pulse_1 = waveform.iloc[ limits_1[0]:limits_1[1] ].to_list()

    return(pulse_0, pulse_1) # gives the y-values result



#=====================================================================================================
def contour_arbitrary_df(waveforms, peaks, random_left=10, random_right=15):
    '''
    waveforms:
    peaks: 
    random_left: specified number that tells how much to displace to left before start to retrieve the sample.
    random_right: idem, but to the right side
    '''
    
    """
    Test for elements outside waveform:
        in order to use the query method, a copy-DataFrame will be created and renamed with the correspondent
        columns names. It will avoid having problems if we want to rename the columns on the peaks DataFrame later.
    """
    peaks_cp = peaks.copy()
    peaks_cp.columns = ['peak_X0', 'peak_X1', 'peak_Y0', 'peak_Y1']
    problems = peaks_cp.query("peak_X0 < @random_right  |  peak_X1 > 2500 - @random_left")
    
    if len(problems.index) > 0: # if it's not empty, then delete the problems
        
        problems_list = problems.index.to_list()

        peaks_cp.drop(labels=problems_list, inplace=True)    
        print(f'\n\nWhen trying to handle with the contour, a few events seem to have a problem with the contour going outside the waveform limit.\nThey are {problems_list}. {len(problems_list)} in total.\nTo solve, please check the arbitrary values for the pulse width.\n\n')

        wvfrms = waveforms.copy() # if any event is removed from from peaks, it also needs to be removed on the waveforms 
        wvfrms.drop(labels=problems_list, axis=1, inplace=True)
    
    else:
        
        wvfrms = waveforms

    """
    Append contours to two DataFrames
    """
    pulses_0 = pd.DataFrame()
    pulses_1 = pd.DataFrame()

    for i in range(wvfrms.shape[1]):
        
        event = wvfrms[ wvfrms.columns[i] ]
        event_peaks = peaks_cp.iloc[i]
        pulse_0 , pulse_1 = contour_arbitrary(waveform=event, peak=event_peaks, random_left=random_left, random_right=random_right)
        pulses_0[ wvfrms.columns[i] ] = pulse_0
        pulses_1[ wvfrms.columns[i] ] = pulse_1
    
    return(pulses_0, pulses_1)