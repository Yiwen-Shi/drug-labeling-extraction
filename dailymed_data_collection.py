import pandas as pd
import requests

from static.constants import URL, FILE_PATH

if __name__ == '__main__':
    dm_metadata_df = pd.read_csv(FILE_PATH.DAILYMED_ORIGIN, delimiter='|', dtype=str)
    print(len(dm_metadata_df))
    spl_df = pd.DataFrame(columns=['SETID', 'SPL'])
    error_df = pd.DataFrame(columns=['SETID'])
    for index, row in dm_metadata_df.iterrows():
        try:
            r = requests.get(url=URL.DAILYMED_SPL + row.SETID + '.xml')
            spl_df = spl_df.append({
                'SETID': row.SETID,
                'SPL': r.content
            }, ignore_index=True)
        except:
            print("cannot get SPL for SETID %s." % row.SETID)
            error_df = error_df.append({'SETID': row.SETID}, ignore_index=True)
            continue

        if (index + 1) % 5000 == 0:
            print('{} completed.{} {}'.format(str(index + 1), str(len(spl_df)), str(len(error_df))))
            spl_df.to_csv(FILE_PATH.DAILYMED_RAW, index=False)
            error_df.to_csv(FILE_PATH.DAILYMED_ERROR, index=False)

    print(len(spl_df))
    spl_df.to_csv(FILE_PATH.DAILYMED_RAW, index=False)
    print(len(error_df))
    error_df.to_csv(FILE_PATH.DAILYMED_ERROR, index=False)
