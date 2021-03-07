#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import pandas as pd
import re
import requests
import io
import os
import _locale

_locale._getdefaultlocale = (lambda *args: ['en_US', 'UTF-8'])#for avoiding encoding errors


from googleads import adwords


output = io.StringIO()

adwords_client = adwords.AdWordsClient.LoadFromStorage('googleads.yaml') #the file contains 4 arguments: client_id,client_secret,developer_token and refresh_token)

report_downloader = adwords_client.GetReportDownloader(version='v201809')

report_query = (adwords.ReportQueryBuilder()
                .Select('AccountDescriptiveName', 'CampaignName', 'AttributeValues')
                # .Select('AdGroupName')
                .From('PLACEHOLDER_FEED_ITEM_REPORT')
                .Where('Status').In('ENABLED')
                #.During('LAST_7_DAYS')
                .During('TODAY')
                .Build())

# You can provide a file object to write the output to. For this
# demonstration we use sys.stdout to write the report to the screen.
report_downloader.DownloadReportWithAwql(
    report_query,
    'CSV',
    output,
    client_customer_id='***-***-****',  # denotes which ads account to pull from
    skip_report_header=True,
    skip_column_header=False,
    skip_report_summary=True,
    include_zero_impressions=False)

output.seek(0)

df1 = pd.read_csv(output)
# df1

df1.columns = ['Account', 'Campaign', 'Exten']
df1['raw_Link'] = [re.search("(?P<url>https?://[^\s]+)", n) for n in df1['Exten']]
df1_without_none = df1[df1['Exten'].str.contains('http', regex=True, na=False)]
# df1_without_none.head()
df1_without_none['Links'] = [i.group(0) for i in df1_without_none['raw_Link']]
df1_without_none['Links'] = df1_without_none['Links'].str.split('"').str[0]


uniq = df1_without_none['Links'].unique()
df_uniq_links = pd.DataFrame(uniq)
df_uniq_links.columns = ['uniq']

#start a loop to check the links
links = []
n = 1
for url in df_uniq_links['uniq']:
    r = requests.head(url)
    df = pd.DataFrame({'Links': [url], 'Codes': [r.status_code]})
    print('Checked: ' + str(n) + ' from ' + str(len(df_uniq_links['uniq'])) + ' SiteLinks.' ' Status: ' + str(
        r.status_code))

    n += 1
    # time.sleep(5)

    links.append(df)

df_uniq_links_code = pd.concat(links, ignore_index=True)
df_joined = pd.merge(df1_without_none, df_uniq_links_code, how='left', on='Links')
df_final = df_joined.filter(items=['Account', 'Campaign', 'Exten', 'Links', 'Codes'])
#final_df

#write the df to an excel file
writer = pd.ExcelWriter('Bad_links.xlsx', engine='xlsxwriter')    
df_final.to_excel(writer,'Links', index=False)
writer.save()

print('')
print('Done!')

