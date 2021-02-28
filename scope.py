import configs.cfg_scope as config
import re
import pyvisa
import numpy as np
import pandas as pd
from time import time, ctime
from datetime import timedelta
from scipy.signal import find_peaks

def Scope_Set_Parameters(oscilloscope):
    '''
    Note: I don't now exactly why, but sometimes an error will occour in this part of the code. It's a runtime error. I THINK it's something to
    do with a problem on the communication between computer and oscilloscope.
    '''
    try:
        #oscilloscope.clear()
        oscilloscope.write('ACQuire:STATE RUN')
        scope.write("ACQUIRE:MODE SAMPLE")
        scope.write("ACQUIRE:STOPAFTER SEQUENCE")
        #print('\nState: RUN')
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

rm = pyvisa.ResourceManager()                                    # Calling PyVisa library
scope = rm.open_resource('USB0::0x0699::0x0363::C061073::INSTR') # Connecting via USBs
print()

#Scope_Set_Parameters(oscilloscope=scope)

start = time()
#scope.write('ACQuire:STATE RUN')
#scope_values = np.array(  re.split( '\n|,|:CURVE ' , scope.query('CURVe?') )[1:-1]  ,  float  ) #Selecting the essential part on the string
print(scope.query('curve?'))
mid = time()
#peaks , _    = find_peaks(-1*scope_values, height=0)
end = time()

print(f'Time: {timedelta(seconds=mid-start)}')
print(f'Time: {timedelta(seconds=end-mid)}')
print('\ndone\n')

'''
scope.query("*IDN?")
scope.clear()
scope.write("ACQUIRE:STATE OFF")
scope.write("SELECT:CH1 ON")
scope.write('DATa:SOUrce CH1')
scope.write("ACQUIRE:MODE SAMPLE")
scope.write("ACQUIRE:STOPAFTER SEQUENCE")
scope.write('TRIGGER:MAIN:EDGE:SLOPE RISE') 
print( scope.query("MEASUrement:IMMed?") )
scope.write("MEASUREMENT:IMMED:SOURCE CH1")
scope.write("MEASUrement:IMMed:TYPe MINIMUM")
print( scope.query("MEASUrement:IMMed?") )
scope.write("ACQUIRE:STATE ON")
print( scope.query("MEASUrement:IMMed:VALue?") )

MEASUREMENT:IMMED:TYPE AMPLITUDE
MEASUREMENT:IMMED:SOURCE CH1
While BUSY? keep looping
MEASUREMENT:IMMED:VALUE?
'''