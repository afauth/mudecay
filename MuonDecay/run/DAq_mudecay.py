try:
    from acquisition.Configs import cfg_scope
    from acquisition.DataAcquisition.Acquisition_Waveform import Acquisition_Waveform
    from acquisition.DataAcquisition.Set_Scope_Parameters import Set_Scope_Parameters, check_parameters
    from acquisition.SaveOutputs.Save_Output import myprint, outputs, Create_Folder, Acquisition_Type
    from acquisition.SaveOutputs.Send_Email import SendEmail
    from acquisition.DataAcquisition.Conversion_Values import units_conversion_parameters
except:
    raise ImportError('Error on importing modules. Please, try again.')

import os
import pyvisa
import pandas as pd
from time import time, ctime, sleep
from datetime import timedelta


#                           Initial time and create storage folder
#==========================================================================================================

'''Initial time'''
time_start = time()

'''Create folder to store logging, waveforms and conversion file'''
acquisition_type = Acquisition_Type(min_peaks=cfg_scope.min_peaks)
folder_name = f'../documents/data/{acquisition_type}/{time_start}'
Create_Folder(name=folder_name) #documents/data/{tag_name}/{time_start}

'''Print local time and type of acquisition'''
myprint( f'\nStarting acquisition... Local time: {ctime(time_start)}\nThis is a \"{acquisition_type}\" type of acquisition.\n'  ) 
sleep(3)



#                           Call oscilloscope and set the parameters
#==========================================================================================================
rm = pyvisa.ResourceManager()                    # Calling PyVisa library
scope = rm.open_resource(str(cfg_scope.ScopeID)) # Connecting via USB

Set_Scope_Parameters(oscilloscope=scope)
trigger, y_scale = check_parameters(oscilloscope=scope)
converter = units_conversion_parameters(oscilloscope=scope)



#                           Print preamble of informations
#==========================================================================================================
myprint(f'\nNumber of requested samples: {cfg_scope.necessarySamples}')
myprint(f'Minimal number of peaks: {cfg_scope.min_peaks}')
if cfg_scope.email_me == True:
    myprint(f'An email will be sent when acquisition is over or in case of error.\n')
else:
    myprint('No email.\n')



#                           RUN ACQUISITION
#==========================================================================================================

'''
Converting trigger to proper value; the software trigger and the hardware trigger must match
'''

#converter = units_conversion_parameters(oscilloscope=scope)
#height     = convert_y_to_units(cfg_scope.trigger, conversion)
#trigger = 1000*cfg_scope.trigger #mV
#print('\ntrigger =', trigger, '\n')


try: # Try to get all the datas

    Acquisition_Waveform(
        oscilloscope=scope,
        necessarySamples=cfg_scope.necessarySamples,
        path=folder_name,
        height=trigger,
        min_peaks=cfg_scope.min_peaks,
        min_separation=cfg_scope.min_separation,
        samples=cfg_scope.samples,
        rnd_sample=cfg_scope.random_samples, 
        converter=converter
    )
    


except: # Log error. Raise error. Interrupt the execution.

    time_finish = time()
    myprint(f'\n\nFATAL ERROR.\nAn unexpected error occoured.\n\nPlease, re-check the acquisition and try again.\n\nLocal time: {ctime(time())}\nAfter {str(timedelta(seconds=time_finish - time_start))}')
        
    '''Assemble all the terminal outputs in one txt file'''
    logging_file = f"{folder_name}/output.txt"
    open(logging_file, "w").write("\n".join(outputs))
        
    if cfg_scope.email_me == True:
        subject = f'[MuDecay] Acquisition results'
        with open(logging_file) as f:
            msg = f.read()
            SendEmail(subject=subject, msg=f'ERROR\n {msg}')
        
    raise ("Problem on the acquisition. Please, re-run.")



else: # Execute if everything occoured as expected

    time_finish = time() # Get finish time
    myprint( f'\nFinishing acquisition... Local time: {ctime(time_finish)}\nAfter {str(timedelta(seconds=time_finish - time_start))}'  )

    myprint('\nEND acquisition\n\n')

    '''Assemble all the terminal outputs in one txt file'''
    logging_file = f"{folder_name}/output.txt"
    open(logging_file, "w").write("\n".join(outputs))

    '''Send an email'''
    if cfg_scope.email_me == True:
        subject = f'[MuDecay] Acquisition results'
        with open(logging_file) as f:
            msg = f.read()
            SendEmail(subject=subject, msg=msg)

"""
Ainda precisa implementar a parte de coletar e devolver os dados já analizados

Implementar parte que verifica se o csv é vazio ou não e o deleta?
"""
