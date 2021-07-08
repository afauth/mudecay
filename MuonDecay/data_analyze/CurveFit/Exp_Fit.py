import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# from data_analyze.FindPeaks.peaks



#=====================================================================================================
def Time_Difference(df): #Columns: peak_X0, peak_X1, peak_Y0, peak_Y1
    '''dataFrame of differences'''
    delta_t = pd.DataFrame(df.columns[1] - df.columns[0], columns=['delta_x']) 
    return(delta_t)



#=====================================================================================================
'''
Find bins for a histogram with given x-axis
Basically, retrieve the info of the Seaborn histogram
'''
def Bins_Infos(x_values , number_of_bins=50): 
    
    data_entries, bins_edges = np.histogram(x_values , bins=number_of_bins)
        
    dt = bins_edges[1] - bins_edges[0]
    centers = np.array([ bins_edges[i] + dt/2 for i in range(len(bins_edges)-1) ])

    return(data_entries, bins_edges, centers)



#=====================================================================================================
'''Exponential curve function to make a regression'''
def fit_function(t, A, tau, C):
    return(  A * np.e**(-t/tau) + C  )



#=====================================================================================================
def Curve_Fit_Exponential(xdata, ydata, fit_function=fit_function, p0=np.array([ 0.5, 0.1, 1 ]) ):
    
    '''
    xdata = bins_centers
    ydata = data_entries
    '''
    coeff, cov_coeff = curve_fit(  fit_function, xdata=xdata, ydata=ydata, p0=p0  )

    '''
    Uncertainties: "sqrt(cov) / sqrt(n - 1)"
    '''
    coeff_error = np.sqrt(np.diag(cov_coeff)) / np.sqrt(len(ydata) - 1) 
    
    '''
    Results
    '''
    coeff_results = pd.DataFrame( [coeff, coeff_error] ).T
    coeff_results.rename( columns={0:'value', 1:'error'}, index={ 0:'A', 1:'tau', 2:'C' } , inplace=True )

    '''
    Conversion to micro-seconds
    The scale factor of an histogram is equivalent to the "number_of_bins / total_data_lenght"
    number_of_bins = len(bins_centers) = len(xdata)
    total_data_lenght = "delta_x.max()-delta_x.min()" = 
                      = bins_centers.max() - bins_centers.min() + bins_centers[1] - bins_centers[0] =
                      = xdata.max() - xdata.min() + xdata[1] - xdata[0]

    '''
    scale_factor = len(xdata) / (xdata.max() - xdata.min() + xdata[1] - xdata[0])
    #print(fator_unidade)

    return(coeff_results, scale_factor)



#=====================================================================================================
def Plot_Fit_Graph(xdata, ydata, coeff, conversionScale=0, plotBars=False):

    '''
    xdata = bins_centers
    ydata = data_entries
    coeff = coeff_results --> DataFrame[A, tau, C]
    conversionScale = 0 if you don't want to convert or "conversionScale" if you specify
    '''

    '''Convert if required'''
    if conversionScale != 0:
        xdata *= conversionScale
        ydata *= conversionScale 
        coeff[coeff.columns[0]][[0,2]] *= conversionScale #"value" column; "A" and "C" constants

    '''Details'''
    fig, ax = plt.figure( figsize=(8,6), dpi=100 )
    ax.set_title('Diferenças de tempo entre os pulsos', fontsize=20)
    ax.set_ylabel(r'${\Delta N} \, / \, {\Delta t} \,\,\, (\mu s^{-1})$', fontsize=16)
    ax.set_xlabel(r'Diferença de tempo ($\mu$s)', fontsize=16)

    '''Histogram plot'''
    if plotBars == True:
        #sns.histplot(x_data, color='gray', bins=number_of_bins)
        raise NotImplementedError

    '''Bins centers (a.k.a. points) plot'''
    plt.scatter(
        x=xdata, 
        y=ydata, 
        color='black',
        label='Pontos experimentais'
    )
    
    '''Plot curve fit'''
    x = np.linspace(0,10,10000)
    plt.plot( 
        x, 
        fit_function( x, *coeff[coeff.columns[0]] ),
        color='orange', 
        label='Ajuste exponencial' 
        )
        
    plt.legend()    

    return(fig)        




#=====================================================================================================
# def curve_fit_exponencial(df, height, convert_to_microsec, custom_number_of_bins=0, plot_graph=1, plt_points=0, plt_bars=1, path_to_save='../Documents/data/images/exp_fit_deltaT.png'):

