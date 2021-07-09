import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from data_analyze.Spectrums.convert_integral import convert_charge


#                          .
#==========================================================================================================
def plots_SingleMuon(path, folder='results', bins='auto'):

    peaks    = pd.read_csv(path+'/'+folder+'/'+'peaks.csv', index_col=0)
    integral = pd.read_csv(path+'/'+folder+'/'+'integral.csv', index_col=0)
    charge   = convert_charge(integral)

    # Main plot
    fig, axes = plt.subplots(ncols=3, nrows=1, figsize=(30,10))
    fig.suptitle(f'Espectros de pico e carga; {peaks.shape[0]} events', fontsize=18)

    # Fig 1
    sns.histplot( peaks['peak_Y0'], ax=axes[0], color='orange', bins=bins )
    axes[0].set_title(f'Espectro de picos')
    axes[0].set_xlabel('peak (mV)')

    # Fig 2
    sns.histplot( -1*charge, ax=axes[1], color='blue', bins=bins )
    axes[1].set_title(f'Espectro de carga')
    axes[1].set_xlabel('charge (pC)')

    #Fig 3
    axes[2].scatter( -1*charge , peaks['peak_Y0'] , color='green' )
    axes[2].set_title(f'picos X carga')
    axes[2].set_ylabel(f'peaks (mV)')
    axes[2].set_xlabel(f'charge (pC)')

    plt.savefig(path+'/'+folder+'/spectrums.png')



#                          .
#==========================================================================================================
def plots_MuonDecay(path, folder='results', bins='auto'):

    peaks      = pd.read_csv(path+'/'+folder+'/'+'peaks.csv', index_col=0)
    integral_0 = pd.read_csv(path+'/'+folder+'/'+'integral_0.csv', index_col=0)
    integral_1 = pd.read_csv(path+'/'+folder+'/'+'integral_1.csv', index_col=0)
    charge_0   = convert_charge(integral_0)
    charge_1   = convert_charge(integral_1)

    # Main plot
    fig, axes = plt.subplots(ncols=3, nrows=2, figsize=(30,20))
    fig.suptitle(f'Espectros de pico e carga; {peaks.shape[0]} events', fontsize=18)

    # Fig 1: peaks_0
    sns.histplot( peaks['peak_Y0'], ax=axes[0,0], color='orange', bins=bins )
    axes[0,0].set_title(f'Espectro de picos')
    axes[0,0].set_xlabel('peak (mV)')

    # Fig 2: charge_0
    sns.histplot( -1*charge_0, ax=axes[0,1], color='blue', bins=bins )
    axes[0,1].set_title(f'Espectro de carga')
    axes[0,1].set_xlabel('charge (pC)')

    #Fig 3: charge_0 x peaks_0
    axes[0,2].scatter( -1*charge_0 , peaks['peak_Y0'] , color='green' )
    axes[0,2].set_title(f'picos X carga')
    axes[0,2].set_ylabel(f'peaks (mV)')
    axes[0,2].set_xlabel(f'charge (pC)')

    # Fig 4: peaks_1
    sns.histplot( peaks['peak_Y1'], ax=axes[1,0], color='orange', bins=bins )
    axes[1,0].set_title(f'Espectro de picos')
    axes[1,0].set_xlabel('peak (mV)')

    # Fig 5: charge_1
    sns.histplot( -1*charge_1, ax=axes[1,1], color='blue', bins=bins )
    axes[1,1].set_title(f'Espectro de carga')
    axes[1,1].set_xlabel('charge (pC)')

    #Fig 6: charge_1 x peaks_1
    axes[1,2].scatter( -1*charge_1 , peaks['peak_Y1'] , color='green' )
    axes[1,2].set_title(f'picos X carga')
    axes[1,2].set_ylabel(f'peaks (mV)')
    axes[1,2].set_xlabel(f'charge (pC)')

    plt.savefig(path+'/'+folder+'/spectrums.png')



#                          .
#==========================================================================================================
def plot_event(event, limits=[0,2500]):

    x = [ i for i in range( event.shape[0] ) ][ limits[0]:limits[1] ]
    y = event[ limits[0]:limits[1] ]
    plt.plot( x, y )


