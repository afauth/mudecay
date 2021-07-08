import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks



#                          .
#==========================================================================================================
def contours_single_muon(waveform, peak, random_left=10, random_right=15):

    df = waveform[ peak.index ] 

    contours = pd.DataFrame()
    problems = pd.DataFrame()

    for i in range(df.shape[1]):

        event = df[ df.columns[i] ]
        peak_X0 = int(peak['peak_X0'][i])

        limits_0 = [ peak_X0-random_left, peak_X0+random_right ]
        pulse = event.iloc[ limits_0[0]:limits_0[1] ].to_list()

        if len(pulse) == (random_left + random_right):
            contours[ event.name ] = pulse
        else:
            problems[event.name] = ['contour out of bounds']
 
    problems = problems.T
    if problems.shape[1] > 0:
        problems.columns = ['problem']

    return(contours, problems)



#                          .
#==========================================================================================================
def contours_muon_decay(waveform, peak, random_left=10, random_right=15):

    df = waveform[ peak.index ] 

    contours_0 = pd.DataFrame()
    contours_1 = pd.DataFrame()
    problems = pd.DataFrame()

    for i in range(df.shape[1]):

        event = df[ df.columns[i] ]
        peak_X0 = int(peak['peak_X0'][i])
        peak_X1 = int(peak['peak_X1'][i])

        limits_0 = [ peak_X0-random_left, peak_X0+random_right ]
        limits_1 = [ peak_X1-random_left, peak_X1+random_right ]
        pulse_0  = event.iloc[ limits_0[0]:limits_0[1] ].to_list()
        pulse_1  = event.iloc[ limits_1[0]:limits_1[1] ].to_list()

        if len(pulse_0) == (random_left + random_right) and len(pulse_1) == (random_left + random_right):
            contours_0[ event.name ] = pulse_0
            contours_1[ event.name ] = pulse_1
        else:
            problems[event.name] = [f'contour out of bounds']
 
    problems = problems.T
    if problems.shape[1] > 0:
        problems.columns = ['problem']

    return(contours_0, contours_1, problems)


