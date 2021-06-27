import re
import numpy as np
import pyvisa
import matplotlib.pyplot as plt
from acquisition.Configs import cfg_scope as config
from time import time, ctime, sleep
from datetime import timedelta
from acquisition.DataAcquisition.Conversion_Values import convert_y_to_volts
from acquisition.DataAcquisition.Conversion_Values import units_conversion_parameters, convert_y_to_units


def y_values(oscilloscope):
    start = time()
    y = np.array(  re.split('\n|,|:CURVE ' , oscilloscope.query('CURVe?'))[1:-1]  ,  float  ) #Selecting the essential part on the string
    finish = time()
    print(f'Time: {timedelta(seconds=finish - start)}')
    return(y)

def y_values_ascii(oscilloscope):
    start = time()
    y = oscilloscope.query_ascii_values('CURVe?')
    finish = time()
    print(f'Time: {timedelta(seconds=finish - start)}')
    return(y)

def plot_values(oscilloscope):
    y = oscilloscope.query_ascii_values('CURVe?')
    x = [i for i in range(len(y))]
    converter = units_conversion_parameters(oscilloscope=scope)
    event = convert_y_to_volts(y, converter)
    print(event)
    plt.plot(x, event)
    plt.show()

rm = pyvisa.ResourceManager()                 # Calling PyVisa library
scope = rm.open_resource(str(config.ScopeID)) # Connecting via USB
