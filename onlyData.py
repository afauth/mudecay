import visa
import pylef
import numpy as np
import pandas as pd
from time import time, ctime
from scipy.signal import find_peaks
print()

"""
The next loop is the one who asks the oscilloscope for a list of 2500 points, 
which through SciPy find_peaks, finds all local maxima by simple comparison of neighbouring values.

For the present experiment about 5000 samples were required, so the loop is programmed to have these.
In each iteration when there is a pick, it is discriminated if the first has an amplitude greater than 50 units,
that the second is greater than 20 units and that the difference in microseconds between
both picks is greater than 0.1 units of time.

Finish the process by adding to the list of 'eventsList' lists a list with 2500 points. 
And to the list 'differencesList' the value in units of time of the two picks found.
"""

# while len(eventsList) <= necessarySamples:
#     pointsList = scope.ch1.acquire_y_raw()
#     peaks, _ = find_peaks(-1 * pointsList, height=0)

#     if len(peaks) == 2:
#         if peaks[0] > 50.0:
#             if peaks[1] > 20.0:
#                 difference = peaks[1] - peaks[0]
#                 microseconds = difference / 250
#                 if microseconds > 0.1:
#                     eventsList.append(pointsList)
#                     #differencesList.append(microseconds)
#                     print('number of current samples: ', len(eventsList))

#Funções a serem utilizadas
#==========================================================================================================
def Acquisition_Waveform( necessarySamples , oscilloscope_resolution=2500 , numberBins=100 ):
    
    waveformsList = np.empty( (1,oscilloscope_resolution) ) #array 1 x oscilloscope_resolution; vetor linha
    timesList     = np.empty( (1,1) )    
    '''
    Nota sobre np.empty(shape): tenha em mente que isso é um array criado e preenchido com números aleatórios.
    Os valores não são inexistentes e essa linha deve ser removida depois. 
    Vide mais informações em: https://numpy.org/doc/stable/reference/generated/numpy.empty.html
    '''

    counter = 0
    while waveformsList.shape[0] - 1 < necessarySamples: #-1 porque a primeira linha será deletada depois
        counter += 1
        scope_values = scope.ch1.acquire_y_raw() # Valores, em y, dos pontos do osciloscópio
        peaks , _    = find_peaks(-1*scope_values, height=0) # Vide bloco de comentários abaixo
        '''
        O base line precisa ser medido ao início de cada aquisição. 
        No caso, como ele é ~= -50, valores a partir de 0 já configuram um bom trigger para a aquisição.
        É importante evitar problemas de "pico picado".
        '''

        if len(peaks) > 0:
            waveformsList = np.vstack( (waveformsList, scope_values) )
            timesList     = np.append( timesList, time(), axis=None )
        if (counter % 100 == 0):
            print(f'{round(100*waveformsList.shape[0]/necessarySamples)}% concluido(s)')

    '''
    Lembre-se de deletar a primeira linha, que é auxiliar e feita de números aleatórios.
    '''
    waveformsList = np.delete( arr=waveformsList, obj=0, axis=0 ).T #(y_n X t) --> (y_n X t) 
    timesList     = np.delete( arr=timesList, obj=0, axis=None )

    '''
        Anexar os instantes de tempo, individualmente, às waveforms
    ''' 
    waveforms = np.vstack( (timesList, waveformsList) )

    '''
        Cria um DataFrame e exporta como csv "num-amostras_waveforms_instante-de-tempo.csv"
    '''
    df = pd.DataFrame(
            data=waveforms,
            index=['time_epoch']+[ str(i) for i in range(waveforms.shape[0]-1) ], 
            columns=[ ('event_'+str(i)) for i in range(waveforms.shape[1]) ],
                    )
    df.to_csv( path_or_buf=f'data/{necessarySamples}_waveforms_{time()}.csv', header=True, index=True ) 

    return(df)



#
#==========================================================================================================
number_of_samples = int( input('\nQual o tamanho da amostra que precisa ser obtida? ') )  #number of samples needed to search
osc_resolution    = 2500 #número de pontos em cada waveform selecionada
numberBins        = 100  #number of bins to graph
print()



rm = visa.ResourceManager() #list of connected visa resources with PyVisa as a visa
rm.list_resources() #Print resource list
#scope = rm.open_resource('USB0::0x0699::0x0363::C061073::INSTR') #Enter the resource to be connected manually
scope = pylef.TektronixTBS1062() #use the Pylef functions, to handle oscilloscope
scope.start_acquisition() #Start the aquisition of the waveform
scope.ch1.turn_on() #Turn channel on
scope.ch1.set_scale('0.010') #Ch1 10,0mV = 0,010 VOLTS
scope.ch1.set_position(2) #Vertical position for channel 1 must be 2
scope.ch1.set_probe(1) #Voltage probe must be at 1
scope.trigger.set_level(-0.020) #Trigger in -20mV
scope.set_horizontal_scale(1 / 1000000) #Oscilloscope SEC/DIV time 1.00 us = 1e-06
scope.write('HORizontal:MAIn:POSition 0;') #Initial horizontal position 0 default
scope.write('HORizontal:MAIn:POSition 0.00000460;') #Horizontal position with respect to the start of the oscilloscope window
scope.write('DISplay:PERSistence INF') #Infinite persistence
scope.write('TRIGGER:MAIN:EDGE:SLOPE FALL') #Negative slope



#Iniciando a aquisição
#==========================================================================================================
print( f'\nStarting acquisition. Local time: {ctime(time())} \n'  ) # Print da hora local marcada no computador

Acquisition_Waveform(necessarySamples=number_of_samples, oscilloscope_resolution=osc_resolution, numberBins=numberBins)

print( f'\nEnding acquisition. Local time: {ctime(time())} \n'  ) # Print da hora local marcada no computador



'''
1. (FEITO!) Converter para array
2. (FEITO!) Exportar df como csv
3. Enviar email avisando que acabou
4. (FEITO!) Indicar, sempre que quiser, o número de amostras para coleta 
5. (FEITO!) Adicionar o tempo em época ao data-frame
'''