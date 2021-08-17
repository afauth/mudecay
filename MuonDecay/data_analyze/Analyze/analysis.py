# #                          Imports
# #==========================================================================================================
import pathlib
import pandas as pd

from data_analyze.Preliminaries.concat_csv_files import concat_csv
from data_analyze.Preliminaries.read_output_file import trigger_acquisition, retrieve_y_to_volts
from data_analyze.Spectrums.integral import simpson_integral_df
from acquisition.DataAcquisition.Conversion_Values import convert_y_to_units, trigger_slope_value

from data_analyze.FindPeaks.peaks import peaks_single_muon, peaks_muon_decay
from data_analyze.Spectrums.contours import contours_single_muon, contours_muon_decay


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

    print('\n============\nAnalysis Single Muon...\n')

    '''
    Concatenate all sub-csv files
    '''
    df = concat_csv(path=folder)
    waveform = df[1:] #eliminate the row of the time_epoch data

    '''
    Retrieve base line and trigger, for the analysis
    '''
    baseLine = waveform.iloc[:130].mean().mean() #assume that the peaks occours until x=150; then, the baseLine is the general mean
    
    print(baseLine)
    
    trigger_in_mV, slope_string = trigger_acquisition(folder) #reads the trigger on the output.txt file; trigger is in mV

    converter = retrieve_y_to_volts(folder)

    '''Convert trigger to units and slope to a number'''
    trigger_in_units = convert_y_to_units(trigger_in_mV, converter)
    slope_number     = trigger_slope_value(slope_string)

    '''
    Find peaks and problems; save to csv
    '''
    peaks, problems_peaks = peaks_single_muon(df=waveform, height=trigger_in_units, slope=slope_number, first_peak_loc=100)
    
    pathlib.Path(f"{folder}/results").mkdir(parents=True, exist_ok=True) #create folder to store the results
    peaks.to_csv(f"{folder}/results/peaks.csv")
    problems_peaks.to_csv(f"{folder}/results/problems.csv") #saves only the peaks problem, in case of unexpected error

    '''
    Find contours, problems and calculate integrals; save to csv
    '''
    contours, problems_contour = contours_single_muon(waveform=waveform, peak=peaks, random_left=10, random_right=15)
    integral = simpson_integral_df(contours - baseLine)
    
    contours.to_csv(f"{folder}/results/contours.csv")
    integral.to_csv(f"{folder}/results/integral.csv")

    '''
    Concat both problem-catchers in one single csv file; rewrite previous csv file 
    '''
    problems = pd.concat([problems_peaks, problems_contour])
    problems.to_csv(f"{folder}/results/problems.csv")
    
    print('\nending analysis...\n============\n')


#                          .
#==========================================================================================================
def Analysis_MuonDecay(folder):
    """
    This function is built to 

    Parameters
    ----------
    folder: string
        This is the main folder that contains the sub_files of the acquisition and the output file.
        Example: '../documents/single_muon/1619201634.9231706'
        Please, note that the '..' is used to acess a parent folder.
    """

    '''
    Concatenate all sub-csv files
    '''
    df = concat_csv(path=folder)
    waveform = df[1:] #eliminate the row of the time_epoch data

    '''
    Retrieve base line and trigger, for the analysis
    '''
    baseLine = waveform.iloc[:130].mean().mean() #assume that the peaks occours until x=150; then, the baseLine is the general mean
        
    trigger_in_mV, slope_string = trigger_acquisition(folder) #reads the trigger on the output.txt file; trigger is in mV

    converter = retrieve_y_to_volts(folder)

    '''Convert trigger to units and slope to a number'''
    trigger_in_units = convert_y_to_units(trigger_in_mV, converter)
    slope_number     = trigger_slope_value(slope_string)

    '''
    Find peaks and problems; save to csv
    '''
    peaks, problems_peaks = peaks_muon_decay(df=waveform, height=trigger_in_units, slope=slope_number, first_peak_loc=100)
    
    pathlib.Path(f"{folder}/results").mkdir(parents=True, exist_ok=True) #create folder to store the results
    peaks.to_csv(f"{folder}/results/peaks.csv")
    problems_peaks.to_csv(f"{folder}/results/problems.csv") #saves only the peaks problem, in case of unexpected error

    '''
    Find contours, problems and calculate integrals; save to csv
    '''
    contours_0, contours_1, problems_contour = contours_muon_decay(waveform=waveform, peak=peaks, random_left=10, random_right=15)
    integral_0 = simpson_integral_df(contours_0 - baseLine)
    integral_1 = simpson_integral_df(contours_1 - baseLine)
    
    contours_0.to_csv(f"{folder}/results/contours_0.csv")
    integral_0.to_csv(f"{folder}/results/integral_0.csv")
    contours_1.to_csv(f"{folder}/results/contours_1.csv")
    integral_1.to_csv(f"{folder}/results/integral_1.csv")

    '''
    Concat both problem-catchers in one single csv file; rewrite previous csv file 
    '''
    problems = pd.concat([problems_peaks, problems_contour])
    problems.to_csv(f"{folder}/results/problems.csv")