#     # _ = pd.DataFrame(   peaks_em_x(df=df, height=height),  columns = ['peak_0', 'peak_1']   )   
#     # delta_x = (   _['peak_1']  -  _['peak_0']   )*convert_to_microsec
#     # delta_x.name = 'delta_x'
#     # #print(f'Total de {len(delta_x)} eventos')
#     # #print(delta_x.min(), delta_x.max())
    


#     '''
#     (b) Coletamos os dados e fazemos plots preliminares, para ir acompanhando os resultados
#         Obs.: a variável number_of_bins é o jeito padrão de quantificar quantos bins se tem num histograma
#         fonte: https://stackoverflow.com/questions/60512271/how-can-i-extract-the-bins-from-seaborns-kde-distplot-object
#     '''
#     # if custom_number_of_bins == 0:
#     #     number_of_bins = min(  len( np.histogram_bin_edges(delta_x, bins="fd") ), 50  )
#     # else:
#     #     number_of_bins = custom_number_of_bins
#     # data_entries, bins = np.histogram(delta_x , bins=number_of_bins)
#     # dt = bins[1] - bins[0]
#     # bins_centers       = np.array([ bins[i] + dt/2 for i in range(len(bins)-1) ])

#     '''
#     (c) Fazemos a regressão pela curve_fit do Scipy
#         obs.: É importante dar um valor inicial para os parâmetros, como um chute inicial. 
#         Nesse caso, eu apenas chutei os valores mesmo algumas vezes
#     '''
#     # p0 = np.array([ 0.5, 0.1, 1 ]) # initial guess for the parameters: y(t) = A * np.e**(-t/tau) + C
#     # coeff, cov_coeff = curve_fit(  fit_function , xdata = bins_centers , ydata = data_entries, p0 = p0  )

#     # '''
#     # (d) incertezas
#     # '''
#     # coeff_error = np.sqrt(np.diag(cov_coeff)) / np.sqrt(number_of_bins - 1) #"np.sqrt(cov) / sqrt(n - 1)"
    
#     # '''
#     # (e) Resultado
#     # '''
#     # coeff_results = pd.DataFrame( [coeff, coeff_error] ).T
#     # coeff_results.rename( columns={0:'valor', 1:'incerteza'}, index={ 0:'A', 1:'tau', 2:'C' } , inplace=True )

#     # '''
#     # (f) Plot com histograma e regressão da curva
#     # '''
#     # fator_unidade = number_of_bins/(delta_x.max()-delta_x.min())
#     # print(fator_unidade)

#     if plot_graph == 1:
#             # detalhes
#         fig = plt.figure( figsize=(8,6), dpi=85 )
#         plt.title('Diferenças de tempo entre os pulsos')
#         plt.xlabel(r'Diferença de tempo ($\mu$s)')
#         plt.ylabel(r'${\Delta N} \, / \, {\Delta t} \,\,\, (\mu s^{-1})$')
#             # plot do histograma
#         if plt_bars == 1:
#             sns.histplot(delta_x, color='gray', bins=number_of_bins)
#             # plot dos centros dos bins
#         if plt_points == 1:
#             plt.scatter(bins_centers, fator_unidade*data_entries, color = 'black', label='Pontos experimentais')
#             # plot da curve_fit
#         x = np.linspace(0,10,10000)
#         # plt.plot( 
#         #     x, fit_function(x, coeff[0], coeff[1], coeff[2]), 
#         #     color = 'orange', label='Ajuste exponencial' 
#         #         )
#         plt.plot( 
#             x, fit_function(x, fator_unidade*coeff[0], coeff[1], fator_unidade*coeff[2]), 
#             color = 'orange', label='Ajuste exponencial' 
#                 )
#         # plt.text(5, 250, f'Total N$_{{0}}=$ {len(delta_x)} eventos', fontsize=12)
#         # plt.text(5, 230, f'${{y(t) = {round(coeff[0],2)} \cdot e^{{-t / {round(coeff[1],2)}}} + {round(coeff[2],2)} }}$', fontsize=12)
    
#             # plot teorico: phi(t) = dN(0<=x<=t)/dt = N_0*gamma*e^(-gamma*t)
#         # def funcao_teorica(t,N_0,gamma,delta_t):
#         #     return( N_0*delta_t*gamma*np.e**(-gamma*t) )
#         # plt.plot( 
#         #     x, funcao_teorica(t=x, N_0=5555, gamma=1/coeff[1], delta_t=dt), 
#         #     color='red', linestyle='dashed', label='Modelo teórico' 
#         #         )
        
#         plt.legend()
#         #plt.savefig(path_to_save)
#         return(coeff_results, fig, bins_centers, data_entries)

#     else: 
#         #print('No figure')
#         return(coeff_results, bins_centers, data_entries)