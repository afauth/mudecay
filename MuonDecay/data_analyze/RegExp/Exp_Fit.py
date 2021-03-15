import pandas as pd
import numpy as np





def fit_function(t, A, tau, C): # função de ajuste exponencial
    return(  A * np.e**(-t/tau) + C  )


def time_difference(df): #peak_X0, peak_X1, peak_Y0, peak_Y1
    '''dataFrame of differences'''
    delta_t = pd.DataFrame(df.columns[1] - df.columns[0], columns=['delta_x']) 
    return(delta_t)


'''
Find bins for a histogram with given x-axis
Basically, retrieve the info of the Seaborn histogram
'''
def bins_centers(x_values , custom_number_of_bins=0): 
    
    if custom_number_of_bins == 0:
        number_of_bins = min(  len( np.histogram_bin_edges(x_values, bins="fd") ), 50  )
    else:
        number_of_bins = custom_number_of_bins
    
    data_entries, bins = np.histogram(x_values , bins=number_of_bins)
    
    dt = bins[1] - bins[0]
    centers = np.array([ bins[i] + dt/2 for i in range(len(bins)-1) ])

    return(centers)


def curve_fit_exponencial(df, height, convert_to_microsec, custom_number_of_bins=0, plot_graph=1, plt_points=0, plt_bars=1, path_to_save='../Documents/data/images/exp_fit_deltaT.png'):

    # _ = pd.DataFrame(   peaks_em_x(df=df, height=height),  columns = ['peak_0', 'peak_1']   )   
    # delta_x = (   _['peak_1']  -  _['peak_0']   )*convert_to_microsec
    # delta_x.name = 'delta_x'
    # #print(f'Total de {len(delta_x)} eventos')
    # #print(delta_x.min(), delta_x.max())
    


    '''
    (b) Coletamos os dados e fazemos plots preliminares, para ir acompanhando os resultados
        Obs.: a variável number_of_bins é o jeito padrão de quantificar quantos bins se tem num histograma
        fonte: https://stackoverflow.com/questions/60512271/how-can-i-extract-the-bins-from-seaborns-kde-distplot-object
    '''
    # if custom_number_of_bins == 0:
    #     number_of_bins = min(  len( np.histogram_bin_edges(delta_x, bins="fd") ), 50  )
    # else:
    #     number_of_bins = custom_number_of_bins
    # data_entries, bins = np.histogram(delta_x , bins=number_of_bins)
    # dt = bins[1] - bins[0]
    # bins_centers       = np.array([ bins[i] + dt/2 for i in range(len(bins)-1) ])

    '''
    (c) Fazemos a regressão pela curve_fit do Scipy
        obs.: É importante dar um valor inicial para os parâmetros, como um chute inicial. 
        Nesse caso, eu apenas chutei os valores mesmo algumas vezes
    '''
    p0 = np.array([ 0.5, 0.1, 1 ]) # initial guess for the parameters: y(t) = A * np.e**(-t/tau) + C
    coeff, cov_coeff = curve_fit(  fit_function , xdata = bins_centers , ydata = data_entries, p0 = p0  )

    '''
    (d) incertezas
    '''
    coeff_error = np.sqrt(np.diag(cov_coeff)) / np.sqrt(number_of_bins - 1) #"np.sqrt(cov) / sqrt(n - 1)"
    
    '''
    (e) Resultado
    '''
    coeff_results = pd.DataFrame( [coeff, coeff_error] ).T
    coeff_results.rename( columns={0:'valor', 1:'incerteza'}, index={ 0:'A', 1:'tau', 2:'C' } , inplace=True )

    '''
    (f) Plot com histograma e regressão da curva
    '''
    fator_unidade = number_of_bins/(delta_x.max()-delta_x.min())
    print(fator_unidade)

    if plot_graph == 1:
            # detalhes
        fig = plt.figure( figsize=(8,6), dpi=85 )
        plt.title('Diferenças de tempo entre os pulsos')
        plt.xlabel(r'Diferença de tempo ($\mu$s)')
        plt.ylabel(r'${\Delta N} \, / \, {\Delta t} \,\,\, (\mu s^{-1})$')
            # plot do histograma
        if plt_bars == 1:
            sns.histplot(delta_x, color='gray', bins=number_of_bins)
            # plot dos centros dos bins
        if plt_points == 1:
            plt.scatter(bins_centers, fator_unidade*data_entries, color = 'black', label='Pontos experimentais')
            # plot da curve_fit
        x = np.linspace(0,10,10000)
        # plt.plot( 
        #     x, fit_function(x, coeff[0], coeff[1], coeff[2]), 
        #     color = 'orange', label='Ajuste exponencial' 
        #         )
        plt.plot( 
            x, fit_function(x, fator_unidade*coeff[0], coeff[1], fator_unidade*coeff[2]), 
            color = 'orange', label='Ajuste exponencial' 
                )
        # plt.text(5, 250, f'Total N$_{{0}}=$ {len(delta_x)} eventos', fontsize=12)
        # plt.text(5, 230, f'${{y(t) = {round(coeff[0],2)} \cdot e^{{-t / {round(coeff[1],2)}}} + {round(coeff[2],2)} }}$', fontsize=12)
    
            # plot teorico: phi(t) = dN(0<=x<=t)/dt = N_0*gamma*e^(-gamma*t)
        # def funcao_teorica(t,N_0,gamma,delta_t):
        #     return( N_0*delta_t*gamma*np.e**(-gamma*t) )
        # plt.plot( 
        #     x, funcao_teorica(t=x, N_0=5555, gamma=1/coeff[1], delta_t=dt), 
        #     color='red', linestyle='dashed', label='Modelo teórico' 
        #         )
        
        plt.legend()
        #plt.savefig(path_to_save)
        return(coeff_results, fig, bins_centers, data_entries)

    else: 
        #print('No figure')
        return(coeff_results, bins_centers, data_entries)