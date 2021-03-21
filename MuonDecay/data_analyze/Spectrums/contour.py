import pandas as pd
import numpy as np

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



def contorno_limite_derivada(series, VA_1, VA_2, height): # recebe uma Series do pandas para começar
    '''
    Define um recorte de onde se deve buscar um pulso e os seus delimitadores
    VA_1 e VA_2 são variáveis arbitrárias para definir a largura do pulso 
    '''
    peak = peak_finder(series, height=height) # encontrar os picos da waveform
    
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



def contour_arbitrary(waveform, peak, random_left, random_right):
    '''
    waveform: column of the waveforms DataFrame.
    random_left: specified number that tells how much to displace to left before start to retrieve the sample.
    random_right: idem, but to the right side
    '''

    




def contorno_limite_arbitrario(df, VA_1, VA_2, height , err_mess=0):
    '''
        Esse loop serve para olhar, em cada waveform do Data Frame original, o contorno ao redor de cada pulso, selecionado através do pico e das larguras arbitradas.
        Por razões de implementaçao, filtramos como queremos em cada uma das waveforms e transformamos num array. Com isso,
    acho que ficará bem mais rápido de fazer essas operações. O resultado é empilhado e transformado num Data Frame.
    '''

    peaks_0   ,   peaks_1      =     peaks_divididos_01(df=df, height=height)
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
    

    if err_mess == 1:
        
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
        if err_mess == 1:
            print('\nNão foram detectados problemas na questão do tamanho da janela do contorno\n')

    #Retorna dois DataFrames contendo os contornos de cada waveform para cada um dos dois picos
    return(  contorno_0, contorno_1  )



def contorno_limite_arbitrario_picos(df, peaks_01, VA_1, VA_2, height, err_mess=0):
    '''
        Esse loop serve para olhar, em cada waveform do Data Frame original, o contorno ao redor de cada pulso, selecionado através do pico e das larguras arbitradas.
    Por razões de implementaçao, filtramos como queremos em cada uma das waveforms e transformamos num array. Com isso,
    acho que ficará bem mais rápido de fazer essas operações. O resultado é empilhado e transformado num Data Frame.
    '''

    peaks_xy_0   ,   peaks_xy_1      =     peaks_01
    
    '''
        Para eventos que "terminam na borda" da janela, é possível que tenhamos um problema de tamanho do contorno, 
    que seria de não pegarmos ou todo o pulso ou de não conseguir alocar tudo num DataFrame por causa da diferença
    de tamanho.  
    '''
    # aux = []

    # for i in range( df.shape[1]  ): 
        
    #     evento = df[ df.columns[i] ]

    #     s0 = evento.where( 
    #        (evento.index >= peaks_0.x.iloc[i] - VA_1) & (evento.index <= peaks_0.x.iloc[i] + VA_2) 
    #                     ).dropna().array
    #     if len(s0) != 1 + VA_1 + VA_2:
    #         s0 = np.append(   s0   ,   np.full(1 + VA_1 + VA_2 - len(s0) , np.nan)    )
    #         aux.append(i)
    #     # if len(s0) != 1 + VA_1 + VA_2:
    #     #         print(f'erro em {i}')

    #     s1 = evento.where( 
    #        (evento.index >= peaks_1.x.iloc[i] - VA_1) & (evento.index <= peaks_1.x.iloc[i] + VA_2) 
    #                     ).dropna().array
    #     if len(s1) != 1 + VA_1 + VA_2:
    #         s1 = np.append(   s1   ,   np.full(1 + VA_1 + VA_2 - len(s1) , np.nan)    )
    #         aux.append(i)
    #     # if len(s1) != 1 + VA_1 + VA_2:
    #     #         print(f'erro em {i}')

    contorno_0 = []
    aux_0 = []
    for i in peaks_xy_0.index:
        evento = df[ df.columns[i] ]
        s0 = evento.where( 
            (evento.index >= peaks_xy_0['x'][i] - VA_1) & (evento.index <= peaks_xy_0['x'][i] + VA_2) 
                            ).dropna().array
        if len(s0) != 1 + VA_1 + VA_2:
            s0 = np.append(   s0   ,   np.full(1 + VA_1 + VA_2 - len(s0) , np.nan)    )
            aux_0.append(i)
            # if len(s0) != 1 + VA_1 + VA_2:
            #         print(f'erro em {i}')
        contorno_0.append(s0)
    
    contorno_1 = []
    aux_1 = []
    for i in peaks_xy_1.index:
        evento = df[ df.columns[i] ]
        s1 = evento.where( 
            (evento.index >= peaks_xy_1['x'][i] - VA_1) & (evento.index <= peaks_xy_1['x'][i] + VA_2) 
                            ).dropna().array
        if len(s1) != 1 + VA_1 + VA_2:
            s1 = np.append(   s1   ,   np.full(1 + VA_1 + VA_2 - len(s1) , np.nan)    )
            aux_1.append(i)
            # if len(s1) != 1 + VA_1 + VA_2:
            #         print(f'erro em {i}')
        contorno_1.append(s1)

    contorno_0 = pd.DataFrame( np.array(contorno_0) ).T # pontos do contorno vs waveform
    contorno_1 = pd.DataFrame( np.array(contorno_1) ).T
    

    if err_mess == 1:
        
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
    
    aux = aux_0 + aux_1
    if len(aux) != 0:
        print(f'\nForam detectados {len(aux)} problemas na questão do tamanho da janela do contorno;\nOs problemas estão em {aux};\nPreenchidos com valores Nan\n')
    else:
        if err_mess == 1:
            print('\nNão foram detectados problemas na questão do tamanho da janela do contorno\n')

    '''
    Retorna dois DataFrames contendo os contornos de cada waveform para cada um dos dois picos
    '''
    return(  contorno_0, contorno_1  )