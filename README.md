# Drug Labeling Retrieval Application
## Install dependencies
```console
pip install -r requirements.txt
```

### Data Source files
 Data Source | Data File Name | File Path | Download Website |
| -----------| ----------- | ----------- | ----------- |
| OrangeBook | products.txt | /datafiles/orangebook | https://www.fda.gov/drugs/drug-approvals-and-databases/orange-book-data-files |
| DailyMed   | dm_spl_zip_files_meta_data.txt | /datafiles/dailymed | https://dailymed.nlm.nih.gov/dailymed/spl-resources-all-mapping-files.cfm |
| DrugBank   | fulldatabase.xml | /datafiles/drugbank | https://go.drugbank.com/releases/latest |
| Drugs@FDA  | ApplicationDocs.txt<br />Applications.txt | /datafiles/drugsfda | https://www.fda.gov/drugs/drug-approvals-and-databases/drugsfda-data-files |

## Data Collection
### DailyMed
```console
python dailymed_data_collection.py
```
### Drugs@FDA
```console
python drugsfda_data_collection.py
```
### DrugBank
Download full database from https://go.drugbank.com/releases/latest
## Data Preprocess
### DailyMed
```console
python dailymed_preprocess.py
```
### Drugs@FDA
```console
python drugsfda_preprocess.py
```
### DrugBank
```console
python drugbank_preprocess.py
```

## Comparison of Source Coverage and Overlap of Unique Drug and Drug Labeling Sections 
Combine Drug Information from Multiple Data Sources and Basic Statistics
```console
python multi_data_source_combine.py
```
Calculate Data Source Coverage and Overlap
```console
python calculate_coverage_overlap.py
```


## Food Effect Classification Model
### Data Preprocessing
```console
python food_effect_model_data_preprocess.py
```
### Model Training & Evaluation
Run
`food_model.ipynb` and `food_model_bert.ipynb`

