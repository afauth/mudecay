import configs.cfg_scope as config
from send_email import Send_Email
import re
import pyvisa
import numpy as np
import pandas as pd
from time import time, ctime
from datetime import timedelta
from scipy.signal import find_peaks
print()

"""
"""

#                           Funções a serem utilizadas
#==========================================================================================================
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

def Acquisition_Waveform( oscilloscope , necessarySamples , height=-100 , min_peaks=2 , oscilloscope_resolution=2500 , numberBins=100, track_progress=False ):
    
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
            scope_values = np.array(  re.split( '\n|,|:CURVE ' , oscilloscope.query('CURVe?') )[1:-1]  ,  float  ) #Selecting the essential part on the string
            peaks , _    = find_peaks(-1*scope_values, height=-height) # Vide bloco de comentários abaixo
            '''
            O base line precisa ser medido ao início de cada aquisição.
            No caso, como ele é ~= -50, valores a partir de 0 já configuram um bom trigger para a aquisição.
            É importante evitar problemas de "pico picado".
            '''

            if len(peaks) >= min_peaks:
                waveformsList = np.vstack( (waveformsList, scope_values) )
                timesList     = np.append( timesList, time(), axis=None )
                if (counter % 5 == 0):
                    print(f'{round(100*(waveformsList.shape[0] - 1)/necessarySamples)}% concluido(s)')
                counter += 1
    elif track_progress == False:
        while waveformsList.shape[0] - 1 < necessarySamples: #-1 porque a primeira linha será deletada depois
            counter += 1
            scope_values = np.array(  re.split( '\n|,|:CURVE ' , oscilloscope.query('CURVe?') )[1:-1]  ,  float  ) #Selecting the essential part on the string
            peaks , _    = find_peaks(-1*scope_values, height=-height) # Vide bloco de comentários abaixo
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
        Anexar os instantes de tempo, individualmente, às waveforms
    ''' 
    waveforms = np.vstack( (timesList, waveformsList) )

    '''
        Cria um DataFrame para os valores das waveforms
    '''
    df = pd.DataFrame(
            data=waveforms,
            index=['time_epoch']+[ str(i) for i in range(waveforms.shape[0]-1) ], 
            columns=[ ('event_'+str(i)) for i in range(waveforms.shape[1]) ],
                    )
    
    
    return(df) #[ epoch_time , time_instant ] X [events]

def Scope_Set_Parameters(oscilloscope):
    '''
    Note: I don't now exactly why, but sometimes an error will occour in this part of the code. It's a runtime error. I THINK it's something to
    do with a problem on the communication between computer and oscilloscope.
    '''
    try:
        oscilloscope.write('ACQuire:STATE RUN')
        print('\nState: RUN')
        oscilloscope.write(f'SELECT:{config.channel} ON')
        print(f'{config.channel} ON')
        oscilloscope.write(f'DATa:SOUrce {config.channel}') 
        #print(f'')
        oscilloscope.write(f'DATa:ENCdg {config.encode_format}') 
        print(f'Encode Format: {config.encode_format}')
        oscilloscope.write(f'DATa:WIDth {config.width}') 
        print(f'Data Width: {config.width}')
        oscilloscope.write(f'{config.channel}:SCAle {config.channel_scale}')
        print(f'{config.channel} scale: {config.channel_scale}')
        oscilloscope.write(f'{config.channel}:POSition {config.channel_position}')
        print(f'{config.channel} position: {config.channel_position}')
        oscilloscope.write(f'{config.channel}:PRObe {config.channel_probe}')
        print(f'{config.channel} probe: {config.channel_probe}')
        oscilloscope.write(f'TRIGger:MAIn:LEVel {config.trigger}')
        print(f'Trigger: {config.trigger}')
        oscilloscope.write(f'HORizontal:MAIn:SCAle {config.horizontal_scale}')
        print(f'Horizontal scale: {config.horizontal_scale}')
        oscilloscope.write(f'HORizontal:MAIn:POSition {config.horizontal_position_1};') 
        print(f'Horizontal Position: {config.horizontal_position_1}')
        oscilloscope.write(f'HORizontal:MAIn:POSition {config.horizontal_position_2};') 
        print(f'Horizontal Position: {config.horizontal_position_2}')
        oscilloscope.write(f'DISplay:PERSistence {config.persistence}') 
        print(f'Persistence: {config.persistence}')
        oscilloscope.write(f'TRIGGER:MAIN:EDGE:SLOPE {config.slope}') 
        print(f'Slope: {config.slope}')
        print(f'Oscilloscope informations: loaded successfully. Scope ID: {rm.list_resources()[0]}\n')
        print( f'\nSCOPE INFOs:\n{oscilloscope.query("WFMPre?")}\n' ) #Command to transfer waveform preamble information.
    except:
        print('Failed to write scope parameters.\nPlease, check connection with the oscilloscope and try again.')
        raise

def Find_Conversion_Parameters(oscilloscope):
    _ = [ 
        substr_to_number( oscilloscope.query('WFMPre:XZEro?')  ),
        substr_to_number( oscilloscope.query('WFMPre:XINcr?')  ),
        substr_to_number( oscilloscope.query('WFMPre:PT_OFf?') ),
        substr_to_number( oscilloscope.query('WFMPre:YZEro?')  ),
        substr_to_number( oscilloscope.query('WFMPre:YMUlt?')  ),
        substr_to_number( oscilloscope.query('WFMPre:YOFf?')   )
        ]
    df = pd.DataFrame( data=_ , index=['X_zero' , 'X_incr' , 'Pt_off' , 'Y_zero' , 'Y_mult' , 'Y_off'] , columns=['value'] )
    return(df)




    

#                           Call oscilloscope and set the parameters
#==========================================================================================================
print()
rm = pyvisa.ResourceManager()                 # Calling PyVisa library
scope = rm.open_resource(str(config.ScopeID)) # Connecting via USB
Scope_Set_Parameters(oscilloscope=scope)


#                           Start time
#========================================================================================================== 
time_start = time()
print( f'\nStarting acquisition... Local time: {ctime(time_start)} \n'  ) # Print da hora local marcada no computador


#                           Print preamble of informations
#==========================================================================================================
print(f'\nNumber of requested samples: {config.necessarySamples}')
print(f'Minimal number of peaks: {config.min_peaks}')
print(f'Progress tracker is {"ON" if config.track_progress == True else "OFF"}')
if config.email_me == True:
    print(f'An email will be sent when acquisition is over or in case of error.\n')
else:
    print('No email.\n')


#                           RUN ACQUISITION
#==========================================================================================================
try:
    df_conversion = Find_Conversion_Parameters(oscilloscope=scope)
    height = height_in_units(df_conversion=df_conversion, height_in_volts=config.trigger)
    #print(height)
    df = Acquisition_Waveform(
                oscilloscope=scope,
                necessarySamples=config.necessarySamples,
                height=height,
                min_peaks=config.min_peaks, 
                oscilloscope_resolution=config.scopeResolution,
                numberBins=config.numberBins,
                track_progress=config.track_progress
                            )
    time_finish = time() # Get finish time
    print( f'\nFinishing acquisition... Local time: {ctime(time_finish)}\nAfter {str(timedelta(seconds=time_finish - time_start))}'  ) # Print da hora local marcada no computador

    print( '\nSaving Data Frame and conversion parameters to .csv files...\n' )
    df_file = f'data/{time_finish}_{config.necessarySamples}-samples_{config.min_peaks}-peaks_waveforms.csv'
    df.to_csv( path_or_buf=df_file, header=True, index=True ) 
    df_conversion.to_csv( path_or_buf=f'data/{time_finish}_conversion-values.csv', header=True, index=True )

    if config.email_me == True:
        subject = f'[MuDecay] Acquisition Finished succesfully'
        msg = f'Acquisition finished! Check the .csv file.\nNumber of samples: {config.necessarySamples}.\nNumber min of peaks: {config.min_peaks} \n\nLocal time: {ctime(time())}\nAfter {str(timedelta(seconds=time_finish - time_start))}'
        Send_Email(subject=subject, msg=msg)

except:
    if config.email_me == True:
        subject = f'[MuDecay] Error on acquisition'
        msg = f'An unexpected error occoured.\n\nPlease, re-check the acquisition and try again.\nLocal time: {ctime(time())}\nAfter {str(timedelta(seconds=time_finish - time_start))}'
        Send_Email(subject=subject, msg=msg)
    print('\nUnexpected error. Please, re-check parameters and oscilloscope connection and try again.\n')
    raise

#                          END
#==========================================================================================================
print('\nEND\n\n')