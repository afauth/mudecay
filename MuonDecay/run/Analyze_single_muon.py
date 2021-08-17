from data_analyze.Analyze.analysis import Analysis_SingleMuon
from data_analyze.Plots.plots import plots_SingleMuon

path = 'documents/data/single_muon/'
folder = '1629221080.9279172'


Analysis_SingleMuon(path+folder)
plots_SingleMuon(path+folder)
