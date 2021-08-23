import pandas as pd
import numpy as np

# from data_analyze.Preliminaries.read_output_file import convert_y_to_volts

#                          .
#==========================================================================================================
def convert_charge(integral, converter_df, number_of_points=2500):

    R = 50 #ohm
    binTime = 4E-3 # in micro-seconds; 10 micro-sec / 2500 points
    # VoltCh  = 100 / 255 #100mV/(256-1)bits

    integral_in_mV = number_of_points*converter_df['y_zero'][0] + converter_df['y_mult'][0]*( integral - number_of_points*converter_df['y_off'][0] )
    charge = 1_000*integral_in_mV*binTime/R #pC: "mV * micro-sec * 1000/1000 = pico-coulombs"

    return(charge) #pC



#                          .
#==========================================================================================================
def convert_energy(integral, converter_df, single_muon_energy_MeV=1000, single_muon_charge_pC=15.5725):

    single_muon_energy_MeV = 1.032*2.297*10*1.09 #density*energy_cm^2_per_gram*lenght*conversion_factor

    ratio_MeV_per_pC = single_muon_energy_MeV / single_muon_charge_pC # MeV/pC
    
    charge_in_pC = convert_charge(integral=integral, converter_df=converter_df)

    energy = ratio_MeV_per_pC*charge_in_pC

    return(energy)



#                          .
#==========================================================================================================
def find_charge_single_muon(path='../documents/data/single_muon/1625353737.1067114/results', file='integral.csv', number_of_bins=100):

    integrals = pd.read_csv(f'{path}/{file}', index_col=0)
    charge    = convert_charge(integral=-1*integrals)

    values = charge[charge.columns[0]]
    bins   = np.linspace( values.min(), values.max(), number_of_bins+1 )

    histogram = pd.cut( values, bins ).value_counts()

    interval  = histogram.index[0]
    max_value = (interval.left + interval.right) / 2

    histogram = histogram.sort_index()

    return( histogram , max_value )


