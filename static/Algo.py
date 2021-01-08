import pandas as pd
import numpy as np

uni_mappings = pd.read_csv('static/Country-Continent-Language.csv')
module_mappings = pd.read_csv('static/Module-Mappings.csv')

def unique(lst):
    unique_elements = []
    for i in lst:
        if i not in unique_elements:
            unique_elements.append(i)
    return unique_elements

### Add to this as required
def repeated_mods_finder(lst):
    n = len(lst)
    for i in range(n):
        try:
            if lst[i][:6] == 'CS1010':
                lst[i] = 'CS1010'
            elif lst[i][:6] == 'CS1231':
                lst[i] = 'CS1231'
            elif lst[i][:6] == 'CS2040':
                lst[i] = 'CS2040'
            elif lst[i][:6] == 'CS2030':
                lst[i] = 'CS2030'
            elif lst[i][:6] == 'CS1101':
                lst[i] = 'CS1010'
            elif lst[i][:7] == 'ACC1002':
                lst[i] = 'ACC1002'
            elif lst[i][:7] == 'ACC1701':
                lst[i] = 'ACC1701'
            elif lst[i][:6] == 'CS2103':
                lst[i] = 'CS2103'
            elif lst[i][:7] == 'FIN2004':
                lst[i] = 'FIN2004'
            elif (lst[i][:3] in ['LSM','BSP','ACC','FIN']) and (lst[i][-1] not in '1234567890'):
                lst[i] = lst[i][:-1]
        except:
            pass
    return lst

def parser(input_dict):
    if input_dict['Location_type'].lower() == 'regions':
        restricted_unis = uni_mappings.loc[uni_mappings['Continent'].isin(input_dict['Location'])]
    elif input_dict['Location_type'].lower() == 'countries':
        restricted_unis = uni_mappings.loc[uni_mappings['Country'].isin(input_dict['Location'])]
    elif input_dict['Location_type'].lower() == 'universities':
        restricted_unis = uni_mappings.loc[uni_mappings['University'].isin(input_dict['Location'])]
    else:
        raise ValueError("Value of Location_type MUST be either 'regions', 'countries' or 'universities'")
    return {'valid unis': list(restricted_unis['University']),
            'Ess_nus_codes': repeated_mods_finder(input_dict['Ess_nus_codes']),
            'Op_nus_codes': repeated_mods_finder(input_dict['Op_nus_codes'])}

def essential_mods_finder(restricted_unis,mods):
    output = []
    for uni in restricted_unis:
        valid = True
        for mod in mods:
            if mod.upper() not in uni_mods[uni]:
                valid = False
                break
        if valid:
            output.append(uni)
    return output

def optional_mods_finder(restricted_unis,mods):
    output = {}
    for uni in restricted_unis:
        output[uni] = []
        for mod in mods:
            if mod.upper() in uni_mods[uni]:
                output[uni].append(mod.upper())
    return output

countries = unique(uni_mappings['Country'])
continents = unique(uni_mappings['Continent'])

english_speaking = []
for i in range(len(uni_mappings)):
    if uni_mappings.iloc[i]['English-speaking']:
        english_speaking.append(uni_mappings.iloc[i]['University'])

uni_mods = {}
for uni in uni_mappings['University']:
    rows = module_mappings.loc[module_mappings['Partner University'] == uni]
    mods = unique(rows['NUS Module 1'].append(rows['NUS Module 2']))
    mods.remove(np.nan)
    if uni[:24] == 'University of California':
        rows1 = module_mappings.loc[module_mappings['Partner University'] == 'University of California']
        for mod in unique(rows1['NUS Module 1'].append(rows1['NUS Module 2'])):
            mods.append(mod)
        try:
            mods.remove(np.nan)
        except:
            pass
    mods = unique(repeated_mods_finder(mods))
    try:
        mods.remove(np.nan)
    except:
        pass
    uni_mods[uni] = mods

module_mappings['NUS Module 1'] = repeated_mods_finder(list(module_mappings['NUS Module 1']))
module_mappings['NUS Module 2'] = repeated_mods_finder(list(module_mappings['NUS Module 2']))

def main(input_dict):
    parsed = parser(input_dict)
    unis_with_essentials = essential_mods_finder(parsed['valid unis'],parsed['Ess_nus_codes'])
    unis_with_optionals = optional_mods_finder(unis_with_essentials,parsed['Op_nus_codes'])
    output = {}
    for uni in unis_with_optionals:
        region = uni_mappings.loc[uni_mappings['University'] == uni]['Continent'].iloc[0]
        if region not in output:
            output[region] = {}

        country = uni_mappings.loc[uni_mappings['University'] == uni]['Country'].iloc[0]
        if country not in output[region]:
            output[region][country] = {}

        uni_name = uni
        if country not in output[region][country]:
            output[region][country][uni] = {}

        if uni[:24] != 'University of California':
            df = module_mappings.loc[module_mappings['Partner University'] == uni]
        else:
            df = module_mappings.loc[(module_mappings['Partner University'] == uni) | (module_mappings['Partner University'] == 'University of California')]

        for module in input_dict['Ess_nus_codes']:
            details = df.loc[(df['NUS Module 1'] == module.upper()) | (df['NUS Module 2'] == module.upper())]
            try:
                PU_Title = details['PU Module 1 Title'].iloc[0]
            except:
                print(uni,module)
            PU_Code = details['PU Module 1'].iloc[0]
            output[region][country][uni][module] = {'PU Module Title': PU_Title, 'PU Module Code': PU_Code}

        for module in input_dict['Op_nus_codes']:
            details = df.loc[(df['NUS Module 1'] == module.upper()) | (df['NUS Module 2'] == module.upper())]
            try:
                PU_Title = details['PU Module 1 Title'].iloc[0]
                PU_Code = details['PU Module 1'].iloc[0]
                output[region][country][uni][module] = {'PU Module Title': PU_Title, 'PU Module Code': PU_Code}
            except:
                pass
        output[region][country][uni]['n_mods'] = len(output[region][country][uni])
    return output
