import json
import pandas as pd

from core.drugsfda import DrugsFDAPdf
from static.constants import FILE_PATH


def preprocess(raw_df):
    nda_pattern = r'^ANDA|^NDA'
    nda_filter = raw_df['full_appl_no'].str.match(nda_pattern)

    nda_df = raw_df[nda_filter].copy()
    nda_df = nda_df \
        .sort_values(['full_appl_no', 'docs_date'], ascending=(True, False)) \
        .reset_index(drop=True)
    nda_df = nda_df \
        .drop_duplicates(subset=['full_appl_no'], keep='first') \
        .reset_index(drop=True)

    non_nda_df = raw_df[~nda_filter].copy()
    non_nda_df = non_nda_df \
        .sort_values(['full_appl_no', 'docs_date'], ascending=(True, False)) \
        .reset_index(drop=True)
    non_nda_df = non_nda_df \
        .drop_duplicates(subset=['full_appl_no'], keep='first') \
        .reset_index(drop=True)

    return nda_df, non_nda_df


def dict_helper(title_idx_list, content_list):
    content_dict = {}
    for i, title_idx in enumerate(title_idx_list):
        if i == len(title_idx_list) - 1:
            content_dict[title_idx[1]] = content_list[title_idx[0] + 1:]
        else:
            content_dict[title_idx[1]] = content_list[title_idx[0] + 1:title_idx_list[i + 1][0]]
    return content_dict


if __name__ == '__main__':
    drugs_fda_raw_df = pd.read_csv(FILE_PATH.DRUGSFDA_RAW)
    print('drugs_fda_raw_df: ' + str(len(drugs_fda_raw_df)))

    drugs_fda_nda_df, drugs_fda_non_nda_df = preprocess(drugs_fda_raw_df)
    print('drugs_fda_nda_df: ' + str(len(drugs_fda_nda_df)))
    print('drugs_fda_non_nda_df: ' + str(len(drugs_fda_non_nda_df)))

    for i, row in drugs_fda_nda_df.iterrows():
        drugsFDAPdf = DrugsFDAPdf(row.pdf_content)
        drugs_fda_nda_df.at[i, 'pdf_dict'] = json.dumps(drugsFDAPdf.pdf_content_dict, sort_keys=True, indent=4)
        drugs_fda_nda_df.at[i, 'Box_Warning'] = drugsFDAPdf.Boxed_Warning
        drugs_fda_nda_df.at[i, 'Indication'] = drugsFDAPdf.Indication
        drugs_fda_nda_df.at[i, 'Dosage_Administration'] = drugsFDAPdf.Dosage_Administration
        drugs_fda_nda_df.at[i, 'Pregnancy'] = drugsFDAPdf.Pregnancy
        drugs_fda_nda_df.at[i, 'Lactation'] = drugsFDAPdf.Lactation
        drugs_fda_nda_df.at[i, 'Mechanism_of_Action'] = drugsFDAPdf.Mechanism_of_Action
        drugs_fda_nda_df.at[i, 'Pharmacodynamics'] = drugsFDAPdf.Pharmacodynamics
        drugs_fda_nda_df.at[i, 'Pharmacokinetics'] = drugsFDAPdf.Pharmacokinetics
        drugs_fda_nda_df.at[i, 'Absorption'] = drugsFDAPdf.Absorption
        drugs_fda_nda_df.at[i, 'Distribution'] = drugsFDAPdf.Distribution
        drugs_fda_nda_df.at[i, 'Metabolism'] = drugsFDAPdf.Metabolism
        drugs_fda_nda_df.at[i, 'Excretion'] = drugsFDAPdf.Excretion
        drugs_fda_nda_df.at[i, 'Food_Effect'] = drugsFDAPdf.Food_Effect
        drugs_fda_nda_df.at[i, 'Food_Effect_1'] = drugsFDAPdf.Food_Effect_1
        drugs_fda_nda_df.at[i, 'Food_Effect_2'] = drugsFDAPdf.Food_Effect_2
        drugs_fda_nda_df.at[i, 'Cytotoxic'] = drugsFDAPdf.Cytotoxic
        drugs_fda_nda_df.at[i, 'Information_for_Patients'] = drugsFDAPdf.Information_for_Patients
        drugs_fda_nda_df.at[i, 'Other'] = drugsFDAPdf.Other

    drugs_fda_nda_df.drop(['pdf_content'], axis=1).to_csv(FILE_PATH.DRUGSFDA_PREPROCESS, index=False)
