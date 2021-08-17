import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from data_analyze.Spectrums.convert_integral import convert_charge, convert_energy
from data_analyze.Preliminaries.read_output_file import retrieve_y_to_volts, convert_y_to_mili_volts


#                          .
#==========================================================================================================
def plots_SingleMuon(path, folder='results', bins='auto'):

    converter = retrieve_y_to_volts(path=path)

    peaks    = pd.read_csv(path+'/'+folder+'/'+'peaks.csv', index_col=0)
    integral = pd.read_csv(path+'/'+folder+'/'+'integral.csv', index_col=0)
    
    peaks_mV = convert_y_to_mili_volts(peaks, converter)
    charge   = -1*convert_charge(integral, converter)

    # Main plot
    fig, axes = plt.subplots(ncols=3, nrows=1, figsize=(30,10))
    fig.suptitle(f'Espectros de pico e carga; {peaks.shape[0]} events', fontsize=18)

    # Fig 1
    sns.histplot( -1*peaks_mV['peak_Y0'], ax=axes[0], color='orange', bins=bins )
    axes[0].set_title(f'Espectro de picos')
    axes[0].set_xlabel('peak (mV)')

    # Fig 2
    sns.histplot( charge, ax=axes[1], color='blue', bins=bins )
    axes[1].set_title(f'Espectro de carga')
    axes[1].set_xlabel('charge (pC)')

    #Fig 3
    axes[2].scatter( charge , -1*peaks_mV['peak_Y0'] , color='green' )
    axes[2].set_title(f'picos X carga')
    axes[2].set_ylabel(f'peaks (mV)')
    axes[2].set_xlabel(f'charge (pC)')

    plt.savefig(path+'/'+folder+'/spectrums.png')

    plot_random_contours_single_muon(path+'/'+folder)



#                          .
#==========================================================================================================
def plots_MuonDecay(path, folder='results', bins='auto'):

    converter = retrieve_y_to_volts(path=path)

    peaks      = -1*pd.read_csv(path+'/'+folder+'/'+'peaks.csv', index_col=0)
    integral_0 = pd.read_csv(path+'/'+folder+'/'+'integral_0.csv', index_col=0)
    integral_1 = pd.read_csv(path+'/'+folder+'/'+'integral_1.csv', index_col=0)

    peaks_mV   = convert_y_to_mili_volts(peaks, converter)
    charge_0   = -1*convert_charge(integral_0, converter)
    charge_1   = -1*convert_charge(integral_1, converter)

    # Main plot
    fig, axes = plt.subplots(ncols=3, nrows=2, figsize=(30,20))
    fig.suptitle(f'Espectros de pico e carga; {peaks_mV.shape[0]} events', fontsize=18)

    # Fig 1: peaks_0
    sns.histplot( peaks_mV['peak_Y0'], ax=axes[0,0], color='orange', bins=bins )
    axes[0,0].set_title(f'Espectro de picos')
    axes[0,0].set_xlabel('peak (mV)')

    # Fig 2: charge_0
    sns.histplot( charge_0, ax=axes[0,1], color='blue', bins=bins )
    axes[0,1].set_title(f'Espectro de carga')
    axes[0,1].set_xlabel('charge (pC)')
    # 'energy (MeV)'

    #Fig 3: charge_0 x peaks_0
    axes[0,2].scatter( charge_0 , peaks_mV['peak_Y0'] , color='green' )
    axes[0,2].set_title(f'picos X energia')
    axes[0,2].set_ylabel(f'peaks (mV)')
    # axes[0,2].set_xlabel(f'charge (pC)')
    axes[0,2].set_xlabel(f'charge (pC)')

    # Fig 4: peaks_1
    sns.histplot( peaks_mV['peak_Y1'], ax=axes[1,0], color='orange', bins=bins )
    axes[1,0].set_title(f'Espectro de picos')
    axes[1,0].set_xlabel('peak (mV)')

    # Fig 5: charge_1
    sns.histplot( charge_1, ax=axes[1,1], color='blue', bins=bins )
    axes[1,1].set_title(f'Espectro de carga')
    # axes[1,1].set_xlabel('charge (pC)')
    axes[1,1].set_xlabel('charge (pC)')

    #Fig 6: charge_1 x peaks_1
    axes[1,2].scatter( charge_1 , peaks_mV['peak_Y1'] , color='green' )
    axes[1,2].set_title(f'picos X energia')
    axes[1,2].set_ylabel(f'peaks (mV)')
    # axes[1,2].set_xlabel(f'charge (pC)')
    axes[1,2].set_xlabel(f'charge (pC)')

    plt.savefig(path+'/'+folder+'/spectrums.png')

    # plot_random_contours_single_muon



#                          .
#==========================================================================================================
def plot_event(event, limits=[0,2500]):

    x = [ i for i in range( event.shape[0] ) ][ limits[0]:limits[1] ]
    y = event[ limits[0]:limits[1] ]
    plt.plot( x, y )



def plot_random_contours_single_muon(path, limit_number=10):

    contours = pd.read_csv(path+'/contours.csv', index_col=0)

    if contours.shape[0] <= limit_number:
        number_of_plots = contours.shape[0]
    else:
        number_of_plots = limit_number

    df = contours.sample(n=number_of_plots, axis=1)

    fig, axes = plt.subplots(ncols=1, nrows=1, figsize=(10,10))
    axes.plot(df)
    plt.savefig(path+'/random_plots.png')



def plot_random_contours_muon_decay(path, folder='results'):

    contours_0 = pd.read_csv(path+'/'+folder+'/'+'contours_0.csv', index_col=0)
    contours_1 = pd.read_csv(path+'/'+folder+'/'+'contours_1.csv', index_col=0)

    if contours_0.shape[0] <= 10:
        number_of_plots = contours_0.shape[0]
    else:
        number_of_plots = 10

    df_0 = contours_0.sample(n=number_of_plots, axis=1)
    df_1 = contours_1.sample(n=number_of_plots, axis=1)

    fig, axes = plt.subplots(ncols=2, nrows=1, figsize=(20,10))
    axes[0].plot(df_0)
    axes[1].plot(df_1)
    plt.savefig(path+'/'+folder+'/random_plots.png')


