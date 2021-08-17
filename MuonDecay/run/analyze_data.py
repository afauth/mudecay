from data_analyze.Analyze.analysis import Analysis_MuonDecay, Analysis_SingleMuon
from data_analyze.Plots.plots import plots_MuonDecay, plots_SingleMuon
import os



def analyze_folders_muondecay(path='documents/data/muon_decay'):

    folders_muondecay = os.listdir(path)

    for i in range( len(folders_muondecay) ):
        folder = f'{path}/{folders_muondecay[i]}'
        Analysis_MuonDecay(folder)
        plots_MuonDecay(folder)


def analyze_folders_singlemuon(path='documents/data/single_muon'):
    
    folders_singlemuon = os.listdir(path)

    for i in range( len(folders_singlemuon) ):
        folder = f'{path}/{folders_singlemuon[i]}'
        Analysis_SingleMuon(folder)
        plots_SingleMuon(folder)


analyze_folders_muondecay()

# analyze_folders_singlemuon()


