import pandas as pd
import numpy as np



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
def convert_energy(integral, single_muon_energy_MeV=1000, single_muon_charge_pC=15.5725):

    ratio_MeV_per_pC = single_muon_energy_MeV / single_muon_charge_pC # MeV/pC
    
    charge_in_pC = convert_charge(integral=integral)

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


