import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as path
import matplotlib.patches as patches
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

"""
Number of bins to graph.
List that stores the data saved after the search
 """
numberBins = 100 
readDifferences = [] 

"""
Beginning of the data analysis to find the average life time 
according to the differences of the events found;
"""
nameFile = "5500_events.csv" #Name of the file containing the previously saved differences

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
