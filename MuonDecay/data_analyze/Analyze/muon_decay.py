# # #                          Imports
# # #==========================================================================================================
# import pathlib
# import seaborn as sns
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.signal import find_peaks

# from data_analyze.Preliminaries.concat_csv_files import concat_csv
# from data_analyze.Preliminaries.read_output_file import trigger_acquisition
# from data_analyze.Spectrums.integral import simpson_integral_df



# #                          .
# #==========================================================================================================
# def peaks_muon_decay(df, height, first_peak_loc=False):

#     Peaks    = pd.DataFrame()
#     problems = pd.DataFrame()

#     for i in range(df.shape[1]):

#         event = df[df.columns[i]]
#         x_peaks, _ = find_peaks(event, height=height)

#         if len(x_peaks) != 2:
#             # raise ValueError(f'the numbers of peaks must be 2 and it found {len(x_peaks)} on {event.name}')
#             problems[event.name] = [f'peaks quantity ({len(x_peaks)})']
#             continue

#         if first_peak_loc != False: #trigger makes us expect the pulse in [80:120]
#             if (x_peaks[0] < first_peak_loc - 15) or (x_peaks[0] > first_peak_loc + 15):
#                 # raise ValueError(f'the first peak of {event.name} is not around the point {first_peak_loc}, but in the instant {x_peaks[0]}')
#                 problems[event.name] = ['1st peak outrange']
#                 continue

#         y_peaks = event.iloc[x_peaks].tolist()

#         peaks = np.append(x_peaks, y_peaks)

#         Peaks[event.name] = peaks

#     Peaks = Peaks.T
#     if Peaks.shape[1] > 0:
#         Peaks.columns = ['peak_X0', 'peak_X1', 'peak_Y0', 'peak_Y1']
#     else:
#         raise('no peaks detected at all...\n\n')

#     problems = problems.T
#     if problems.shape[1] > 0:
#         problems.columns = ['problem']

#     return(Peaks, problems)



# #                          .
# #==========================================================================================================
# def contours_muon_decay(waveform, peak, random_left=10, random_right=15):

#     df = waveform[ peak.index ] 

#     contours_0 = pd.DataFrame()
#     contours_1 = pd.DataFrame()
#     problems = pd.DataFrame()

#     for i in range(df.shape[1]):

#         event = df[ df.columns[i] ]
#         peak_X0 = int(peak['peak_X0'][i])
#         peak_X1 = int(peak['peak_X1'][i])

#         limits_0 = [ peak_X0-random_left, peak_X0+random_right ]
#         limits_1 = [ peak_X1-random_left, peak_X1+random_right ]
#         pulse_0  = event.iloc[ limits_0[0]:limits_0[1] ].to_list()
#         pulse_1  = event.iloc[ limits_1[0]:limits_1[1] ].to_list()

#         if len(pulse_0) == (random_left + random_right) and len(pulse_1) == (random_left + random_right):
#             contours_0[ event.name ] = pulse_0
#             contours_1[ event.name ] = pulse_1
#         else:
#             problems[event.name] = [f'contour out of bounds']
 
#     problems = problems.T
#     if problems.shape[1] > 0:
#         problems.columns = ['problem']

#     return(contours_0, contours_1, problems)



# #                          .
# #==========================================================================================================
# def Analysis_MuonDecay(folder):
#     """
#     This function is built to 

#     Parameters
#     ----------
#     folder: string
#         This is the main folder that contains the sub_files of the acquisition and the output file.
#         Example: '../documents/single_muon/1619201634.9231706'
#         Please, note that the '..' is used to acess a parent folder.
#     """

#     '''
#     Concatenate all sub-csv files
#     '''
#     df = concat_csv(path=folder)
#     waveform = df[1:] #eliminate the row of the time_epoch data

#     '''
#     Retrieve base line and trigger, for the analysis
#     '''
#     baseLine = waveform.iloc[150:].mean().mean() #assume that the peaks occours until x=150; then, the baseLine is the general mean
#     trigger, slope = trigger_acquisition(folder) #reads the trigger on the output.txt file; trigger is in mV

#     '''
#     Find peaks and problems; save to csv
#     '''
#     peaks, problems_peaks = peaks_muon_decay(df=slope*waveform, height=slope*trigger, first_peak_loc=100)
    
