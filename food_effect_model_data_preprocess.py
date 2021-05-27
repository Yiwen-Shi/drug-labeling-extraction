import re
import pandas as pd

if __name__ == '__main__':
    full_info_df = pd.read_csv('full_info_df.csv', dtype=str)
    food_training_df = pd.DataFrame(columns=['FDA_Application_Number', 'Data_Source', 'Topic', 'Paragraph'])

    df_food_effect_df = full_info_df.loc[
    full_info_df['df_Food_Effect'].notna(), ['df_FDA_Application_Number', 'df_Food_Effect']].copy()
    df_food_effect_df.columns = df_food_effect_df.columns.str.lstrip('df_')
    df_food_effect_df['Topic'] = 'Food Effect'
    df_food_effect_df['Data_Source'] = 'DrugsFDA'
    df_food_effect_df.rename(columns={'Food_Effect': 'Paragraph'}, inplace=True)
    food_training_df = food_training_df.append(df_food_effect_df)
    print(len(df_food_effect_df))

    df_absorption_df = full_info_df[(full_info_df['df_Absorption'].notna())].copy()
    df_absorption_df = df_absorption_df[['df_FDA_Application_Number', 'df_Absorption']]
    df_absorption_df.columns = df_absorption_df.columns.str.lstrip('df_')
    df_absorption_df['Topic'] = 'Non Food Effect'
    df_absorption_df['Data_Source'] = 'DrugsFDA'
    df_absorption_df.rename(columns={'Absorption': 'Paragraph'}, inplace=True)
    food_training_df = food_training_df.append(df_absorption_df)
    print(len(df_absorption_df))

    dm_food_effect_df = full_info_df.loc[full_info_df['dm_Food_Effect'].notna(), ['dm_FDA_Application_Number', 'dm_Food_Effect']].copy()
    dm_food_effect_df.columns = dm_food_effect_df.columns.str.lstrip('dm_')
    dm_food_effect_df['Topic'] = 'Food Effect'
    dm_food_effect_df['Data_Source'] = 'DailyMed'
    dm_food_effect_df.rename(columns={'Food_Effect': 'Paragraph'}, inplace=True)
    food_training_df = food_training_df.append(dm_food_effect_df)
    print(len(dm_food_effect_df))

    dm_absorption_df = full_info_df[(full_info_df['dm_Absorption'].notna())].copy()
    dm_absorption_df = dm_absorption_df[['dm_FDA_Application_Number', 'dm_Absorption']]
    dm_absorption_df.columns = dm_absorption_df.columns.str.lstrip('dm_')
    dm_absorption_df['Topic'] = 'Non Food Effect'
    dm_absorption_df['Data_Source'] = 'DailyMed'
    dm_absorption_df.rename(columns={'Absorption': 'Paragraph'}, inplace=True)
    food_training_df = food_training_df.append(dm_absorption_df)
    print(food_training_df[['Topic', 'Data_Source']].value_counts())

    for index, row in food_training_df.iterrows():
        paragraph_list = row['Paragraph'].split('\n')
        paragraph_list = list(filter(len, paragraph_list))
        paragraph = paragraph_list[0]
        paragraph = re.sub(r'\\x..', ' ', paragraph)
        paragraph = re.sub(r'\\t', ' ', paragraph)
        paragraph = ' '.join(paragraph.split())
        if paragraph and paragraph[-1] == '.':
            row['Paragraph'] = paragraph.lower()
        else:
            row['Paragraph'] = ''

    food_training_df = food_training_df[food_training_df['Paragraph'].str.len() > 0]
    food_training_df = food_training_df.drop_duplicates(subset=['Paragraph'], keep='first')
    food_training_df[['Topic', 'Data_Source','Paragraph']].to_csv('food_training_df.csv', index=False)