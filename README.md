# Repositório para os códigos do experimento vida média dos múons.
================================================================================
  O experimento utiliza:
  -  osciloscópio Tektronix TDS 1002B com driver Visa e  pacote pylef do LEB-IFGW
     TEKVISA Connectivity Software - V4.2.0
	 https://download.tek.com/secure/software/TekVISA_404_066093809.exe?nva=20200613175735&nbv=20200613174235&token=0bccb3f1f3c552b1fccdf
	 
	 pylef: https://github.com/gwiederhecker/pylef
	 
  - detector de particulas (cintilador plástico+PMT+fonte de HV)
  - computador com Python3 (Anaconda, spyder)
===============================================================================
    Os códigos no momento são:
	 - daqTek_onlyData.py
	 - daqTek_fitPlot.py
	 - plotVidamedia.py
	 
	Para o desenvolvimento do projeto em casa usamos os arquivos de dados
	 - 5500_diferencias.cvs (diferença de tempo, em microsegundo, entre dois pulsos)
	 - eventos200.cvs (200 waveforms com 2500 pontos cada uma, o arquivo com 5500 é mito grande e o github não aceita)
	    - o arquivo com 5500 eventos está no Google Drive: https://drive.google.com/open?id=12PdxqnW8CiDlFmtguUx0o1hdQtklEnFw
	 
Para fazer:
 1) introduzir o tempo em UTC de cada evento (= dois pulsos na waveform)
 2) codigos para fazer obter os espectros de carga (e amplitude) dos dois pulsos 
 2) codigos para verificar a boa qualidade dos dados obtidos
	contagem x tempo,  carga x tempo (intervalo de tempo variável, 5min..., eixo y em hz, eixo x em minutos)
