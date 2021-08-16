import pathlib
import pandas as pd
import os

#                          .
#==========================================================================================================
def Assemble_MuonDecay(path = 'documents/data/muon_decay'):
    """
    This function is built to 

    Parameters
    ----------

        . 

    """
    folders_list = os.listdir(path)
    folders_list_full_path = [ (path + '/' + i) for i in folders_list ]
    folders_list = [ i for i in folders_list_full_path if (os.path.isdir(i) == True) and (i != f'{path}/results') ] #only include folders

    integral_0 = []
    integral_1 = []
    peaks      = []

    for i in range( len(folders_list) ):

        folder_result_full_path = folders_list[i] + '/' + 'results'
        folder_results_content  = [ (folder_result_full_path + '/' + i) for i in os.listdir(folder_result_full_path) ]
        
        integral_0.extend( [ j for j in folder_results_content if 'integral_0.csv' in j ] )
        integral_1.extend( [ j for j in folder_results_content if 'integral_1.csv' in j ] )
        peaks.extend( [ j for j in folder_results_content if 'peaks.csv' in j ] )

    integral_0_total = pd.DataFrame()
    integral_1_total = pd.DataFrame()
    peaks_total      = pd.DataFrame()

    for i in range( len(integral_0) ):
    
        df_integral_0 = pd.read_csv( integral_0[i], index_col=0 )
        df_integral_1 = pd.read_csv( integral_1[i], index_col=0 )
        df_peaks      = pd.read_csv( peaks[i], index_col=0 )

        integral_0_total = pd.concat( [integral_0_total, df_integral_0] )
        integral_1_total = pd.concat( [integral_1_total, df_integral_1] )
        peaks_total      = pd.concat( [peaks_total     , df_peaks] )

    index = [ ('event_' + str(i)) for i in range(integral_0_total.shape[0]) ]
    integral_0_total.index = index
    integral_1_total.index = index
    peaks_total.index      = index
    
    pathlib.Path(f"{path}/results").mkdir(parents=True, exist_ok=True) #create folder to store the results
    integral_0_total.to_csv(path+'/results/integral_0.csv')
    integral_1_total.to_csv(path+'/results/integral_1.csv')
    peaks_total.to_csv(path+'/results/peaks.csv')

    print(f'\nDocuments joined on \n{path}/results\n')



#                          .
#==========================================================================================================
def Assemble_SingleMuon(path = 'documents/data/single_muon'):
    """
    This function is built to 

    Parameters
    ----------

        . 

    """

    raise(NotImplementedError)


