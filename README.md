# Códigos do experimento vida média dos múons.

### Requisitos:
===========================================================================
  
O experimento utiliza:
 - Osciloscópio Tektronix TDS 1002B com driver Visa TEKVISA Connectivity Software - V4.2.0
	- Link: https://download.tek.com/secure/software/TekVISA_404_066093809.exe?nva=20200613175735&nbv=20200613174235&token=0bccb3f1f3c552b1fccdf
 - Python3 (com Anaconda, de preferência)
 	- a biblioteca utilizada para comunicação com o osciloscópio é, atualmente, o pyvisa (https://pyvisa.readthedocs.io/en/latest/#)
 - Detector de particulas (cintilador de plástico+PMT+fonte de HV)
 - Computador com Windows 7/10 
 - Opcional: para o desenvolvimento do código, utiliza-se o VS Code; ROOT também é opcional (visite https://root.cern/install/) para mais detalhes).



### Overview
 - MuonDecay: diretório principal do código em Python
 - ROOT: diretório contendo arquivos desenvolvidos em ROOT. Basicamente, servem para o mesmo propósito que os códigos em Python do MuonDecay



	 
### Para fazer:
===========================================================================
 - Verificar a aquisição rodando com longevidade
 - Fazer o _curve fit_ do espectro de Michel nos dados
 - Escolher uma versão adequada dos filtros
 - Como incorporar a captura do múon negativo?
 



### Para mais detalhes: 
===========================================================================

Visite os diretórios correspondentes
