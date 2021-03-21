import pandas as pd
import numpy as np
from scipy.signal import find_peaks


#=====================================================================================================
def Find_Peaks_Waveforms(df, height=0, invert_waveform=True):
    
    if invert_waveform == True:
        wvfrs = -1*df
    else:
        wvfrs = df
    
    Peaks = pd.DataFrame()

    for i in range(wvfrs.shape[1]):

        event = wvfrs[wvfrs.columns[i]]
        x_peaks, _ = find_peaks( event, height=height ) #x_peaks is an array
        y_peaks    = event.iloc[x_peaks].tolist()

        peaks = np.append(x_peaks, y_peaks)

        Peaks[wvfrs.columns[i]] = peaks

    Peaks = Peaks.T
    Peaks.columns = ['peak_X0', 'peak_X1', 'peak_Y0', 'peak_Y1']

    return(Peaks) # [event_0, event_1, ..., event_n] X [peak_X0, peak_X1, peak_Y0, peak_Y1]
