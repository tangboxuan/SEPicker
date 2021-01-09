import pandas as pd
import numpy as np

mappings = pd.read_csv('static/Module-Mappings.csv')
mappings = mappings.fillna('INVALID')

def dict_merger(dict1,dict2):
    for region in dict2:
        if region not in dict1:
            dict1[region] = dict2[region]
            continue
        for country in dict2[region]:
            if country not in dict1[region]:
                dict1[region][country] = dict2[region][country]
                continue
            # Doesn't matter if we overwrite since the data is the same if they exist in both
            for uni in dict2[region][country]:
                dict1[region][country][uni] = dict2[region][country][uni]

    return dict1

def main(input_dict):
    if input_dict['Location_type'].lower() == 'regions':
        areas = mappings[mappings['Continent'].isin(input_dict['Location'])]
    elif input_dict['Location_type'].lower() == 'countries':
        areas = mappings[mappings['Country'].isin(input_dict['Location'])]
    elif input_dict['Location_type'].lower() == 'universities':
        areas = mappings[mappings['Partner University'].isin(input_dict['Location'])]
    else:
        raise ValueError("Value of Location_type MUST be either 'regions', 'countries' or 'universities'")
    departments = list(input_dict['Departments'].keys())
    truthy = (areas['Department 1'] == departments[0]) # & (areas['Level'] == input_dict['Departments'][departments[0]])
    for key in departments[1:]:
        truthy = truthy | (areas['Department 1'] == key) # & (areas['Level'] == input_dict['Departments'][key])
    levels = areas[truthy]

    unique_unis = np.unique(levels['Partner University'])

    output_dict = {}
    for uni in unique_unis:
        uni_reference = levels[levels['Partner University'] == uni]
        region = uni_reference['Continent'].iloc[0]
        country = uni_reference['Country'].iloc[0]
        if region not in output_dict:
            output_dict[region] = {country: {}}
        if country not in output_dict[region]:
            output_dict[region][country] = {uni: {}}
        if uni not in output_dict[region][country]:
            output_dict[region][country][uni] = {}
        modules = uni_reference['NUS Module 1']
        unique_modules = np.unique(modules)
        for module in unique_modules:
            row = uni_reference[uni_reference['NUS Module 1'] == module]
            PU_title = row['PU Module 1 Title'].iloc[0]
            PU_code = row['PU Module 1'].iloc[0]
            output_dict[region][country][uni][module] = {'PU Module Title': PU_title, 'PU Module Code': PU_code}
        output_dict[region][country][uni]['n_mods'] = len(output_dict[region][country][uni])
    return output_dict
