#Imports

import pandas  as pd
import seaborn as sns
import numpy   as np
import matplotlib.pyplot as plt
from scipy.signal    import find_peaks
from scipy.integrate import simps, trapz
from scipy.optimize  import curve_fit


###################################################################################################################
#1. Picos


## 1.1.
def peak_finder(series, height): # peak_finder se aplica em data frames com valores do eixo y    
    #print('= Chamando funcao: peak_finder...')
    '''
    Auxilia a encontrar todos os picos de uma waveform. No caso, encontra dois picos.
    Essa função retorna os valores no eixo x
    '''    
    # get the actual peaks
    peaks, _ = find_peaks( (-1)*series, height = height ) # height é um parâmetro decidido
    
    return(peaks)


## 1.2.
def peaks_em_x(df, height):
    '''
    Esse loop cria e checa se existem erros na obtenção dos picos através da função peak-finder, quando peaks != 2
    '''
    
    peaks_em_x = []
    counter = 0
    
    for i in range(df.shape[1]):
        evento = df[ df.columns[i] ]
        _ = peak_finder(evento, height = height)
        if len(_) != 2:
            print(f'problema no {evento.name} com tamanho = {len(_)} e picos em {_}')
            counter += 1
        peaks_em_x.append(_)

    print(f'\nloop finalizado com {counter} erros')

    return(peaks_em_x)


## 1.3.
def peak_finder_xy(series, height): 
    '''
    Essa função utiliza a peak_finder e já retorna os dados como uma Series com os valores em x e y de cada pico
    '''
    __ = peak_finder(series, height = height)
    
    return(series.iloc[__])


## 1.4.
def peaks_em_xy(df, height):
    peaks_em_xy = pd.Series([])

    for i in range( df.shape[1] ):
        evento = df[ df.columns[i] ]
        _ = peak_finder_xy(evento, height = height)
        peaks_em_xy = pd.concat([  peaks_em_xy, _  ])

    if len(peaks_em_xy) != 2*(df.shape[1] ): # se ele reconhe algo diferente de dois picos por waveform:
        print(f'existe um erro nos picos, pois aparece(m) {len(peaks_em_xy) - 2*(df.shape[1] )} pico(s) a mais')
    else:
        print('não foram detectados problemas na quantidade de picos')

    peaks_em_xy = pd.DataFrame(peaks_em_xy).reset_index()
    peaks_em_xy.columns = ['x', 'y']

    return(peaks_em_xy)


##1.5. 
def peaks_divididos_01(df, height):
    _ = peaks_em_xy(df = df, height = height)
    peaks_0,   peaks_1   =   _.query('index % 2 == 0'),   _.query('index % 2 != 0')
    return(peaks_0, peaks_1)






###################################################################################################################
#2

##2.1.
def derivada_x(s): # insira uma series na entrada; o valor retornado está em coordenadas do eixo x
    '''
    Encontra as diferenças entre elementos lado-a-lado. Serve para avaliar quando estamos começando ou terminando um pulso.
    '''
    VA_derivada_baseLine = 5  #   flutuação/amplitude máxima da base-line;
                              #   valor arbirtrário para saber se o número em questão está fora da 
                              # base-line; não é exatamente a derivada
    _ = []
    for i in range( len(s) - 1 ): # i = index da series
        if abs(s[i] - s[i+1]) > VA_derivada_baseLine:
            _.append(i) 
        
    return (_) # o valor retornado está em coordenadas do eixo x





###################################################################################################################
#3. Contornos

##3.1.
def contorno_limite_derivada(series, VA_1, VA_2, height): # recebe uma Series do pandas para começar
    
    
    '''
    Define um recorte de onde se deve buscar um pulso e os seus delimitadores
    VA_1 e VA_2 são variáveis arbitrárias para definir a largura do pulso 
    '''
    

    peak = peak_finder(series, height = height) # encontrar os picos da waveform
    
    s1 = series[ (peak[0] - VA_1):(peak[0] + VA_2) ] # recortar envolta dos picos
    s2 = series[ (peak[1] - VA_1):(peak[1] + VA_2) ]
    
    df1 = pd.DataFrame( dict(s1 = s1) ).reset_index() # cria um Data Frame com os valores do recorte
    df1.columns = ['time', 's1']                      # renomeia a coluna do data frame
    df2 = pd.DataFrame( dict(s1 = s2) ).reset_index()
    df2.columns = ['time', 's2']
    
    
    '''
    Calcular a "derivada" em cada ponto no entorno, para saber os limitantes do pulso
    Ao terminar, retornar o data frame que contem os valores limitantes do contorno do pulso
    '''  

    indexLim_1 = derivada_x( df1['s1'] ) # índices limitantes
    indexLim_2 = derivada_x( df2['s2'] )
    
    # redefine os valores para apenas os limitantes do data frame
    df1 = df1.iloc[    [  indexLim_1[0], indexLim_1[-1]  ]    ] 
    df2 = df2.iloc[    [  indexLim_2[0], indexLim_2[-1]  ]    ] 
    
    # print(df2) # series marcada pelas colunas 
    
    
    # da Series original, temos agora o contorno do pulso
    s1 = series[ df1['time'].iloc[0] : df1['time'].iloc[1]+1 ] # soma 1 para incluir o último termo
    s2 = series[ df2['time'].iloc[0] : df2['time'].iloc[1]+1 ] 
    
    # print(s2)
    
    pulsos = s1, s2
    
    return(pulsos) # retorna os dois contornos, um de cada pulso


