import re
import pandas as pd

from core.SPL import SPL
from static.constants import FILE_PATH

header = ['FDA_Application_Number',
          'SETID',
          'Drug_Name',
          'Effective_Date',
          'Box_Warning',
          'Indication',
          'Dosage_Administration',
          'Pregnancy',
          'Teratogenic_Effects',
          'Nonteratogenic_Effects',
          'Lactation',
          'Nursing_Mothers',
          'Mechanism_of_Action',
          'Pharmacodynamics',
          'Pharmacokinetics',
          'Carcinogenesis',
          'Information_for_Patients',
          'Absorption',
          'Distribution',
          'Metabolism',
          'Excretion',
          'Food_Effect',
          'Food_Effect_1',
          'Food_Effect_2',
          'Other'
          ]

admef_pattern = ['^absorption$',
                 '^distribution$',
                 '^metabolism$',
                 '^excretion$',
                 '^elimination$',
                 '^effect of food$',
                 '^effects of food$',
                 '^food effect$',
                 '^food effects$',
                 'table',
                 'figure',
                 'population',
                 'impairment',
                 'geriatric',
                 'pediatric',
                 'gender',
                 'race',
                 'ethnicity',
                 'interaction',
                 'interactions',
                 'racial',
                 'age',
                 'populations',
                 'weight',
                 'half-life']
adme_pattern = ['absorption', 'distribution', 'metabolism', 'excretion', 'elimination']


def spl_parse(raw_df):
    df = pd.DataFrame(columns=header)
    for i, row in raw_df.iterrows():
        if re.search(r'<document.+</document>', row.SPL):
            try:
                spl = SPL(re.search(r'<document.+</document>', row.SPL).group())
                df = df.append({
                    'FDA_Application_Number': spl.Appl_No,
                    'SETID': row.SETID,
                    'Drug_Name': spl.Drug_Name,
                    'Effective_Date': str(spl.Effective_Date),
                    'Box_Warning': spl.Box_Warning,
                    'Indication': spl.Indication,
                    'Dosage_Administration': spl.Dosage_Administration,
                    'Pregnancy': spl.Pregnancy,
                    'Teratogenic_Effects': spl.Teratogenic_Effects,
                    'Nonteratogenic_Effects': spl.Nonteratogenic_Effects,
                    'Lactation': spl.Lactation,
                    'Nursing_Mothers': spl.Nursing_Mothers,
                    'Mechanism_of_Action': spl.Mechanism_of_Action,
                    'Pharmacodynamics': spl.Pharmacodynamics,
                    'Pharmacokinetics': spl.Pharmacokinetics,
                    'Carcinogenesis': spl.Carcinogenesis,
                    'Information_for_Patients': spl.Information_for_Patients
                }, ignore_index=True)
            except:
                continue
        if (i + 1) % 5000 == 0:
            print('{} completed.'.format(str(i + 1)))
    return df


def identifier_remap(raw_df):
    new_row_count = 0
    new_row_df = pd.DataFrame()
    raw_df['Effective_Date'] = pd.to_datetime(raw_df['Effective_Date']).dt.date
    remap_df = raw_df.copy()
    for index, row in remap_df.iterrows():
        if not pd.isna(row.FDA_Application_Number):
            fda_appl_no_list = row['FDA_Application_Number'].split(' ')
            if len(fda_appl_no_list) > 1:
                new_row_count += len(fda_appl_no_list) - 1
                remap_df.at[index, 'FDA_Application_Number'] = fda_appl_no_list[0]
                for i in range(1, len(fda_appl_no_list)):
                    new_row = row
                    new_row['FDA_Application_Number'] = fda_appl_no_list[i]
                    new_row_df = new_row_df.append(new_row)
    print('new_row_df: ' + str(len(new_row_df)))
    remap_df = remap_df.append(new_row_df)
    return remap_df


