import re
import numpy as np
import pyvisa
from Configs import cfg_scope as config
from time import time, ctime, sleep
from datetime import timedelta



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

rm = pyvisa.ResourceManager()                 # Calling PyVisa library
scope = rm.open_resource(str(config.ScopeID)) # Connecting via USB