##3.2. 
def contorno_limite_arbitrario(df, VA_1, VA_2, height, check):
    '''
        Esse loop serve para olhar, em cada waveform do Data Frame original, o contorno ao redor de cada pulso, selecionado através do pico e das larguras arbitradas.
        Por razões de implementaçao, filtramos como queremos em cada uma das waveforms e transformamos num array. Com isso,
    acho que ficará bem mais rápido de fazer essas operações. O resultado é empilhado e transformado num Data Frame.
    '''

    _ = peaks_divididos_01(df = df, height = height)
    peaks_0   ,   peaks_1      =     _[0]   ,    _[1]

    # if len(peaks_0) != len(peaks_1):
    #     print('erro na obtenção dos picos divididos')

    contorno_0 = []
    contorno_1 = []

    '''
    Para eventos que "terminam na borda" da janela, é possível que tenhamos um problema de tamanho do contorno, 
    que seria de não pegarmos ou todo o pulso ou de não conseguir alocar tudo num DataFrame por causa da diferença
    de tamanho.  
    '''
    aux = []

    for i in range( df.shape[1]  ): 
        
        evento = df[ df.columns[i] ]

        s0 = evento.where( 
           (evento.index >= peaks_0.x.iloc[i] - VA_1) & (evento.index <= peaks_0.x.iloc[i] + VA_2) 
                        ).dropna().array
        if len(s0) != 1 + VA_1 + VA_2:
            s0 = np.append(   s0   ,   np.full(1 + VA_1 + VA_2 - len(s0) , np.nan)    )
            aux.append(i)
        # if len(s0) != 1 + VA_1 + VA_2:
        #         print(f'erro em {i}')

        s1 = evento.where( 
           (evento.index >= peaks_1.x.iloc[i] - VA_1) & (evento.index <= peaks_1.x.iloc[i] + VA_2) 
                        ).dropna().array
        if len(s1) != 1 + VA_1 + VA_2:
            s1 = np.append(   s1   ,   np.full(1 + VA_1 + VA_2 - len(s1) , np.nan)    )
            aux.append(i)
        # if len(s1) != 1 + VA_1 + VA_2:
        #         print(f'erro em {i}')


        contorno_0.append(s0)
        contorno_1.append(s1)

    contorno_0 = pd.DataFrame( np.array(contorno_0) ).T # pontos do contorno vs waveform
    contorno_1 = pd.DataFrame( np.array(contorno_1) ).T
    


    # contorno_0 = np.array([])
    # contorno_1 = np.array([])

    # for i in range( df.shape[1]  ): 
        
    #     evento = df[ df.columns[i] ]
    #     s0 = evento.where( 
    #        (evento.index >= peaks_0.x.iloc[i] - VA_1) & (evento.index <= peaks_0.x.iloc[i] + VA_2) 
    #                     ).dropna().array
    #     s1 = evento.where( 
    #        (evento.index >= peaks_1.x.iloc[i] - VA_1) & (evento.index <= peaks_1.x.iloc[i] + VA_2) 
    #                     ).dropna().array

    #     if len(s1) != 91:
    #         print(f'erro em {i}')

    #     contorno_0 = np.append( contorno_0,s0 )
    #     contorno_1 = np.append( contorno_1,s1 )

    # contorno_0 = pd.DataFrame( 
    #     contorno_0.reshape( (df.shape[1] , 1 + VA_1 + VA_2) ) 
    #                         )

    # contorno_1 = pd.DataFrame( 
    #     contorno_1.reshape( (df.shape[1] , 1 + VA_1 + VA_2) ) 
    #                         )


    # contorno_0 = np.zeros(1 + VA_1 + VA_2)
    # contorno_1 = np.zeros(1 + VA_1 + VA_2)

    # for i in range( df.shape[1]  ): 
        
    #     evento = df[ df.columns[i] ]
    #     s0 = evento.where( 
    #        (evento.index >= peaks_0.x.iloc[i] - VA_1) & (evento.index <= peaks_0.x.iloc[i] + VA_2) 
    #                     ).dropna().array
    #     s1 = evento.where( 
    #        (evento.index >= peaks_1.x.iloc[i] - VA_1) & (evento.index <= peaks_1.x.iloc[i] + VA_2) 
    #                     ).dropna().array
    #     print('pimba')
    #     contorno_0 = np.vstack( (contorno_0, s0) )
    #     contorno_1 = np.vstack( (contorno_1, s1) )


    """
    Obs.: O código implementado está como está por uma questão de desempenho, ou seja, de tempo de execução.
        As justificativas se baseiam não só no tempo, na verdade, mas no fato de que eu não consegui mais guardar
    as Series dentro dos arrays, como originalmente. Acho que deve ter algo a ver com alguma atualização do Numpy, 
    mas o resultado agora parece "extender" os dois arrays sem separá-los.
    Ele é bem mais rápido do que o código "intuitivamente" implementado (usando o pd.concat), como segue:
    

    contorno_0 = pd.Series([])
    contorno_1 = pd.Series([])
     
    for i in range( df.shape[1]  ): 
        
       evento = df[ df.columns[i] ]
       s0 = evento.where( 
           (evento.index >= peaks_0.x.iloc[i] - VA_1) & (evento.index <= peaks_0.x.iloc[i] + VA_2) 
                        ).dropna()
       s1 = evento.where( 
           (evento.index >= peaks_1.x.iloc[i] - VA_1) & (evento.index <= peaks_1.x.iloc[i] + VA_2) 
                        ).dropna()
        
       contorno_0 = pd.concat( [contorno_0 , s0] , axis=1 )
       contorno_1 = pd.concat( [contorno_1 , s1] , axis=1 )
    """

    if check == 1:
        
        '''
        Loop de checagem dos contornos
        '''

        if ( len(contorno_0) and len(contorno_1) ) != df.shape[1] :
            _  = abs( len(contorno_0) - len(contorno_1) )
            __ = 'primeiro' if len(contorno_0) > len(contorno_1) else 'segundo'
            print(f'Os contornos não batem no tamanho. Existe(m) {_} a mais no {__}')

        for elemento in (contorno_0 or contorno_1):
            if len(elemento) != VA_1 + VA_2 + 1:
                print(f'Erro no {elemento.name}')
    

    if len(aux) != 0:
        print(f'\nForam detectados {len(aux)} problemas na questão do tamanho da janela do contorno;\nOs problemas estão em {aux};\nPreenchidos com valores Nan\n')
    else:
        print('\nNão foram detectados problemas na questão do tamanho da janela do contorno\n')

    #Retorna dois DataFrames contendo os contornos de cada waveform para cada um dos dois picos
    return(  contorno_0, contorno_1  ) 




