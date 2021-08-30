from data_analyze.Spectrums.convert_integral import find_charge_single_muon
from data_analyze.Preliminaries.read_output_file import retrieve_y_to_volts

folder = 'documents/data/single_muon/1625353737.1067114'

converter = retrieve_y_to_volts(folder)

histogram , max_value = find_charge_single_muon(path=f'{folder}/results', converter_df=converter)

print(max_value)

