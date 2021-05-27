import os


class FILE_PATH:
    ORANGE_BOOK_ORIGIN = os.path.join(os.path.dirname(__file__), '../datafiles/orangebook/products.txt')

    DAILYMED_ORIGIN = os.path.join(os.path.dirname(__file__), '../datafiles/dailymed/dm_spl_zip_files_meta_data.txt')
    DAILYMED_RAW = os.path.join(os.path.dirname(__file__), '../datafiles/dailymed/dailymed_raw.csv')
    DAILYMED_ERROR = os.path.join(os.path.dirname(__file__), '../datafiles/dailymed/dailymed_error.csv')
    DAILYMED_SPL = os.path.join(os.path.dirname(__file__), '../datafiles/dailymed/dailymed_spl.csv')
    DAILYMED_REMAP = os.path.join(os.path.dirname(__file__), '../datafiles/dailymed/dailymed_remap.csv')
    DAILYMED_MAPPING = os.path.join(os.path.dirname(__file__), '../datafiles/dailymed/dailymed_mapping.csv')
    DAILYMED_PREPROCESS = os.path.join(os.path.dirname(__file__), '../datafiles/dailymed/dailymed_preprocess.csv')

    DRUGBANK_ORIGIN = os.path.join(os.path.dirname(__file__), '../datafiles/drugbank/fulldatabase.xml')
    DRUGBANK_RAW = os.path.join(os.path.dirname(__file__), '../datafiles/drugbank/drugbank_raw.csv')
    DRUGBANK_REMAP = os.path.join(os.path.dirname(__file__), '../datafiles/drugbank/drugbank_remap.csv')
    DRUGBANK_MERGE = os.path.join(os.path.dirname(__file__), '../datafiles/drugbank/drugbank_merge.csv')
    DRUGBANK_PREPROCESS = os.path.join(os.path.dirname(__file__), '../datafiles/drugbank/drugbank_preprocess.csv')

    DRUGSFDA_ORIGIN_DOCS = os.path.join(os.path.dirname(__file__), '../datafiles/drugsfda/ApplicationDocs.txt')
    DRUGSFDA_ORIGIN_APPLICATION = os.path.join(os.path.dirname(__file__), '../datafiles/drugsfda/Applications.txt')
    DRUGSFDA_RAW = os.path.join(os.path.dirname(__file__), '../datafiles/drugsfda/drugs_fda_raw.csv')
    DRUGSFDA_ERROR = os.path.join(os.path.dirname(__file__), '../datafiles/drugsfda/drugs_fda_error.csv')
    DRUGSFDA_PREPROCESS = os.path.join(os.path.dirname(__file__), '../datafiles/drugsfda/drugs_fda_preprocess.csv')


class URL:
    DAILYMED_SPL = 'https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/'
    DAILYMED_APPLICATION_NUMBER = 'https://dailymed.nlm.nih.gov/dailymed/services/v2/applicationnumbers.xml?setid='
    DAILYMED_PREFIX = 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid='
