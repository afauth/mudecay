import visa
import pylef
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

necessarySamples = 500 #number of samples needed to search
numberBins = 100 #number of bins to graph
eventsList = [] #list that stores event lists with 2500 points
differencesList = [] #list that stores the difference in microseconds of each 2500 point list
readDifferences = [] #list that stores the data saved after the search

rm = visa.ResourceManager() #list of connected visa resources with PyVisa as a visa
rm.list_resources() #Print resource list
scope = rm.open_resource('USB0::0x0699::0x0363::C061073::INSTR') #Enter the resource to be connected manually
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
while len(eventsList) <= necessarySamples:
    pointsList = scope.ch1.acquire_y_raw()
    peaks, _ = find_peaks(-1 * pointsList, height=0)

    if len(peaks) == 2:
        if peaks[0] > 50.0:
            if peaks[1] > 20.0:
                difference = peaks[1] - peaks[0]
                microseconds = difference / 250
                if microseconds > 0.1:
                    eventsList.append(pointsList)
                    differencesList.append(microseconds)
                    print('number of current samples: ', len(eventsList))

"""
stores the list of events in CSV format, 
if you have other files in your directory, do not 
forget to change your name so that it is not replaced
"""
np.savetxt("EventsList.csv", eventsList, delimiter=",") 
np.savetxt("DifferencesList.csv", differencesList, delimiter=",")