def remove_duplicate(remap_df):
    no_appl_num_df = remap_df[pd.isna(remap_df['FDA_Application_Number'])].copy()
    remap_df = remap_df[~pd.isna(remap_df['FDA_Application_Number'])]

    nda_pattern = r'^ANDA|^NDA'
    nda_filter = remap_df['FDA_Application_Number'].str.match(nda_pattern)

    nda_df = remap_df[nda_filter].copy()
    nda_df = nda_df \
        .sort_values(['FDA_Application_Number', 'Effective_Date'], ascending=(True, False)) \
        .reset_index(drop=True)
    nda_df = nda_df \
        .drop_duplicates(subset=['FDA_Application_Number'], keep='first') \
        .reset_index(drop=True)

    non_nda_df = remap_df[~nda_filter].copy()
    non_nda_df = non_nda_df \
        .sort_values(['FDA_Application_Number', 'Effective_Date'], ascending=(True, False)) \
        .reset_index(drop=True)
    non_nda_df = non_nda_df \
        .drop_duplicates(subset=['FDA_Application_Number'], keep='first') \
        .reset_index(drop=True)
    non_nda_df = non_nda_df.append(no_appl_num_df)

    return nda_df, non_nda_df


def label_admef(df):
    for index, row in df.iterrows():
        if not pd.isna(row['Pharmacokinetics']):
            # Pattern 1
            admef_content_list = re.split('\n|\\\\n', row['Pharmacokinetics'])
            admef_content_list = list(filter(len, admef_content_list))
            admef_idx_list = [(i, item) for i, item in enumerate(admef_content_list)
                              if item
                              and len(item.split(' ')) <= 10
                              and ',' not in item
                              and item[-1] != '.'
                              and re.search(r'|'.join(admef_pattern), re.sub(r'[^a-z ]+', '', item.lower().strip()))]
            if len(list(filter(lambda item: re.search(r'|'.join(adme_pattern), item[1].lower()),
                               admef_idx_list))) > 0:
                admef_dict = build_dict_helper(admef_idx_list, admef_content_list)
                row['Absorption'] = dict_value_helper(admef_dict, 'Absorption')
                row['Distribution'] = dict_value_helper(admef_dict, 'Distribution')
                row['Metabolism'] = dict_value_helper(admef_dict, 'Metabolism')
                row['Excretion'] = dict_value_helper(admef_dict, 'Excretion|Elimination')
                row['Food_Effect_1'] = dict_value_helper(admef_dict,
                                                         'food effect|food effects|effect of food|effects of food')
                row['Other'] = remove_admef(admef_content_list, admef_dict)
                admef_content_list = row['Other'].split('\n')
            # Pattern 2
            for paragraph in admef_content_list:
                if re.search(':|—|-|–', paragraph):
                    title = re.split(':|—|-|–', paragraph)[0]
                    remove_paragraph = lambda x: x is not paragraph
                    found = False
                    if len(title.split(' ')) < 4:
                        if re.search(r'^absorption', title.lower()):
                            row['Absorption'] = paragraph[len(title)+1:].strip()
                            admef_content_list = list(filter(remove_paragraph, admef_content_list))
                            found = True
                        if re.search(r'^distribution', title.lower()):
                            row['Distribution'] = paragraph[len(title)+1:].strip()
                            admef_content_list = list(filter(remove_paragraph, admef_content_list))
                            found = True
                        if re.search(r'^metabolism', title.lower()):
                            row['Metabolism'] = paragraph[len(title)+1:].strip()
                            admef_content_list = list(filter(remove_paragraph, admef_content_list))
                            found = True
                        if re.search(r'^excretion|^elimination', title.lower()):
                            df.at[index, 'Excretion'] = paragraph[len(title)+1:].strip()
                            admef_content_list = list(filter(remove_paragraph, admef_content_list))
                            found = True
                        if re.search(r'|'.join(['^effect of food',
                                                '^effects of food',
                                                '^food effect',
                                                '^food effects']), title.lower()):
                            row['Food_Effect_1'] = paragraph[len(title)+1:].strip()
                            admef_content_list = list(filter(remove_paragraph, admef_content_list))
                            found = True
                        if found:
                            row['Other'] = '\n'.join(admef_content_list)
            # Food Effect in Absorption
            if not pd.isna(row['Absorption']):
                absorption_list = row['Absorption'].split('\n')
                for paragraph in absorption_list:
                    if re.search(r'^(food effect|food effects|effect of food|effects of food)\s*(:|—|-|–)', paragraph.lower()):
                        if pd.isna(row['Food_Effect_1']) or row['Food_Effect_1'] == '':
                            title = re.split(':|—|-|–', paragraph)[0]
                            row['Food_Effect_2'] = paragraph[len(title)+1:].strip()
                            absorption_list.remove(paragraph)
                row['Absorption'] = '\n'.join(absorption_list)
            row['Food_Effect'] = row['Food_Effect_2'] \
                if pd.isna(row['Food_Effect_1']) or row['Food_Effect_1'] == '' \
                else row['Food_Effect_1']
    return df


