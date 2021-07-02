import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from data_analyze.Analyze.single_muon import convert_charge



def plot_event(event, limits=[0,2500]):

    x = [ i for i in range( event.shape[0] ) ][ limits[0]:limits[1] ]
    y = event[ limits[0]:limits[1] ]
    plt.plot( x, y )


