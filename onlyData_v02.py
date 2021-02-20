import re
import pyvisa
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

#Funções a serem utilizadas
#==========================================================================================================

def translada_x_n(x_zero , x_incr , n_ranges , pt_off):
    return( x_zero + x_incr*(n_ranges - pt_off) )

def translada_y_n(y_zero , y_mult , y_n , y_off):
    return( y_zero + y_mult*(y_n - y_off) )

'''
    For Y format, the time (absolute coordinate) of a point, relative to the trigger, can
be calculated using the following formula. N ranges from 0 to 2499.
        Xn = XZEro + XINcr (n - PT_OFf)
    For Y format, the magnitude (usually voltage, relative to ground) (absolute
coordinate) of a point can be calculated:
        Yn = YZEro + YMUIty (yn - YOFf)
'''

def substr_to_number(string): #ex.: 
    return(   float(  re.split(' |\n', string)[1]  )   )

def Acquisition_Waveform( necessarySamples , oscilloscope , min_peaks=2 , oscilloscope_resolution=2500 , numberBins=100, track_progress=False ):
    
    waveformsList = np.empty( (1,oscilloscope_resolution) ) #array 1 x oscilloscope_resolution; vetor linha
    timesList     = np.empty( (1,1) )    
    '''
    Nota sobre np.empty(shape): tenha em mente que isso é um array criado e preenchido com números aleatórios.
    Os valores não são inexistentes e essa linha deve ser removida depois. 
    Vide mais informações em: https://numpy.org/doc/stable/reference/generated/numpy.empty.html
    '''

    '''
        Acquisition. Note: pay attention on the on the conditional "len(peaks) >= min_peaks" that defines the minimal number of peaks to be
        considered as an "event". The second conditional is just a tracking of progress for long acquisitions.
    '''
    counter = 0
    if track_progress == True:
        while waveformsList.shape[0] - 1 < necessarySamples: #-1 porque a primeira linha será deletada depois
            counter += 1
            scope_values = np.array(  re.split( '\n|,|:CURVE ' , oscilloscope.query('CURVe?') )[1:-1]  ,  float  ) #Selecting the essential part on the string
            peaks , _    = find_peaks(-1*scope_values, height=0) # Vide bloco de comentários abaixo
            '''
            O base line precisa ser medido ao início de cada aquisição.
            No caso, como ele é ~= -50, valores a partir de 0 já configuram um bom trigger para a aquisição.
            É importante evitar problemas de "pico picado".
            '''

            if len(peaks) >= min_peaks:
                waveformsList = np.vstack( (waveformsList, scope_values) )
                timesList     = np.append( timesList, time(), axis=None )
            if (counter % 100 == 0):
                print(f'{round(100*waveformsList.shape[0]/necessarySamples)}% concluido(s)')
    elif track_progress == False:
        while waveformsList.shape[0] - 1 < necessarySamples: #-1 porque a primeira linha será deletada depois
            counter += 1
            scope_values = np.array(  re.split( '\n|,|:CURVE ' , oscilloscope.query('CURVe?') )[1:-1]  ,  float  ) #Selecting the essential part on the string
            peaks , _    = find_peaks(-1*scope_values, height=0) # Vide bloco de comentários abaixo
            '''
            O base line precisa ser medido ao início de cada aquisição.
            No caso, como ele é ~= -50, valores a partir de 0 já configuram um bom trigger para a aquisição.
            É importante evitar problemas de "pico picado".
            '''

            if len(peaks) >= min_peaks:
                waveformsList = np.vstack( (waveformsList, scope_values) )
                timesList     = np.append( timesList, time(), axis=None )
    else:
        raise(TypeError('The variable track_error must be True or False'))

    '''
        Lembre-se de deletar a primeira linha, que é auxiliar e feita de números aleatórios.
    '''
    waveformsList = np.delete( arr=waveformsList, obj=0, axis=0 ).T #(y_n X t) --> (y_n X t) 
    timesList     = np.delete( arr=timesList, obj=0, axis=None )

    '''
        Correcting y-values on the waveform. It's made in relation to the formula shown on the "Programmer's Manual"
    '''
    YZEro = substr_to_number( oscilloscope.query('WFMPre:YZEro?') )
    YMUlt = substr_to_number( oscilloscope.query('WFMPre:YMUlt?') )
    YOFf  = substr_to_number( oscilloscope.query('WFMPre:YOFf?') )
    waveformsList_units = translada_y_n(y_zero=YZEro, y_mult=YMUlt, y_n=waveformsList, y_off=YOFf) #The values are now in the units show on the preamble

    '''
        Anexar os instantes de tempo, individualmente, às waveforms
    ''' 
    waveforms = np.vstack( (timesList, waveformsList_units) )

    '''
        Cria um DataFrame
    '''
    df = pd.DataFrame(
            data=waveforms,
            index=['time_epoch']+[ str(i) for i in range(waveforms.shape[0]-1) ], 
            columns=[ ('event_'+str(i)) for i in range(waveforms.shape[1]) ],
                    )
    
    '''
        Add time in units. 
            Note: this "time" is actually the "delta_t" in convenient units where the "zero" is the time after triggering the threshold.
            Note 2: on the df, we can create a column with empty/None/NaN values and the fill only the spaces that interest. 
        That's because the first row will not be converted to a number/ time instant
    '''
    XZEro  = substr_to_number( oscilloscope.query('WFMPre:XZEro?') )
    XINcr  = substr_to_number( oscilloscope.query('WFMPre:XINcr?') )
    PT_OFf = substr_to_number( oscilloscope.query('WFMPre:PT_OFf?') )
    aux    = df.index[1:].to_numpy().astype(np.float64) #the first index is a name, so cannot be a converted to a number
    
    df['time_units'] = np.NaN
    df['time_units'].iloc[1:] = translada_x_n(x_zero=XZEro, x_incr=XINcr, n_ranges=aux, pt_off=PT_OFf)


    return(df) #[ epoch_time , time_instant ] X [events]




