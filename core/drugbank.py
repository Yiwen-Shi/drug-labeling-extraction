import pandas as pd

from static.constants import FILE_PATH


class DrugBank:
    def __init__(self, fda_app_num):
        self.FDA_Application_Number = None
        db_df = pd.read_csv(FILE_PATH.DRUGBANK_PREPROCESS, dtype=str)
        db_df = db_df.fillna('')
        row_df = db_df.loc[db_df['FDA_Application_Number'] == fda_app_num]
        if row_df.shape[0] > 0:
            row = row_df.iloc[0]
            self.FDA_Application_Number = row.FDA_Application_Number
            self.Drug_Name = row.Drug_Name
            self.DrugBank_ID = row.DrugBank_ID
            self.Indication = row.Indication
            self.Pharmacodynamics = row.Pharmacodynamics
            self.Mechanism_of_Action = row.Mechanism_of_Action
            self.Toxicity = row.Toxicity
            self.Absorption = row.Absorption
            self.Metabolism = row.Metabolism
            self.Half_Life = row.Half_Life
            self.Route_of_Elimination = row.Route_of_Elimination
            self.Volume_of_Distribution = row.Volume_of_Distribution
            self.Clearance = row.Clearance