###################################################################################################################
#4. Integrais

##4.1.
def integral_simples(dados_em_y, dx):
    _ = dados_em_y
    I = 0
    for i in range(len(_)):
        y = _.iloc[i]
        I += y * dx
    return(I)


def integral_simples_dataframe(df, dx):
    integrais = np.array([])
    for i in range( df.shape[1] ):
        coluna    = df[ df.columns[i] ].dropna()
        integral  = integral_simples(dados_em_y=coluna , dx=dx)
        integrais = np.append(integrais , integral)
    return(pd.Series(integrais))


###################################################################################################################
#5. Base Line

##5.1.
def baseLine_sample(series, height, VA_1): # recebe uma series do pandas
    '''
    Definimos essa função que retorna uma sample da base line da waveform.
    Retorna uma amostra da waveform para determinar o valor estatístico dela
    '''
    _ = peak_finder(series, height = height)
    
    '''Pega todos os elementos até o início do primeiro pulso; intervalo exclusivo à direita'''
    
    if len(_) != 0: # pode acontecer de que o peak_finder não 
        
        x_inicio_pulso_0 = _[0] - VA_1 # definido arbitrariamente    
        sample  = series.iloc[:x_inicio_pulso_0]
        
    else:
        sample = None

    return( sample ) # este elemento é uma Series


##5.2. Base Line

def baseLine(df, height, VA_1):
    
    baseLines = [] # será uma lista de series
    for i in range( df.shape[1] ):
        evento = df[ df.columns[i] ]
        baseLines.append( baseLine_sample(evento, height, VA_1 = VA_1) )
    baseLines = pd.concat(baseLines)

    return(baseLines) #retorna uma Series com os dados de base line




###################################################################################################################

print('mainFile e bibliotecas importados')