#
#==========================================================================================================
print()
# rm = pyvisa.ResourceManager() #list of connected visa resources with PyVisa as a visa
# rm.list_resources() #Print resource list
# scope = rm.open_resource('USB0::0x0699::0x0363::C061073::INSTR') #Enter the resource to be connected manually 'USB0::0x0699::0x0363::C061073::INSTR'; 'TEKTRONIX,TDS 1002B,C061073,CF:91.1CT FV:v22.11\n'
# scope = pylef.TektronixTBS1062() #use the Pylef functions, to handle oscilloscope
# scope.start_acquisition() #Start the aquisition of the waveform
# scope.ch1.turn_on() #Turn channel on
# scope.ch1.set_scale('0.010') #Ch1 10,0mV = 0,010 VOLTS
# scope.ch1.set_position(2) #Vertical position for channel 1 must be 2
# scope.ch1.set_probe(1) #Voltage probe must be at 1
# scope.trigger.set_level(-0.020) #Trigger in -20mV
# scope.set_horizontal_scale(1 / 1000000) #Oscilloscope SEC/DIV time 1.00 us = 1e-06
# scope.write('HORizontal:MAIn:POSition 0;') #Initial horizontal position 0 default
# scope.write('HORizontal:MAIn:POSition 0.00000460;') #Horizontal position with respect to the start of the oscilloscope window
# scope.write('DISplay:PERSistence INF') #Infinite persistence
# scope.write('TRIGGER:MAIN:EDGE:SLOPE FALL') #Negative slope

rm = pyvisa.ResourceManager() # Calling PyVisa library
scope = rm.open_resource('USB0::0x0699::0x0363::C061073::INSTR') # Connecting via USB

scope.write('ACQuire:STATE RUN')
scope.write('SELECT:CH1 ON')
scope.write('DATa:SOUrce CH1') #Sets or queries which waveform will be transferred from the oscilloscope by the queries. 
scope.write('DATa:ENCdg ASCII') #Sets or queries the format of the waveform data. ASCII, binary etc.
scope.write('DATa:WIDth 1') #Sets the data width to 1 byte per data point for CURVe data.
scope.write('CH1:SCAle 0.010')
scope.write('CH1:POSition 2')
scope.write('CH1:PRObe 1')
scope.write('TRIGger:MAIn:LEVel -0.020')
scope.write('HORizontal:MAIn:SCAle 1.0E-6')
scope.write('HORizontal:MAIn:POSition 0') #Initial horizontal position 0 default
scope.write('HORizontal:MAIn:POSition 0.00000460') #Horizontal position with respect to the start of the oscilloscope window
scope.write('DISplay:PERSistence INF') #Infinite persistence
scope.write('TRIGGER:MAIN:EDGE:SLOPE FALL') #Negative slope

'''
    Note: I don't now exactly why, but sometimes an error will occour in this part of the code. It's a runtime error. I THINK it's something to
    do with a problem on the communication between computer and oscilloscope.
'''
print( f'\nSCOPE INFOs:\n{scope.query("WFMPre?")}\n' )#Command to transfer waveform preamble information.
print(f'\nOscilloscope informations: loaded. {rm.list_resources()[0]}\n')

number_of_samples = int( input('\nQual o tamanho da amostra que precisa ser obtida? ') )  #number of samples needed to search
osc_resolution    = 2500 #número de pontos em cada waveform selecionada
numberBins        = 100  #number of bins to graph


#Iniciando a aquisição
#==========================================================================================================
print( f'\nStarting acquisition... Local time: {ctime(time())} \n'  ) # Print da hora local marcada no computador

df = Acquisition_Waveform(
            necessarySamples=number_of_samples, 
            oscilloscope=scope,
            min_peaks=1, 
            oscilloscope_resolution=osc_resolution,
            numberBins=numberBins
                         )

print( f'\nFinishing acquisition... Local time: {ctime(time())} \n'  ) # Print da hora local marcada no computador

print( '\nSaving .csv file...\n' )

df.to_csv( path_or_buf=f'data/{number_of_samples}-samples_waveforms_{time()}.csv', header=True, index=True ) 

print('\nEND\n\n')

'''
1. (FEITO!) Converter para array
2. (FEITO!) Exportar df como csv
3. Enviar email avisando que acabou
4. (FEITO!) Indicar, sempre que quiser, o número de amostras para coleta 
5. (FEITO!) Adicionar o tempo em época ao data-frame
'''