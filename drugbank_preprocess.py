import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np

from static.constants import FILE_PATH

ns = {'db': 'http://www.drugbank.ca'}


combineDelimiter = '\n\n'


def xml_to_csv():
    raw_df = pd.DataFrame()
    path = []
    with open(FILE_PATH.DRUGBANK_ORIGIN) as xml_file:
        for event, elem in ET.iterparse(xml_file, events=("start", "end")):
            if event == "start":
                path.append(elem.tag)
            if event == "end":
                if elem.tag == ET.QName(ns["db"], 'drug') and len(path) == 2:
                    if elem.find('db:products', ns) is not None:
                        products = elem.find('db:products', ns).findall('db:product', ns)
                        fda_app_num_list = list(
                            map(lambda p: element_value(p.find('db:fda-application-number', ns)), products))
                        fda_app_num_set = set(fda_app_num_list)
                        fda_app_num_set.discard('')
                        unique_fda_app_num_list = list(fda_app_num_set)
                    raw_df = raw_df.append({
                        'FDA_Application_Number': ','.join(unique_fda_app_num_list),
                        'Drug_Name': element_value(elem.find('db:name', ns)),
                        'DrugBank_ID': element_value(elem.find('db:drugbank-id', ns)),
                        'Indication': element_value(elem.find('db:indication', ns)),
                        'Pharmacodynamics': element_value(elem.find('db:pharmacodynamics', ns)),
                        'Mechanism_of_Action': element_value(elem.find('db:mechanism-of-action', ns)),
                        'Toxicity': element_value(elem.find('db:toxicity', ns)),
                        'Absorption': element_value(elem.find('db:absorption', ns)),
                        'Metabolism': element_value(elem.find('db:metabolism', ns)),
                        'Half_Life': element_value(elem.find('db:half-life', ns)),
                        'Route_of_Elimination': element_value(elem.find('db:route-of-elimination', ns)),
                        'Volume_of_Distribution': element_value(elem.find('db:volume-of-distribution', ns)),
                        'Clearance': element_value(elem.find('db:clearance', ns))
                    }, ignore_index=True)
                path.pop()
    return raw_df


def identifier_remap(raw_df):
    remap_df = raw_df.copy()
    new_row_df = pd.DataFrame()
    for index, row in remap_df.iterrows():
        if not pd.isna(row['FDA_Application_Number']):
            fda_app_num_list = row['FDA_Application_Number'].split(',')
            if len(fda_app_num_list) > 1:
                remap_df.at[index, 'FDA_Application_Number'] = fda_app_num_list[0]
                for i in range(1, len(fda_app_num_list)):
                    new_row = row.copy()
                    new_row['FDA_Application_Number'] = fda_app_num_list[i]
                    new_row_df = new_row_df.append(new_row)
    print('new_row_df: ' + str(len(new_row_df)))
    remap_df = remap_df.append(new_row_df)
    return remap_df


def merge(remap_df):
    no_appl_num = pd.isna(remap_df['FDA_Application_Number'])
    no_appl_num_df = remap_df[no_appl_num].copy()
    remap_df = remap_df[~no_appl_num]
    merge_df = remap_df.groupby('FDA_Application_Number').agg({
        'Drug_Name': ', '.join,
        'DrugBank_ID': ', '.join,
        'Indication': lambda r: combine_drug_name(remap_df.loc[r.index]['Drug_Name'],
                                                  remap_df.loc[r.index]['Indication']),
        'Pharmacodynamics': lambda r: combine_drug_name(remap_df.loc[r.index]['Drug_Name'],
                                                        remap_df.loc[r.index]['Pharmacodynamics']),
        'Mechanism_of_Action': lambda r: combine_drug_name(remap_df.loc[r.index]['Drug_Name'],
                                                           remap_df.loc[r.index]['Mechanism_of_Action']),
        'Toxicity': lambda r: combine_drug_name(remap_df.loc[r.index]['Drug_Name'],
                                                remap_df.loc[r.index]['Toxicity']),
        'Absorption': lambda r: combine_drug_name(remap_df.loc[r.index]['Drug_Name'],
                                                  remap_df.loc[r.index]['Absorption']),
        'Metabolism': lambda r: combine_drug_name(remap_df.loc[r.index]['Drug_Name'],
                                                  remap_df.loc[r.index]['Metabolism']),
        'Half_Life': lambda r: combine_drug_name(remap_df.loc[r.index]['Drug_Name'],
                                                 remap_df.loc[r.index]['Half_Life']),
        'Route_of_Elimination': lambda r: combine_drug_name(remap_df.loc[r.index]['Drug_Name'],
                                                            remap_df.loc[r.index]['Route_of_Elimination']),
        'Volume_of_Distribution': lambda r: combine_drug_name(remap_df.loc[r.index]['Drug_Name'],
                                                              remap_df.loc[r.index]['Volume_of_Distribution']),
        'Clearance': lambda r: combine_drug_name(remap_df.loc[r.index]['Drug_Name'],
                                                 remap_df.loc[r.index]['Clearance'])
    }).reset_index()
    merge_df = merge_df.append(no_appl_num_df)
    return merge_df


def split_nda(merge_df):
    merge_df = merge_df.replace(np.nan, '', regex=True)
    nda_pattern = r'^ANDA|^NDA'
    nda_filter = merge_df['FDA_Application_Number'].str.match(nda_pattern)
    nda_df = merge_df[nda_filter].copy()
    non_nda_df = merge_df[~nda_filter].copy()
    return nda_df, non_nda_df


def element_value(element):
    if element is not None and element.text is not None:
        return element.text
    return ''


def combine_drug_name(drug_name, value):
    return drug_name.str.cat(':\n' + value).str.cat(sep='\n\n')


if __name__ == '__main__':
    drugbank_raw_df = xml_to_csv()
    print('drugbank_raw_df: ' + str(len(drugbank_raw_df)))
    drugbank_raw_df.to_csv(FILE_PATH.DRUGBANK_RAW, index=False)

    drugbank_raw_df = pd.read_csv(FILE_PATH.DRUGBANK_RAW, dtype=str)
    drugbank_remap_df = identifier_remap(drugbank_raw_df)
    print('drugbank_remap_df: ' + str(len(drugbank_remap_df)))
    drugbank_remap_df.to_csv(FILE_PATH.DRUGBANK_REMAP, index=False)

    drugbank_remap_df = pd.read_csv(FILE_PATH.DRUGBANK_REMAP, dtype=str)
    drugbank_merge_df = merge(drugbank_remap_df)
    print('drugbank_merge_df: ' + str(len(drugbank_merge_df)))
    drugbank_merge_df.to_csv(FILE_PATH.DRUGBANK_REMAP, index=False)

    drugbank_merge_df = pd.read_csv(FILE_PATH.DRUGBANK_REMAP, dtype=str)
    drugbank_nda_df, drugbank_non_nda_df = split_nda(drugbank_merge_df)
    print('drugbank_nda_df: ' + str(len(drugbank_nda_df)))
    drugbank_nda_df.to_csv(FILE_PATH.DRUGBANK_PREPROCESS, index=False)
