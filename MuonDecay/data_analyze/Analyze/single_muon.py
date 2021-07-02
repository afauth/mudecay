# #                          Imports
# #==========================================================================================================
import pathlib
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

from data_analyze.Preliminaries.concat_csv_files import concat_csv
from data_analyze.Preliminaries.read_output_file import trigger_acquisition
from data_analyze.Spectrums.integral import simpson_integral_df



#                          .
#==========================================================================================================
def peaks_single_muon(df, height, first_peak_loc=False):

    Peaks    = pd.DataFrame()
    problems = pd.DataFrame()

    for i in range(df.shape[1]):

        event = df[df.columns[i]]
        x_peaks, _ = find_peaks(event, height=height)

        if len(x_peaks) != 1:
            # raise ValueError(f'the numbers of peaks must be 1 and it found {len(x_peaks)} on {event.name}')
            problems[event.name] = ['peaks quantity']
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
    Peaks.columns = ['peak_X0', 'peak_Y0']

    problems = problems.T
    if problems.shape[1] > 0:
        problems.columns = ['problem']

    return(Peaks, problems)



#                          .
#==========================================================================================================
def contours_single_muon(waveform, peak, random_left=10, random_right=15):

    pulses_0 = pd.DataFrame()
    
    for i in range(waveform.shape[1]):
        try:
            event = waveform[waveform.columns[i]]

            peak_X0 = int(peak['peak_X0'][i])

            limits_0 = [ peak_X0-random_left, peak_X0+random_right ]

            pulse_0 = event.iloc[ limits_0[0]:limits_0[1] ].to_list()

            pulses_0[ event.name ] = pulse_0
        except:
            raise ValueError(f'problem on {event.name}')

    return(pulses_0)



#                          .
#==========================================================================================================
def convert_charge(integral):
    
    R = 50 #ohm
    binTime = 4E-3 #micro-sec
    VoltCh  = 100 / 255 #100mV/(256-1)bits

    charge = 1_000*integral*binTime/R #pC

    return(charge)



#                          .
#==========================================================================================================
def Analysis_SingleMuon(folder):
    """
    This function is built to 

    Parameters
    ----------
    folder: string
        This is the main folder that contains the sub_files of the acquisition and the output file.
        Example: '../documents/single_muon/1619201634.9231706'
        Please, note that the '..' is used to acess a parent folder.
    """

    df = concat_csv(path=folder)
    waveform = df[1:] #eliminate the row of the time_epoch data

    baseLine = waveform.iloc[150:].mean().mean() #assume that the peaks occours until x=150; then, the baseLine is the general mean
    trigger, slope = trigger_acquisition(folder) #reads the trigger on the output.txt file; trigger is in mV

    peaks, problems = peaks_single_muon(df=slope*waveform, height=slope*trigger, first_peak_loc=100)
    
    contours = contours_single_muon(waveform=waveform, peak=peaks, random_left=10, random_right=15)
    integral = simpson_integral_df(contours - baseLine)

    pathlib.Path(f"{folder}/results").mkdir(parents=True, exist_ok=True) #create folder to store the results

    peaks.to_csv(f"{folder}/results/peaks.csv")
    problems.to_csv(f"{folder}/results/problems.csv")
    contours.to_csv(f"{folder}/results/contours.csv")
    integral.to_csv(f"{folder}/results/integral.csv")


