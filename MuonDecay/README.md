# Código: _overview_ 
===========================================================================

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




# Utilização do código: 
===========================================================================
 

### Instalação do Python no computador

 - Recomenda-se a instalação do Anaconda (https://www.anaconda.com/products/individual), que facilita bastante na questão das bibliotecas e facilita a instalação do python no computador.
 	- Se for instalar o Anaconda, recomenda-se incluir o Anaconda no path do computador. Esse é um passo adiantado, mas pode ser resolvido depois.
 	
 	![alt text](https://fgnt.github.io/python_crashkurs_doc/_images/path.png)
 
 - Se não for usar o Anaconda, pode-se instalar o Python de outras maneiras (https://www.python.org/downloads/)
 - Após a instalação do Python, verifique se as bibliotecas estão todas instaladas corretamente. Se você instalou o Anaconda, pode pular essa etapa
 	- {instruções sobre instalação das bibiotecas necessárias para rodar os códigos a partir do requirements.txt}




### Repositório no computador e PythonPATH

 - É necessário clonar o repositório do GitHub no computador
 - *IMPORTANTÍSSIMO*: para rodar os códigos que estão no repositório do GitHub é necessário ajeitar o PATH do Python para que ele consiga reconhecer o diretório e encontrar os códigos que são importados. 
 	- {intruções detalhadas aqui}
 
 
 
### Execução dos códigos

 - Após essas preliminares estarem resolvidas, pode-se partir para a execução dos códigos
 	- Aquisição: em "development/onlyData_v06.py" está a última versão do código. Ele pode ser executado normalmente com o Python a partir do terminal (cmd, powershell etc.)
 		- Se ocorrer algum erro com problema de _import_ do Python, verifique o PythonPATH no seu sistema operacional
 		- O código deve, normalmente, levar um longo tempo para ser concluído
 		- Se ocorrer um erro por causa da falta do arquivo de "config_email", é porque é necessário que você crie o seu próprio. Recomenda-se que você adicione o arquivo ao "git ignore" no seu computador
 	- Análise de dados: o código de análise "data_analyze/analyze.ipynb" é um _Jupyter notebook_. Ele pode ser rodado diretamente também, basta abri-lo e executá-lo.




### Desenvolvimento:
===========================================================================
 - Para o desenvolvimento do projeto em casa usamos os arquivos de dados "documents/data/previous_data/5555_eventos-edit.csv".
 - O desenvolvimento do código de aquisição envolve o pyvisa e o código de análise é basicamente fundamentado no pandas.
 - Obs:
 	- Este arquivo é uma versão modificada de um arquivo que não cabia no GitHub e que está no GoogleDrive (https://drive.google.com/open?id=12PdxqnW8CiDlFmtguUx0o1hdQtklEnFw)
 	- Existem outros arquivos, como uns arquivos com menos eventos ou outros arquivos com outros registros, mas o principal é o mencionado acima
 
