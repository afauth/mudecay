from os import path
from data_analyze.Analyze.assemble import Assemble_MuonDecay, Assemble_SingleMuon
from data_analyze.Plots.plots import plots_MuonDecay, plots_SingleMuon
from data_analyze.CurveFit.Exp_Fit import Curve_Fit_Exponential, Plot_Fit_Graph



Assemble_MuonDecay(path='../documents/data/muon_decay')

plots_MuonDecay(path='../documents/data/muon_decay')

# Curve_Fit_Exponential(xdata=)
