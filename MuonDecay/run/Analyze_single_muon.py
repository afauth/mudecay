from data_analyze.Analyze.analysis import Analysis_SingleMuon
from data_analyze.Plots.plots import plots_SingleMuon
from data_analyze.Spectrums.convert_integral import convert_charge
from data_analyze.Preliminaries.read_output_file import retrieve_y_to_volts

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

path = 'documents/data/single_muon/'
folder = '1625353737.1067114'


# Analysis_SingleMuon(path+folder)
# plots_SingleMuon(path+folder)

integral = pd.read_csv(path+folder+'/results/integral.csv', index_col=0)
integral.columns = ['integral']

converter = retrieve_y_to_volts(path+folder)

charge = convert_charge(integral, converter)
# print(integral)

sns.histplot(-1*charge)
plt.xlabel('carga (pC)')
plt.ylabel('contagem')
plt.show()


