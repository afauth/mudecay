import configs.cfg_scope as config
import re
import pyvisa
import numpy as np
import pandas as pd
from time import time, ctime
from scipy.signal import find_peaks

print()

"""
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

def Acquisition_Waveform( oscilloscope , necessarySamples , min_peaks=2 , oscilloscope_resolution=2500 , numberBins=100, track_progress=False ):
    
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

def Scope_Set_Parameters(oscilloscope):
    '''
    Note: I don't now exactly why, but sometimes an error will occour in this part of the code. It's a runtime error. I THINK it's something to
    do with a problem on the communication between computer and oscilloscope.
    '''
    try:
        scope.write('ACQuire:STATE RUN')
        print('\nState: RUN')
        scope.write(f'SELECT:{config.channel} ON')
        print(f'{config.channel} ON')
        scope.write(f'DATa:SOUrce {config.channel}') 
        #print(f'')
        scope.write(f'DATa:ENCdg {config.encode_format}') 
        print(f'Encode Format: {config.encode_format}')
        scope.write(f'DATa:WIDth {config.width}') 
        print(f'Data Width: {config.width}')
        scope.write(f'{config.channel}:SCAle {config.channel_scale}')
        print(f'{config.channel} scale: {config.channel_scale}')
        scope.write(f'{config.channel}:POSition {config.channel_position}')
        print(f'{config.channel} position: {config.channel_position}')
        scope.write(f'{config.channel}:PRObe {config.channel_probe}')
        print(f'{config.channel} probe: {config.channel_probe}')
        scope.write(f'TRIGger:MAIn:LEVel {config.trigger}')
        print(f'Trigger: {config.trigger}')
        scope.write(f'HORizontal:MAIn:SCAle {config.horizontal_scale}')
        print(f'Horizontal scale: {config.horizontal_scale}')
        scope.write(f'HORizontal:MAIn:POSition {config.horizontal_position_1};') 
        print(f'Horizontal Position: {config.horizontal_position_1}')
        scope.write(f'HORizontal:MAIn:POSition {config.horizontal_position_2};') 
        print(f'Horizontal Position: {config.horizontal_position_2}')
        scope.write(f'DISplay:PERSistence {config.persistence}') 
        print(f'Persistence: {config.persistence}')
        scope.write(f'TRIGGER:MAIN:EDGE:SLOPE {config.slope}') 
        print(f'Slope: {config.slope}')
        print(f'Oscilloscope informations: loaded successfully. Scope ID: {rm.list_resources()[0]}\n')
        print( f'\nSCOPE INFOs:\n{scope.query("WFMPre?")}\n' ) #Command to transfer waveform preamble information.
    except:
         raise Exception('Failed to write scope parameters.\nPlease, check connection with the oscilloscope and try again.')



#
#==========================================================================================================
print()
rm = pyvisa.ResourceManager() # Calling PyVisa library
scope = rm.open_resource(str(config.ScopeID)) # Connecting via USB

Scope_Set_Parameters(oscilloscope=scope)

#Iniciando a aquisição
#==========================================================================================================
print( f'\nStarting acquisition... Local time: {ctime(time())} \n'  ) # Print da hora local marcada no computador

df = Acquisition_Waveform(
            oscilloscope=scope,
            necessarySamples=config.necessarySamples, 
            min_peaks=config.min_peaks, 
            oscilloscope_resolution=config.scopeResolution,
            numberBins=config.numberBins,
            track_progress=config.track_progress
                         )

print( f'\nFinishing acquisition... Local time: {ctime(time())} \n'  ) # Print da hora local marcada no computador

print( '\nSaving .csv file...\n' )

df.to_csv( path_or_buf=f'data/{config.necessarySamples}-samples_waveforms_{time()}.csv', header=True, index=True ) 

print('\nEND\n\n')

'''
1. (FEITO!) Converter para array
2. (FEITO!) Exportar df como csv
3. Enviar email avisando que acabou
4. (FEITO!) Indicar, sempre que quiser, o número de amostras para coleta 
5. (FEITO!) Adicionar o tempo em época ao data-frame
'''