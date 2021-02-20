print()
import pyvisa
import visa
import numpy as np
from struct import unpack
import pylab

# Establish Connection
rm = pyvisa.ResourceManager() # Calling PyVisaPy library
print (rm.list_resources())
scope = rm.open_resource('USB0::0x0699::0x0363::C061073::INSTR') # Connecting via USB

scope.write('ACQuire:STATE RUN')
scope.write('SELECT:CH1 ON')
scope.write('CH1:SCAle 0.010')
scope.write('CH1:POSition 2')
scope.write('CH1:PRObe 1')
scope.write('TRIGger:MAIn:LEVel -0.020')
scope.write('HORizontal:MAIn:SCAle 1.0E-6')

scope.write('HORizontal:MAIn:POSition 0;') #Initial horizontal position 0 default
scope.write('HORizontal:MAIn:POSition 0.00000460;') #Horizontal position with respect to the start of the oscilloscope window
scope.write('DISplay:PERSistence INF') #Infinite persistence
scope.write('TRIGGER:MAIN:EDGE:SLOPE FALL') #Negative slope


'''
(OK) rm = pyvisa.ResourceManager() #list of connected visa resources with PyVisa as a visa
(OK) rm.list_resources() #Print resource list
(OK) scope = rm.open_resource('USB0::0x0699::0x0363::C061073::INSTR') #Enter the resource to be connected manually 'USB0::0x0699::0x0363::C061073::INSTR'; 'TEKTRONIX,TDS 1002B,C061073,CF:91.1CT FV:v22.11\n'
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
'''

print('\nFinished\n')