def build_dict_helper(title_idx_list, content_list):
    content_dict = {}
    for i, title_idx in enumerate(title_idx_list):
        if i == len(title_idx_list) - 1:
            content_dict[title_idx[1]] = content_list[title_idx[0] + 1:]
        else:
            content_dict[title_idx[1]] = content_list[title_idx[0] + 1:title_idx_list[i + 1][0]]
    return content_dict


def dict_value_helper(dist, key):
    value_list = []
    for dict_key, dict_value in dist.items():
        if re.search(rf'{key.lower()}', dict_key.lower()):
            value_list.extend(filter(len, dict_value))
    return '\n'.join(value_list)


def remove_admef(content_list, admef_dict):
    content_list = list(content_list)
    for dict_key, dict_value in admef_dict.items():
        if re.search(r'|'.join(['absorption',
                                'distribution',
                                'metabolism',
                                'excretion',
                                'elimination',
                                'effect of food',
                                'effects of food',
                                'food effect',
                                'food effects']), dict_key.lower()):
            content_list.remove(dict_key)
            content_list = list(filter(lambda x: x not in dict_value, content_list))
    return '\n'.join(content_list)


if __name__ == '__main__':
    dailymed_raw_df = pd.read_csv(FILE_PATH.DAILYMED_RAW, dtype=str)
    print('dailymed_raw_df: ' + str(len(dailymed_raw_df)))
    dailymed_spl_df = spl_parse(dailymed_raw_df)
    dailymed_spl_df.to_csv(FILE_PATH.DAILYMED_SPL, index=False)

    dailymed_spl_df = pd.read_csv(FILE_PATH.DAILYMED_SPL, dtype=str)
    dailymed_remap_df = identifier_remap(dailymed_spl_df)
    print('dailymed_remap_df: ' + str(len(dailymed_remap_df)))
    dailymed_remap_df.to_csv(FILE_PATH.DAILYMED_REMAP, index=False)

    dailymed_remap_df = pd.read_csv(FILE_PATH.DAILYMED_REMAP, dtype=str)
    dailymed_nda_df, dailymed_non_nda_df = remove_duplicate(dailymed_remap_df)
    print('dailymed_nda_df: ' + str(len(dailymed_nda_df)))
    print('dailymed_non_nda_df: ' + str(len(dailymed_non_nda_df)))
    dailymed_nda_df.loc[:, ['FDA_Application_Number', 'SETID', 'Drug_Name', 'Effective_Date']].to_csv(FILE_PATH.DAILYMED_MAPPING, index=False)
    # dailymed_nda_df.to_csv(FILE_PATH.DAILYMED_PREPROCESS, index=False)

    # dailymed_nda_df = pd.read_csv(FILE_PATH.DAILYMED_PREPROCESS, dtype=str)
    dailymed_admef_df = label_admef(dailymed_nda_df)
    print('dailymed_admef_df: ' + str(len(dailymed_admef_df)))
    dailymed_admef_df.to_csv(FILE_PATH.DAILYMED_PREPROCESS, index=False)
