import pandas as pd
import numpy as np

from static.constants import FILE_PATH


def count_not_nan(row, columns):
    return row[columns].count()


if __name__ == '__main__':
    fda_app_num_df = pd.DataFrame(columns=['ID'])
    full_info_df = pd.DataFrame(columns=['ID'])

    # Orange Book
    ob_raw_df = pd.read_csv(FILE_PATH.ORANGE_BOOK_ORIGIN, delimiter='~', dtype=str)
    print('OrangeBook Initial: ' + str(len(ob_raw_df)))
    ob_raw_df['Full_Appl_No'] = np.where(ob_raw_df.Appl_Type == 'N', 'NDA' + ob_raw_df.Appl_No, 'ANDA' + ob_raw_df.Appl_No)
    ob_raw_df = ob_raw_df.sort_values(['Full_Appl_No'], ascending=True).reset_index(drop=True)
    ob_unique_df = ob_raw_df.drop_duplicates(subset=['Full_Appl_No'], keep='first')
    ob_unique_df = ob_unique_df[['Full_Appl_No']].copy()
    ob_unique_df['ID'] = ob_unique_df['Full_Appl_No']
    ob_unique_df = ob_unique_df.rename(columns={'Full_Appl_No': 'ob_FDA_Application_Number'})
    print('OrangeBook Filtered: ' + str(len(ob_unique_df)))
    full_info_df = ob_unique_df[['ID']].copy()
    full_info_df = pd.merge(full_info_df, ob_unique_df, how='left', on='ID')

    # DailyMed
    dm_origin_df = pd.read_csv(FILE_PATH.DAILYMED_ORIGIN, delimiter='|')
    print('DailyMed Initial: ' + str(len(dm_origin_df)))
    dm_accessible_df = pd.read_csv(FILE_PATH.DAILYMED_RAW)
    print('DailyMed Accessible: ' + str(len(dm_accessible_df)))
    dm_remap_df = pd.read_csv(FILE_PATH.DAILYMED_REMAP)
    print('DailyMed Remap: ' + str(len(dm_remap_df)))
    dm_df = pd.read_csv(FILE_PATH.DAILYMED_PREPROCESS)
    print('DailyMed Preprocess: ' + str(len(dm_df)))
    dm_df = dm_df.add_prefix('dm_')
    dm_df['ID'] = dm_df['dm_FDA_Application_Number']
    full_info_df = pd.merge(full_info_df, dm_df, how='left', on='ID')

    # DrugBank
    db_remap_df = pd.read_csv(FILE_PATH.DRUGBANK_REMAP)
    print('DrugBank Remap: ' + str(len(db_remap_df)))
    db_df = pd.read_csv(FILE_PATH.DRUGBANK_PREPROCESS)
    print('DrugBank Preprocess: ' + str(len(db_df)))
    db_df = db_df.add_prefix('db_')
    db_df['ID'] = db_df['db_FDA_Application_Number']
    full_info_df = pd.merge(full_info_df, db_df, how='left', on='ID')

    # Drugs@FDA
    drugs_fda_initial_df = pd.read_csv(FILE_PATH.DRUGSFDA_ORIGIN_DOCS, encoding="ISO-8859-1", delimiter='\t', dtype=str)
    drugs_fda_initial_df = drugs_fda_initial_df[drugs_fda_initial_df.ApplicationDocsTypeID == '2']
    print('Drugs@FDA Initial: ' + str(len(drugs_fda_initial_df)))
    drugs_fda_accessible_df = pd.read_csv(FILE_PATH.DRUGSFDA_RAW)
    print('Drugs@FDA Accessible: ' + str(len(drugs_fda_accessible_df)))
    df_df = pd.read_csv(FILE_PATH.DRUGSFDA_PREPROCESS)
    print('Drugs@FDA Preprocess: ' + str(len(df_df)))
    df_df = df_df.add_prefix('df_')
    df_df['ID'] = df_df['df_full_appl_no']
    df_df = df_df.rename(columns={'df_full_appl_no': 'df_FDA_Application_Number'})
    full_info_df = pd.merge(full_info_df, df_df, how='left', on='ID')

    full_info_df['drug_count'] = full_info_df.apply(
        lambda x: x[['dm_FDA_Application_Number', 'db_FDA_Application_Number', 'df_FDA_Application_Number']].count(), axis=1)

    full_info_df['box_warning_count'] = full_info_df.apply(
        lambda x: x[['dm_Box_Warning', 'df_Box_Warning']].count(), axis=1)
    full_info_df['indication_count'] = full_info_df.apply(
        lambda x: x[['dm_Indication', 'db_Indication', 'df_Indication']].count(), axis=1)
    full_info_df['dosage_admin_count'] = full_info_df.apply(
        lambda x: x[['dm_Dosage_Administration', 'df_Dosage_Administration']].count(), axis=1)
    full_info_df['pregnancy_count'] = full_info_df.apply(
        lambda x: x[['dm_Pregnancy', 'df_Pregnancy']].count(), axis=1)
    full_info_df['lactation_count'] = full_info_df.apply(
        lambda x: x[['dm_Lactation', 'df_Lactation']].count(), axis=1)
    full_info_df['mechanism_of_action_count'] = full_info_df.apply(
        lambda x: x[['dm_Mechanism_of_Action', 'db_Mechanism_of_Action', 'df_Mechanism_of_Action']].count(), axis=1)
    full_info_df['pharmacodynamics_count'] = full_info_df.apply(
        lambda x: x[['dm_Pharmacodynamics', 'db_Pharmacodynamics', 'df_Pharmacodynamics']].count(), axis=1)
    full_info_df['information_for_patients_count'] = full_info_df.apply(
        lambda x: x[['dm_Information_for_Patients', 'df_Information_for_Patients']].count(), axis=1)

    full_info_df['absorption_count'] = full_info_df.apply(
        lambda x: x[['dm_Absorption', 'db_Absorption', 'df_Absorption']].count(), axis=1)
    full_info_df['distribution_count'] = full_info_df.apply(
        lambda x: x[['dm_Distribution', 'db_Volume_of_Distribution', 'df_Distribution']].count(), axis=1)
    full_info_df['metabolism_count'] = full_info_df.apply(
        lambda x: x[['dm_Metabolism', 'db_Metabolism', 'df_Metabolism']].count(), axis=1)
    full_info_df['excretion_count'] = full_info_df.apply(
        lambda x: x[['dm_Excretion', 'db_Route_of_Elimination', 'df_Excretion']].count(), axis=1)
    full_info_df['food_effect_count'] = full_info_df.apply(
        lambda x: x[['dm_Food_Effect', 'df_Food_Effect']].count(), axis=1)

    print('full_info_df: ' + str(len(full_info_df)))
    full_info_df.to_csv('full_info_df.csv', index=False)
