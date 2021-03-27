# Códigos do experimento vida média dos múons.
================================================================================
  
O experimento utiliza:
 - Osciloscópio Tektronix TDS 1002B com driver Visa TEKVISA Connectivity Software - V4.2.0
	- Link: https://download.tek.com/secure/software/TekVISA_404_066093809.exe?nva=20200613175735&nbv=20200613174235&token=0bccb3f1f3c552b1fccdf
 - Python3 (com Anaconda, de preferência)
 	- a biblioteca utilizada para comunicação com o osciloscópio é, atualmente, o pyvisa (https://pyvisa.readthedocs.io/en/latest/#)
 - Detector de particulas (cintilador de plástico+PMT+fonte de HV)
 - Computador com Windows 7/10 
 - Opcional: para o desenvolvimento do código, utiliza-se o VS Code. 


### Código: _overview_ 
===============================================================================

Os códigos em Python no momento são:

- MuonDecay
	 - acquisition
		- Configs: onde são guardados os config_files para a aquisição
		- DataAcquisition: contem as funções para aquisição dos dados e para o _set_ do osciloscópio
		- SaveOutputs: contem as funções auxiliares, como as funções de enviar email, salvar o _output_ do terminal, criar as pastas para armazenar os dados adquiridos etc.

	 - data_analyze
		- .old: versões anteriores do projeto
		- Analyze: 
		- FindPeaks:   
		- Preliminaries: 
		- RegExp: 
		- Spectrums: 

	 - development: códigos experimentais	

	 - documents
		- .old: versões anteriores dos documentos
		- data: pasta onde são armazenados os documentos de aquisição e dos resultados das análises de dados
		- images: pasta para armazenar os gráficos e os resultados em imagem



### Desenvolvimento:
===============================================================================

Para o desenvolvimento do projeto em casa usamos os arquivos de dados "documents/data/previous_data/5555_eventos-edit.csv".
 - Obs:
 	- Este arquivo é uma versão modificada de um arquivo que não cabia no GitHub e que está no GoogleDrive (https://drive.google.com/open?id=12PdxqnW8CiDlFmtguUx0o1hdQtklEnFw)
 	- Existem outros arquivos, como uns arquivos com menos eventos ou outros arquivos com outros registros, mas o principal é o mencionado acima
 

	 
### Para fazer:
===============================================================================
 - introduzir o tempo em UTC no início de cada linha dos dados
 	- ver codigo daqTek_FauthBruno.py
 - codigos para fazer obter os espectros de carga (e amplitude) dos dois pulsos 
 - codigos para verificar a boa qualidade dos dados obtidos
	- contagem x tempo,  carga x tempo (intervalo de tempo variável, 5min..., eixo y em hz, eixo x em minutos)


Importante:
 - Para rodar os códigos no repositório do GitHub é necessário ajeitar o PATH do Python para que ele consiga reconhecer o diretório e encontrar os códigos que são importados.
 [dar instruções e tal]
