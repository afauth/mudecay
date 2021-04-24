from data_analyze.FindPeaks.peaks import Find_Peaks_Waveforms
from data_analyze.Spectrums.contour import contour_arbitrary_df
from data_analyze.Spectrums.integral import integral_rectangle_df, simpson_integral_df, trapeziod_integral_df

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from time import time
from datetime import timedelta



#=====================================================================================================
def Results_Analyze(waveforms, height):
    '''
    waveforms: waveforms DataFrame.
    '''

    # Start time
    time_start = time()

    # Find the peaks
    peaks = Find_Peaks_Waveforms(waveforms=waveforms, height=height)

    # Find the contours
    contours = contour_arbitrary_df(waveforms=waveforms, peaks=peaks)

    # Calculate integrals
    integrals_0 = simpson_integral_df(waveforms=contours[0])
    integrals_1 = simpson_integral_df(waveforms=contours[1])
    integrals = pd.concat([integrals_0, integrals_1], axis=1)
    integrals.columns = ['integrals_0', 'integrals_1']

    # Assemble all the results
    events_filtereds = contours[0].columns # it could be contours[1].columns as well
    df = waveforms[ events_filtereds ]
    results = pd.concat( [peaks.loc[events_filtereds], integrals] , axis=1 )

    # Final time
    time_finish = time()

    #Delta time
    time_delta = time_finish - time_start
    print( timedelta(seconds=time_delta) )

    return(df, results)



#=====================================================================================================
def plots_collection(results, title):

    print(f"{results.shape[0]} events")

    # Main plot
    fig, axes = plt.subplots(ncols=2, nrows=2, figsize=(16,10))
    fig.suptitle(title)
    
    # Fig 1
    sns.histplot(results[['peak_Y0','peak_Y1']], ax=axes[0,0])
    axes[0,0].set_title('Espectro de amplitude; Histograma dos picos')

    # Fig 2
    sns.histplot(results[['integrals_0', 'integrals_1']], ax=axes[0,1])
    axes[0,1].set_title('Espectro de carga; Histograma dos pulsos')

    # Fig 3
    axes[1,0].scatter( x=results['integrals_0'], y=results['peak_Y0'], label='pulse_0' )
    axes[1,0].set_title('Primeiro pulso: Carga X Picos')
    axes[1,0].set_xlabel('Picos')
    axes[1,0].set_ylabel('Carga')
    axes[1,0].legend()

    # Fig 4
    axes[1,1].scatter( x=results['integrals_1'], y=results['peak_Y1'], color='orange', label='pulse_1' )
    axes[1,1].set_title('Segundo pulso: Carga X Picos')
    axes[1,1].set_xlabel('Picos')
    axes[1,1].set_ylabel('Carga')
    axes[1,1].legend()

    plt.show()
