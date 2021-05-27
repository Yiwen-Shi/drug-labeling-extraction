import pandas as pd
import requests
import pdftotext

from static.constants import FILE_PATH

if __name__ == '__main__':
    drugs_fda_df = pd.read_csv(FILE_PATH.DRUGSFDA_ORIGIN_DOCS, encoding="ISO-8859-1", delimiter='\t', dtype=str)
    drugs_fda_application_df = pd.read_csv(FILE_PATH.DRUGSFDA_ORIGIN_APPLICATION, encoding="ISO-8859-1", delimiter='\t', dtype=str)
    drugs_fda_df = pd.merge(drugs_fda_df, drugs_fda_application_df, how='left', on='ApplNo')
    drugs_fda_df['FullApplNo'] = drugs_fda_df.ApplType + drugs_fda_df.ApplNo
    drugs_fda_df.ApplicationDocsDate = pd.to_datetime(drugs_fda_df.ApplicationDocsDate).dt.date
    drugs_fda_label_df = drugs_fda_df[(drugs_fda_df.ApplicationDocsTypeID == '2') & (~drugs_fda_df.ApplicationDocsURL.isnull())]
    print(len(drugs_fda_label_df))

    label_content_df = pd.DataFrame(columns=['full_appl_no', 'fda_app_number', 'docs_date', 'pdf_url', 'pdf_content'])
    label_error_df = pd.DataFrame(columns=['full_appl_no', 'fda_app_number', 'docs_date', 'pdf_url'])
    count = 0
    for index, row in drugs_fda_label_df.iterrows():
        try:
            r = requests.get(row.ApplicationDocsURL)
            with open('templbl.pdf', 'wb') as fd:
                fd.write(r.content)
            f = open('templbl.pdf', 'rb')
            pdf = pdftotext.PDF(f)
            label_content_df = label_content_df.append({
                'full_appl_no': row.FullApplNo,
                'fda_app_number': row.ApplNo,
                'docs_date': row.ApplicationDocsDate,
                'pdf_url': row.ApplicationDocsURL,
                'pdf_content': "\n\n".join(pdf)
            }, ignore_index=True)
        except:
            label_error_df = label_error_df.append({
                'full_appl_no': row.FullApplNo,
                'fda_app_number': row.ApplNo,
                'docs_date': row.ApplicationDocsDate,
                'pdf_url': row.ApplicationDocsURL
            }, ignore_index=True)

        count += 1
        if count % 1000 == 0:
            label_content_df.to_csv(FILE_PATH.DRUGSFDA_RAW, index=False)
            label_error_df.to_csv(FILE_PATH.DRUGSFDA_ERROR, index=False)
            print('{} completed.{} {}'.format(str(count), str(len(label_content_df)), str(len(label_error_df))))

    label_content_df.to_csv(FILE_PATH.DRUGSFDA_RAW, index=False)
    label_error_df.to_csv(FILE_PATH.DRUGSFDA_ERROR, index=False)
    print('{} completed.{} {}'.format(str(count), str(len(label_content_df)), str(len(label_error_df))))
