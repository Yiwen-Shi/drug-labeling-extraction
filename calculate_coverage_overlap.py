import pandas as pd

if __name__ == '__main__':
    stat_df = pd.DataFrame(columns=['OrangeBook',
                                    'DailyMed', 'DailyMed_Coverage', 'DailyMed_Overlap',
                                    'DrugBank', 'DrugBank_Coverage', 'DrugBank_Overlap',
                                    'DrugsFDA', 'DrugsFDA_Coverage', 'DrugsFDA_Overlap'])

    full_info_df = pd.read_csv('full_info_df.csv', dtype=str)
    # print(len(full_info_df['ob_FDA_Application_Number'].dropna().tolist()))
    full_info_df = full_info_df[full_info_df['ob_FDA_Application_Number'].str.contains('^NDA') == True]

    Box_Warning_total = len(full_info_df[['dm_Box_Warning', 'df_Box_Warning']].dropna(how='all'))
    stat_df.loc['Box_Warning'] = [
        Box_Warning_total,
        len(full_info_df['dm_Box_Warning'].dropna()),
        len(full_info_df['dm_Box_Warning'].dropna()) / Box_Warning_total * 100,
        (full_info_df[full_info_df.dm_Box_Warning.notna()].box_warning_count.astype(float).mean() - 1) / 2 * 100,
        0,
        0,
        0,
        len(full_info_df.df_Box_Warning.dropna()),
        len(full_info_df.df_Box_Warning.dropna()) / Box_Warning_total * 100,
        (full_info_df[full_info_df.df_Box_Warning.notna()].box_warning_count.astype(float).mean() - 1) / 2 * 100
    ]

    indication_total = len(full_info_df[['dm_Indication', 'db_Indication', 'df_Indication']].dropna(how='all'))
    stat_df.loc['Indication'] = [
        indication_total,
        len(full_info_df.dm_Indication.dropna()),
        len(full_info_df.dm_Indication.dropna())/indication_total * 100,
        (full_info_df[full_info_df.dm_Indication.notna()].indication_count.astype(float).mean() - 1) / 2 * 100,
        len(full_info_df.db_Indication.dropna()),
        len(full_info_df.db_Indication.dropna())/indication_total * 100,
        (full_info_df[full_info_df.db_Indication.notna()].indication_count.astype(float).mean() - 1) / 2 * 100,
        len(full_info_df.df_Indication.dropna()),
        len(full_info_df.df_Indication.dropna()) / indication_total * 100,
        (full_info_df[full_info_df.df_Indication.notna()].indication_count.astype(float).mean() - 1) / 2 * 100
    ]

    Dosage_Administration_total = len(full_info_df[['dm_Dosage_Administration', 'df_Dosage_Administration']].dropna(how='all'))
    stat_df.loc['Dosage_Administration'] = [
        Dosage_Administration_total,
        len(full_info_df.dm_Dosage_Administration.dropna()),
        len(full_info_df.dm_Dosage_Administration.dropna()) / Dosage_Administration_total * 100,
        (full_info_df[full_info_df.dm_Dosage_Administration.notna()].dosage_admin_count.astype(float).mean() - 1) / 2 * 100,
        0,
        0,
        0,
        len(full_info_df.df_Dosage_Administration.dropna()),
        len(full_info_df.df_Dosage_Administration.dropna()) / Dosage_Administration_total * 100,
        (full_info_df[full_info_df.df_Dosage_Administration.notna()].dosage_admin_count.astype(float).mean() - 1) / 2 * 100
    ]

    Pregnancy_total = len(full_info_df[['dm_Pregnancy', 'df_Pregnancy']].dropna(how='all'))
    stat_df.loc['Pregnancy'] = [
        Pregnancy_total,
        len(full_info_df.dm_Pregnancy.dropna()),
        len(full_info_df.dm_Pregnancy.dropna()) / Pregnancy_total * 100,
        (full_info_df[full_info_df.dm_Pregnancy.notna()].pregnancy_count.astype(float).mean() - 1) / 2 * 100,
        0,
        0,
        0,
        len(full_info_df.df_Pregnancy.dropna()),
        len(full_info_df.df_Pregnancy.dropna()) / Pregnancy_total * 100,
        (full_info_df[full_info_df.df_Pregnancy.notna()].pregnancy_count.astype(float).mean() - 1) / 2 * 100
    ]

    Lactation_total = len(full_info_df[['dm_Lactation', 'df_Lactation']].dropna(how='all'))
    stat_df.loc['Lactation'] = [
        Lactation_total,
        len(full_info_df.dm_Lactation.dropna()),
        len(full_info_df.dm_Lactation.dropna()) / Lactation_total * 100,
        (full_info_df[full_info_df.dm_Lactation.notna()].lactation_count.astype(float).mean() - 1) / 2 * 100,
        0,
        0,
        0,
        len(full_info_df.df_Lactation.dropna()),
        len(full_info_df.df_Lactation.dropna()) / Lactation_total * 100,
        (full_info_df[full_info_df.df_Lactation.notna()].lactation_count.astype(float).mean() - 1) / 2 * 100
    ]

    mechanism_of_action_total = len(
        full_info_df[['dm_Mechanism_of_Action', 'db_Mechanism_of_Action', 'df_Mechanism_of_Action']].dropna(how='all'))
    stat_df.loc['Mechanism_of_Action'] = [
        mechanism_of_action_total,
        len(full_info_df.dm_Mechanism_of_Action.dropna()),
        len(full_info_df.dm_Mechanism_of_Action.dropna()) / mechanism_of_action_total * 100,
        (full_info_df[full_info_df.dm_Mechanism_of_Action.notna()].mechanism_of_action_count.astype(float).mean() - 1) / 2 * 100,
        len(full_info_df.db_Mechanism_of_Action.dropna()),
        len(full_info_df.db_Mechanism_of_Action.dropna()) / mechanism_of_action_total * 100,
        (full_info_df[full_info_df.db_Mechanism_of_Action.notna()].mechanism_of_action_count.astype(float).mean() - 1) / 2 * 100,
        len(full_info_df.df_Mechanism_of_Action.dropna()),
        len(full_info_df.df_Mechanism_of_Action.dropna()) / mechanism_of_action_total * 100,
        (full_info_df[full_info_df.df_Mechanism_of_Action.notna()].mechanism_of_action_count.astype(float).mean() - 1) / 2 * 100
    ]

    pharmacodynamics_total = len(full_info_df[['dm_Pharmacodynamics', 'db_Pharmacodynamics', 'df_Pharmacodynamics']].dropna(how='all'))
    stat_df.loc['Pharmacodynamics'] = [
        pharmacodynamics_total,
        len(full_info_df.dm_Pharmacodynamics.dropna()),
        len(full_info_df.dm_Pharmacodynamics.dropna())/pharmacodynamics_total * 100,
        (full_info_df[full_info_df.dm_Pharmacodynamics.notna()].pharmacodynamics_count.astype(float).mean() - 1) / 2 * 100,
        len(full_info_df.db_Pharmacodynamics.dropna()),
        len(full_info_df.db_Pharmacodynamics.dropna())/pharmacodynamics_total * 100,
        (full_info_df[full_info_df.db_Pharmacodynamics.notna()].pharmacodynamics_count.astype(float).mean() - 1) / 2 * 100,
        len(full_info_df.df_Pharmacodynamics.dropna()),
        len(full_info_df.df_Pharmacodynamics.dropna()) / pharmacodynamics_total * 100,
        (full_info_df[full_info_df.df_Pharmacodynamics.notna()].pharmacodynamics_count.astype(float).mean() - 1) / 2 * 100
    ]

    absorption_total = len(full_info_df[['dm_Absorption', 'db_Absorption', 'df_Absorption']].dropna(how='all'))
    stat_df.loc['Absorption'] = [
        absorption_total,
        len(full_info_df.dm_Absorption.dropna()),
        len(full_info_df.dm_Absorption.dropna())/absorption_total * 100,
        (full_info_df[full_info_df.dm_Absorption.notna()].absorption_count.astype(float).mean() - 1) / 2 * 100,
        len(full_info_df.db_Absorption.dropna()),
        len(full_info_df.db_Absorption.dropna())/absorption_total * 100,
        (full_info_df[full_info_df.db_Absorption.notna()].absorption_count.astype(float).mean() - 1) / 2 * 100,
        len(full_info_df.df_Absorption.dropna()),
        len(full_info_df.df_Absorption.dropna()) / absorption_total * 100,
        (full_info_df[full_info_df.df_Absorption.notna()].absorption_count.astype(float).mean() - 1) / 2 * 100
    ]
    food_effect_total = len(full_info_df[['dm_Food_Effect', 'df_Food_Effect']].dropna(how='all'))
    stat_df.loc['Food_Effect'] = [
        food_effect_total,
        len(full_info_df.dm_Food_Effect.dropna()),
        len(full_info_df.dm_Food_Effect.dropna()) / food_effect_total * 100,
        (full_info_df[full_info_df.dm_Food_Effect.notna()].food_effect_count.astype(float).mean() - 1) / 2 * 100,
        0,
        0,
        0,
        len(full_info_df.df_Food_Effect.dropna()),
        len(full_info_df.df_Food_Effect.dropna()) / food_effect_total * 100,
        (full_info_df[full_info_df.df_Food_Effect.notna()].food_effect_count.astype(float).mean() - 1) / 2 * 100
    ]
    distribution_total = len(full_info_df[['dm_Distribution', 'db_Volume_of_Distribution', 'df_Distribution']].dropna(how='all'))
    stat_df.loc['Distribution'] = [
        distribution_total,
        len(full_info_df.dm_Distribution.dropna()),
        len(full_info_df.dm_Distribution.dropna())/distribution_total * 100,
        (full_info_df[full_info_df.dm_Distribution.notna()].distribution_count.astype(float).mean() - 1) / 2 * 100,
        len(full_info_df.db_Volume_of_Distribution.dropna()),
        len(full_info_df.db_Volume_of_Distribution.dropna())/distribution_total * 100,
        (full_info_df[full_info_df.db_Volume_of_Distribution.notna()].distribution_count.astype(float).mean() - 1) / 2 * 100,
        len(full_info_df.df_Distribution.dropna()),
        len(full_info_df.df_Distribution.dropna()) / distribution_total * 100,
        (full_info_df[full_info_df.df_Distribution.notna()].distribution_count.astype(float).mean() - 1) / 2 * 100,
    ]
    metabolism_total = len(full_info_df[['dm_Metabolism', 'db_Metabolism', 'df_Metabolism']].dropna(how='all'))
    stat_df.loc['Metabolism'] = [
        metabolism_total,
        len(full_info_df.dm_Metabolism.dropna()),
        len(full_info_df.dm_Metabolism.dropna())/metabolism_total * 100,
        (full_info_df[full_info_df.dm_Metabolism.notna()].metabolism_count.astype(float).mean() - 1) / 2 * 100,
        len(full_info_df.db_Metabolism.dropna()),
        len(full_info_df.db_Metabolism.dropna())/metabolism_total * 100,
        (full_info_df[full_info_df.db_Metabolism.notna()].metabolism_count.astype(float).mean() - 1) / 2 * 100,
        len(full_info_df.df_Metabolism.dropna()),
        len(full_info_df.df_Metabolism.dropna()) / metabolism_total * 100,
        (full_info_df[full_info_df.df_Metabolism.notna()].metabolism_count.astype(float).mean() - 1) / 2 * 100,
    ]
    excretion_total = len(full_info_df[['dm_Excretion', 'db_Route_of_Elimination', 'df_Excretion']].dropna(how='all'))
    stat_df.loc['Excretion'] = [
        excretion_total,
        len(full_info_df.dm_Excretion.dropna()),
        len(full_info_df.dm_Excretion.dropna())/excretion_total * 100,
        (full_info_df[full_info_df.dm_Excretion.notna()].excretion_count.astype(float).mean() - 1) / 2 * 100,
        len(full_info_df.db_Route_of_Elimination.dropna()),
        len(full_info_df.db_Route_of_Elimination.dropna())/excretion_total * 100,
        (full_info_df[full_info_df.db_Route_of_Elimination.notna()].excretion_count.astype(float).mean() - 1) / 2 * 100,
        len(full_info_df.df_Excretion.dropna()),
        len(full_info_df.df_Excretion.dropna()) / excretion_total * 100,
        (full_info_df[full_info_df.df_Excretion.notna()].excretion_count.astype(float).mean() - 1) / 2 * 100
    ]

    drug_total = len(full_info_df[['dm_FDA_Application_Number', 'db_FDA_Application_Number', 'df_FDA_Application_Number']].dropna(how='all'))
    stat_df.loc['drug'] = [
        drug_total,
        len(full_info_df['dm_FDA_Application_Number'].dropna()),
        len(full_info_df['dm_FDA_Application_Number'].dropna()) / drug_total * 100,
        (full_info_df[full_info_df['dm_FDA_Application_Number'].notna()].drug_count.astype(float).mean() - 1) / 2 * 100,
        len(full_info_df['db_FDA_Application_Number'].dropna()),
        len(full_info_df['db_FDA_Application_Number'].dropna()) / drug_total * 100,
        (full_info_df[full_info_df['db_FDA_Application_Number'].notna()].drug_count.astype(float).mean() - 1) / 2 * 100,
        len(full_info_df['df_FDA_Application_Number'].dropna()),
        len(full_info_df['df_FDA_Application_Number'].dropna()) / drug_total * 100,
        (full_info_df[full_info_df['df_FDA_Application_Number'].notna()].drug_count.astype(float).mean() - 1) / 2 * 100
    ]

    stat_df.to_csv('stat_df.csv', index=True)
