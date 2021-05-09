from acquisition.Configs import cfg_scope #import config file
from acquisition.SaveOutputs.Save_Output import myprint, outputs #import function "myprint" and variable "outputs"
import pyvisa
from time import sleep



def Scope_Parameters(oscilloscope):

    #oscilloscope.write('ACQuire:STATE RUN')
    #print('\nState: RUN')
                
    oscilloscope.write(f'SELECT:{cfg_scope.channel} ON')
    #print(f'\n{cfg_scope.channel} ON')

    oscilloscope.write(f'DATa:SOUrce {cfg_scope.channel}') 
    #print(f'')
                
    oscilloscope.write(f'DATa:ENCdg {cfg_scope.encode_format}') 
    #print(f'Encode Format: {cfg_scope.encode_format}')

    oscilloscope.write(f'DATa:WIDth {cfg_scope.width}') 
    #print(f'Data Width: {cfg_scope.width}')
                
    oscilloscope.write(f'{cfg_scope.channel}:SCAle {cfg_scope.channel_scale}')
    # myprint(f'{cfg_scope.channel} scale: {cfg_scope.channel_scale}')
                
    oscilloscope.write(f'{cfg_scope.channel}:POSition {cfg_scope.channel_position}')
    # myprint(f'{cfg_scope.channel} position: {cfg_scope.channel_position}')
                
    oscilloscope.write(f'{cfg_scope.channel}:PRObe {cfg_scope.channel_probe}')
    #print(f'{cfg_scope.channel} probe: {cfg_scope.channel_probe}')
                
    oscilloscope.write(f'TRIGger:MAIn:LEVel {cfg_scope.trigger}')
    # myprint(f'Trigger: {1_000*cfg_scope.trigger} mV')
                
    oscilloscope.write(f'HORizontal:MAIn:SCAle {cfg_scope.horizontal_scale}')
    # myprint(f'Horizontal scale: {cfg_scope.horizontal_scale}')
                
    oscilloscope.write(f'HORizontal:MAIn:POSition {cfg_scope.horizontal_position_1};') 
    #print(f'Horizontal Position: {cfg_scope.horizontal_position_1}')
                
    oscilloscope.write(f'HORizontal:MAIn:POSition {cfg_scope.horizontal_position_2};') 
    # myprint(f'Horizontal Position: {cfg_scope.horizontal_position_2}')
                
    oscilloscope.write(f'DISplay:PERSistence {cfg_scope.persistence}') 
    #print(f'Persistence: {cfg_scope.persistence}')
                
    oscilloscope.write(f'TRIGGER:MAIN:EDGE:SLOPE {cfg_scope.slope}') 
    #print(f'Slope: {cfg_scope.slope}')
            
    myprint( f'\nSCOPE INFOs:\n{oscilloscope.query("WFMPre?")}\n' ) #Command to transfer waveform preamble information.

    # myprint(f'TRIGGER: {1000*cfg_scope.trigger} mV\n\n') 



def Set_Scope_Parameters(oscilloscope):
    '''
    Note: I don't now exactly why, but sometimes an error will occour in this part of the code. It's a runtime error. I THINK it's something to
    do with a problem on the communication between computer and oscilloscope.
    '''
    try_set = True
    counter = 0
    sleep(3)

    while try_set == True:
        sleep(1)
        
        try:

            Scope_Parameters(oscilloscope=oscilloscope)

        except:
            
            counter += 1
            myprint(f'FAILED {counter} to write scope parameters.')

            if counter >= 3:
                myprint('FAILED TO WRITE scope parameters, even after three attempts.\nPlease, check connection with the oscilloscope and try again.')
                raise
        
        else:

            try_set = False
            myprint(f'{cfg_scope.channel} scale: {1000*cfg_scope.channel_scale} mV')
            myprint(f'Trigger: {1_000*cfg_scope.trigger} mV')
            myprint(f'Horizontal scale: {10E6*cfg_scope.horizontal_scale} micro-sec')
            myprint(f'Horizontal Position: {10E6*cfg_scope.horizontal_position_2} micro-sec')

            myprint(f'\nOscilloscope informations: LOADED SUCESSFULLY after {counter} attempt(s). Check config file for more details.\n')



def verify_trigger(oscilloscope, trigger):

    scope_trigger = oscilloscope.query("Trigger?")
    
    temp    = re.split( 'Trigger: ' , output )[1]
    trigger = float(re.split( ' mV' , temp )[0])