#     pathlib.Path(f"{folder}/results").mkdir(parents=True, exist_ok=True) #create folder to store the results
#     peaks.to_csv(f"{folder}/results/peaks.csv")
#     problems_peaks.to_csv(f"{folder}/results/problems.csv") #saves only the peaks problem, in case of unexpected error

#     '''
#     Find contours, problems and calculate integrals; save to csv
#     '''
#     contours_0, contours_1, problems_contour = contours_muon_decay(waveform=waveform, peak=peaks, random_left=10, random_right=15)
#     integral_0 = simpson_integral_df(contours_0 - baseLine)
#     integral_1 = simpson_integral_df(contours_1 - baseLine)
    
#     contours_0.to_csv(f"{folder}/results/contours_0.csv")
#     integral_0.to_csv(f"{folder}/results/integral_0.csv")
#     contours_1.to_csv(f"{folder}/results/contours_1.csv")
#     integral_1.to_csv(f"{folder}/results/integral_1.csv")

#     '''
#     Concat both problem-catchers in one single csv file; rewrite previous csv file 
#     '''
#     problems = pd.concat([problems_peaks, problems_contour])
#     problems.to_csv(f"{folder}/results/problems.csv")

    

# #                          .
# #==========================================================================================================
# def convert_charge(integral):
    
#     R = 50 #ohm
#     binTime = 4E-3 #micro-sec
#     VoltCh  = 100 / 255 #100mV/(256-1)bits

#     charge = 1_000*integral*binTime/R #pC

#     return(charge)



# #                          .
# #==========================================================================================================
# def plots_MuonDecay(path, folder='results', bins='auto'):

#     peaks      = pd.read_csv(path+'/'+folder+'/'+'peaks.csv', index_col=0)
#     integral_0 = pd.read_csv(path+'/'+folder+'/'+'integral_0.csv', index_col=0)
#     integral_1 = pd.read_csv(path+'/'+folder+'/'+'integral_1.csv', index_col=0)
#     charge_0   = convert_charge(integral_0)
#     charge_1   = convert_charge(integral_1)

#     # Main plot
#     fig, axes = plt.subplots(ncols=3, nrows=2, figsize=(30,20))
#     fig.suptitle(f'Espectros de pico e carga; {peaks.shape[0]} events', fontsize=18)

#     # Fig 1: peaks_0
#     sns.histplot( peaks['peak_Y0'], ax=axes[0,0], color='orange', bins=bins )
#     axes[0,0].set_title(f'Espectro de picos')
#     axes[0,0].set_xlabel('peak (mV)')

#     # Fig 2: charge_0
#     sns.histplot( -1*charge_0, ax=axes[0,1], color='blue', bins=bins )
#     axes[0,1].set_title(f'Espectro de carga')
#     axes[0,1].set_xlabel('charge (pC)')

#     #Fig 3: charge_0 x peaks_0
#     axes[0,2].scatter( -1*charge_0 , peaks['peak_Y0'] , color='green' )
#     axes[0,2].set_title(f'picos X carga')
#     axes[0,2].set_ylabel(f'peaks (mV)')
#     axes[0,2].set_xlabel(f'charge (pC)')

#     # Fig 4: peaks_1
#     sns.histplot( peaks['peak_Y1'], ax=axes[1,0], color='orange', bins=bins )
#     axes[1,0].set_title(f'Espectro de picos')
#     axes[1,0].set_xlabel('peak (mV)')

#     # Fig 5: charge_1
#     sns.histplot( -1*charge_1, ax=axes[1,1], color='blue', bins=bins )
#     axes[1,1].set_title(f'Espectro de carga')
#     axes[1,1].set_xlabel('charge (pC)')

#     #Fig 6: charge_1 x peaks_1
#     axes[1,2].scatter( -1*charge_1 , peaks['peak_Y1'] , color='green' )
#     axes[1,2].set_title(f'picos X carga')
#     axes[1,2].set_ylabel(f'peaks (mV)')
#     axes[1,2].set_xlabel(f'charge (pC)')

#     plt.savefig(path+'/'+folder+'/spectrums.png')


