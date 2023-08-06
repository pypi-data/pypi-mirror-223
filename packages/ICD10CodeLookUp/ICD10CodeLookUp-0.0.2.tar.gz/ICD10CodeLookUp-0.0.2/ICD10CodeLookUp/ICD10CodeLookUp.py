import pandas as pd
import numpy as np

class DiagnosisCodeLookUp:
    def __init__(self):
        data_file = 'https://raw.githubusercontent.com/famutimine/ICD10CodeLookUp/main/diagnosis_codes_lookup.csv'
        self.df = pd.read_csv(data_file)  # Load the ICD10 diagnosis code data from a default CSV file in the GitHub repo

    def search_by_keyword(self, keyword):
        keyword = keyword.lower()
        matching_rows = self.df[self.df['ccsr_category_description'].str.lower().str.contains(keyword)]
        codes = matching_rows['icd_10_cm_code'].tolist()
        return codes

    def get_mapping_dataframe(self, keyword):
        keyword = keyword.lower()
        mapped = self.df[self.df['ccsr_category_description'].str.lower().str.contains(keyword)]
        mapped.reset_index(drop=True,inplace=True)
        return mapped

    def get_mapping_tuple_list(self, keyword):
        keyword = keyword.lower()
        mapped_tuple = self.df[self.df['ccsr_category_description'].str.lower().str.contains(keyword)]
        mapped_tuple = mapped_tuple.drop('ccsr_category_description', axis=1)
        mapped_tuple.reset_index(drop=True,inplace=True)
        return list(mapped_tuple.itertuples(index=False, name='DiseaseCode'))