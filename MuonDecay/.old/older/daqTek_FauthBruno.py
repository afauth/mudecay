#=========================================================
#Código feito para a Escola de Verão 2020 do IFGW
#acrescentamos no cógigo original do Villagran
#- tempo em UTC para cada evento
#- gráfico parcial durante a aquisição
#- lê dados de um arquivo e já faz um gráfico no início da
#  aquisição. Seve para uma demonstração do experimento, visto que
#  para um fit razoável são necessários várias horas de aquisição.
#  Anderson,Bruno. fev.2020
#=========================================================

import visa
import pylef
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as path
import matplotlib.patches as patches
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

import time
from time import gmtime, strftime

necessarySamples = 500 #number of samples needed to search
numberBins = 100    #number of bins to graph
divisor = 50        #length in which each partial datafile will be splitted
eventsList = [] #list that stores event lists with 2500 poi 'nts
differencesList = [] #list that stores the difference in microseconds of each 2500 point list
readDifferences = [] #list that stores the data saved after the search
pointsList = []

rm = visa.ResourceManager() #list of connected visa resources with PyVisa as a visa
rm.list_resources() #Print resource list
#scope = rm.open_resource('USB0::0x0699::0x0363::C060956::INSTR') #Enter the resource to be connected manually
scope = pylef.TektronixTBS1062() #use the Pylef functions, to handle oscilloscope
scope.start_acquisition() #Start the aquisition of the waveform
scope.ch1.turn_on() #Turn channel on
scope.ch1.set_scale('0.010') #Ch1 10,0mV = 0,010 VOLTS
scope.ch1.set_position(2) #Vertical position for channel 1 must be 2
scope.ch1.set_probe(1) #Voltage probe must be at 1
scope.trigger.set_level(-0.020) #Trigger in -20mV
scope.set_horizontal_scale(1 / 1000000) #Oscilloscope SEC/DIV time 1.00 us = 1e-06
scope.write('HORizontal:MAIn:POSition 0;') #Initial horizontal position 0 default
scope.write('HORizontal:MAIn:POSition 0.00000460;') #Horizontal position with resp''''''''''''''''''''''''''''''''''''''''''''ect to the start of the oscilloscope window
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
print('The program will start the acquisition.')
while len(eventsList) <= necessarySamples:
    pointsList = scope.ch1.acquire_y_raw()
    peaks, _ = find_peaks(-1 * pointsList, height=0)

    if len(peaks) == 2:
        if peaks[0] > 50.0:
            if peaks[1] > 20.0:
                difference = peaks[1] - peaks[0]
                microseconds = difference / 250
                if microseconds > 0.1:
                    epochT1 = time.time()
                    eventsList.append(epochT1)
#                    eventsList.append(pointsList)                              ###
#                    eventsList.append(epochT1)                                 ###
                    differencesList.append(microseconds)
                    print('number of current samples: ', len(eventsList))
                    if len(eventsList) % divisor == 0:
                        filename = str(len(eventsList))+'events_partialData.txt'
                        np.savetxt(filename, np.c_[differencesList, eventsList], fmt='%.10e' , delimiter=", ")
                        _ = plt.hist(differencesList,bins='auto')
                        plt. title('partial histogram with ' + str(len(eventsList)) + ' events')
                        plt.show(block = False)
                        plt.pause(0.01)

"""
stores the list of events in CSV format, 
if you have other files in your directory, do not 
forget to change your name so that it is not replaced
"""
#np.savetxt("EventsList.csv", eventsList, delimiter=",")                        ###
np.savetxt("DifferencesList.csv", differencesList, delimiter=",")              ###
# edited by Bruno Gelli - 05/02/2020
# this new implementation saves the timestamp of the event side by side with the deltaT data in a two column format.

np.savetxt("FullData.csv", np.c_[differencesList, eventsList], fmt='%.10e' , delimiter=", ")

"""
Beginning of the data analysis to find the average life time 
according to the differences of the events found;
"""
nameFile = "DifferencesList.csv" #Name of the file containing the previously saved differences

with open(nameFile, "r") as inp: #systematic reading of the 'CSV' file with the differences in microseconds
    for entry in inp:
        readDifferences.append(float(entry))
    inp.close()

SAMPLE_SIZE = len(readDifferences)



"""
Function definition. Model on which to make the adjustment or fit or fitting
"""
def model_func(x, tau, off, amp): 
    return off + amp * np.exp(-1.0 * x / tau)



"""
Numpy generator, deliver two arrangements. 
The first with the occurrences and the second with the extremes
"""
n, bins = np.histogram(readDifferences, numberBins) #


"""
We eliminate the first BINS, which keep the noise. 
This data must be adjusted, according to the amount of data collected and the number of BINS to be plotted.
For example for the 5000 data, 200 BINS were used and an 'noiseBins' of 8 is added.
"""
noiseBins = 8
n = n[noiseBins:]
bins = bins[noiseBins:]
fig, ax = plt.subplots()


"""
To make histogram graphs according to matplotlib, we get the corners of the rectangles for the histogram.
"""
left = np.array(bins[:-1])
right = np.array(bins[1:])
bottom = np.zeros(len(left))
top = bottom + n
nrects = len(left)


"""
Take the average value of the containers, to build the chart
"""
xdata = (left + right) / 2.0 
""""""

"""
Function to build a compound path
"""
XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T


"""
Get the object path. And we comidify the characteristics of the output.
Get the object pathch out.
"""
barpath = path.Path.make_compound_path_from_polys(XY)

patch = patches.PathPatch(barpath, facecolor='blue', edgecolor='yellow', alpha=0.5)
ax.add_patch(patch)

ax.set_xlim(left[0], right[-1])
ax.set_ylim(bottom.min(), top.max())



"""
curve_fit: the matrix with the "optimal" parameters and a matrix return
"""
popt, pcov = curve_fit(model_func, xdata, n)



"""
Now to the histogram diagram I add the graphs of the theoretical and best fit functions
"""
y_best_fit = np.apply_along_axis(model_func, 0, xdata, popt[0], popt[1], popt[2])

ax.plot(xdata, y_best_fit, 'r-', label='best fit con $f(x) = off + amp \cdot e^{- x / T }$ $\Longrightarrow$ T=%5.4f, off=%5.4f, amp=%5.4f' % tuple(popt), linewidth=2)
ax.legend(loc=1)
ax.set_ylabel('Events')
ax.set_xlabel("Muon Decay Time ($\mu s$)")
ax.set_xlim(left=0.0)

plt.rcParams["figure.figsize"] = (20, 10)
plt.show()
