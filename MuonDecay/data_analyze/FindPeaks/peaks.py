import pandas as pd
import numpy as np
from scipy.signal import find_peaks



#                          .
#==========================================================================================================
def peaks_muon_decay(df, height, slope=-1, first_peak_loc=False):

    Peaks    = pd.DataFrame()
    problems = pd.DataFrame()

    for i in range(df.shape[1]):

        event = df[df.columns[i]]
        x_peaks, _ = find_peaks(slope*event, height=slope*height)

        if len(x_peaks) != 2:
            # raise ValueError(f'the numbers of peaks must be 2 and it found {len(x_peaks)} on {event.name}')
            problems[event.name] = [f'peaks quantity ({len(x_peaks)})']
            continue

        if first_peak_loc != False: #trigger makes us expect the pulse in [80:120]
            if (x_peaks[0] < first_peak_loc - 15) or (x_peaks[0] > first_peak_loc + 15):
                # raise ValueError(f'the first peak of {event.name} is not around the point {first_peak_loc}, but in the instant {x_peaks[0]}')
                problems[event.name] = ['1st peak outrange']
                continue

        y_peaks = event.iloc[x_peaks].tolist()

        peaks = np.append(x_peaks, y_peaks)

        Peaks[event.name] = peaks

    Peaks = Peaks.T
    if Peaks.shape[1] > 0:
        Peaks.columns = ['peak_X0', 'peak_X1', 'peak_Y0', 'peak_Y1']
    else:
        raise ValueError('\nno peaks detected at all...\n\n')

    problems = problems.T
    if problems.shape[1] > 0:
        problems.columns = ['problem']

    return(Peaks, problems)



#                          .
#==========================================================================================================
def peaks_single_muon(df, height, slope=-1, first_peak_loc=False):

    Peaks    = pd.DataFrame()
    problems = pd.DataFrame()

    print(height)

    for i in range(df.shape[1]):

        event = df[df.columns[i]]
        x_peaks, _ = find_peaks(slope*event, height=slope*height)

        if len(x_peaks) != 1:
            # raise ValueError(f'the numbers of peaks must be 1 and it found {len(x_peaks)} on {event.name}')
            problems[event.name] = [f'peaks quantity ({len(x_peaks)})']
            continue

        if first_peak_loc != False: #trigger makes us expect the pulse in [80:120]
            if (x_peaks[0] < first_peak_loc - 15) or (x_peaks[0] > first_peak_loc + 15):
                # raise ValueError(f'the first peak of {event.name} is not around the point {first_peak_loc}, but in the instant {x_peaks[0]}')
                problems[event.name] = ['1st peak outrange']
                continue

        y_peaks = event.iloc[x_peaks].tolist()

        peaks = np.append(x_peaks, y_peaks)

        Peaks[event.name] = peaks

    Peaks = Peaks.T
    if Peaks.shape[1] > 0:
        Peaks.columns = ['peak_X0', 'peak_Y0']
    else:
        raise ValueError('\nno peaks detected at all...\n\n')

    problems = problems.T
    if problems.shape[1] > 0:
        problems.columns = ['problem']

    return(Peaks, problems)


