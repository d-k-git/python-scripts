## Script for parsing old dates in different Yandex.Direct ad blocks


%%time
import datetime
import re
import pandas as pd

import numpy as np
from datesdict23 import d1_month  #dict on months
from datesdict23 import d2_days   #dict of days
import time
from time import sleep
from pyaspeller import YandexSpeller

import locale
import sys
import _locale

import configparser  

import requests
   
_locale._getdefaultlocale = (lambda *args: ['en_US', 'UTF-8'])


LOGIN = str(input('Enter your advertising login in Yandex.Direct without a space: '))
print('')
SPREADSHEETKEY =  str(input('Enter Google Spreadsheet id: '))
print('')
print('Go!')


#Display the date if it has already passed or is coming tomorrow: 
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days = 1)
tomorrow2 = tomorrow.strftime('%Y-%m-%d')


# If the date is 2 months later than the current one  qualify it as suspicious. To catch the November-December dates at the beginning of the year
from dateutil import relativedelta
nextmonth = datetime.date.today() + relativedelta.relativedelta(months=2)
nextmonth2 = nextmonth.strftime('%Y-%m')


#The main function - to search the dictionaries d2_days and d1_month for dates extracted from ads:

def find_matches2(d2_days, d1_month, item):
    for k in d2_days:
        if re.match(k, item):
            return d2_days[k]        
    for k in d1_month:
        if re.match(k, item):
            return d1_month[k]

        
#To display parsing timeа
from datetime import datetime

my_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
df_time = pd.DataFrame({'': [my_time]})
df_mytime =  df_time.to_string(index=False, header=False)    

FIND_DATES = "\sянв|\sфев|\sмар|\sапр|\sмая|\sмае|\sмай|\sиюн|\sиюл|\sавг|\sсент|\sокт|\sнояб|\sдек|\s[0-9].\.01|\s[0-9].\.02|\s[0-9]..03|\s[0-9].\.04|\s[0-9].\.05|\s[0-9].\.06|\s[0-9].\.07|\s[0-9].\.08|\s[0-9].\.09|\s[0-9].\.10|\s[0-9].\.11|\s[0-9].\.12"
CUT_DATES = "([0-9]..янв[а-я]*|[0-9]..фев[а-я]*|[0-9]..мар[а-я]*|[0-9]..апр[а-я]*|[0-9]..мая|мае|[0-9]..май[а-я]*|[0-9]..июн[а-я]*|[0-9]..июл[а-я]*|[0-9]..авг[а-я]*|[0-9]..сент[а-я]*|[0-9]..окт[а-я]*|[0-9]..нояб[а-я]*|[0-9]..дек[а-я]*|\sянв[а-я]*|\sфев[а-я]*|\sмар[а-я]*|\sапр[а-я]*|\sмая|мае|май[а-я]*|\sиюн[а-я]*|\sиюл[а-я]*|\sавг[а-я]*|\sсент[а-я]*|\sокт[а-я]*|\sнояб[а-я]*|\sдек[а-я]*|[0-9].\.01|[0-9].\.02|[0-9]..03|[0-9].\.04|[0-9].\.05|[0-9].\.06|[0-9].\.07|[0-9].\.08|[0-9].\.09|[0-9].\.10|[0-9].\.11|[0-9].\.12)"



config = configparser.ConfigParser()  
config.read("config1.ini")  

access_token = config["auth"]["token"]

login = LOGIN


### Get a list of enabled text campaigns




url = 'https://api.direct.yandex.com/json/v5/campaigns'

headers = { 
    'Authorization': f'Bearer {access_token}', 
    'Client-Login' : login,
    "Accept-Language": "ru",
    "skipReportHeader": "true",
    "skipReportSummary": "true",
    "Use-Operator-Units": "true"  
}

body = {
  "method": "get",
  "params": { 
    "SelectionCriteria": { 
    "Types": ["TEXT_CAMPAIGN"],
    "States": ["ON"],
    #"States": ["ON","SUSPENDED","OFF","ENDED"],
    }, 
    "FieldNames" : ["Id" , "Name", "State" , "Status", "Type"]
  } 
}


status = None

while status in {201, 202, None}:
    res = requests.post(url, headers=headers, json=body)
    status = res.status_code
    retryIn = res.headers.get('retryIn', None)
    reportsInQueue = res.headers.get('reportsInQueue', None)
    #print(f'status = {status} wait {retryIn}. queue {reportsInQueue}')
    
    if retryIn:
        sleep(int(retryIn))

campaign_dict = {}

try:
    for camp in res.json()['result']['Campaigns']:
        for key in camp:
            if key not in campaign_dict:
                campaign_dict[key] = []
                campaign_dict[key].append(camp[key])
            else:
                campaign_dict[key].append(camp[key])

    camp_df = pd.DataFrame(campaign_dict)
    camp_df
    
except KeyError:
    print(res.json()['error']['error_detail'])





camp_df


### All ads from all campaigns




campaigns = camp_df['Id'].unique().tolist()





ads_dict = {}

n = 1

for camp in campaigns:
    print(f'CampaignId: {camp}, {n}/{len(campaigns)}')
    
    url = 'https://api.direct.yandex.com/json/v5/ads'
    
    body = {
          "method": "get",
          "params": { 
            "SelectionCriteria": { 

                "CampaignIds" : [camp]

            }, 
            "FieldNames" : [ "Id" , "State", "CampaignId"] ,
             "TextAdFieldNames": ["Text" , "Title" , "Title2",
                                  "AdExtensions", "SitelinkSetId",
                                  "SitelinksModeration"],


          } 
        } 


    

    status = None
    while status in {201, 202, None}:
        res = requests.post(url, headers=headers, json=body)
        status = res.status_code
        retryIn = res.headers.get('retryIn', None)
        reportsInQueue = res.headers.get('reportsInQueue', None)
        if retryIn:
            sleep(int(retryIn))

    try:
        for ad in res.json()['result']['Ads']:
            if 'TextAd' in ad:
                for key in ad:

                    if key not in ads_dict:
                        ads_dict[key] = []
                        ads_dict[key].append(ad[key])


                    else:
                        ads_dict[key].append(ad[key])
            else:
                continue
                
                
    except KeyError:
        continue
    
    n += 1
            


ads_df = pd.DataFrame(ads_dict)
print(f'\nNumber of Ads: {len(ads_df)}')

ads_df.head()





ads_df = ads_df[ads_df['State'] == 'ON'][['Id','TextAd','CampaignId']] 
# ads_df = ads_df[['Id','TextAd','CampaignId']] # Все
print(f'Number of active ads: {len(ads_df)}')





# Get all texts

texts_dict = {'Id': [], 'CampaignId' : []}


for x, y in ads_df.iterrows():
    
    texts_dict['Id'].append(y[0])
    texts_dict['CampaignId'].append(y[2])    
    
    for key in y[1]:
        
        if key not in texts_dict:
            texts_dict[key] = []
            texts_dict[key].append(y[1][key])           
           
        else:
            texts_dict[key].append(y[1][key])

        
txtdata = pd.DataFrame(texts_dict)
df1 = txtdata.fillna('')


#TEXTS

df_txt = df1.filter(items = ['Text','CampaignId','Id'])


df_txt_dates = df_txt[df_txt['Text'].str.contains(FIND_DATES, regex= True, na=False)]
len(df_txt)
df_txt_dates_col = df_txt_dates['Text']
one_df_txt = df_txt_dates_col.str.extract(CUT_DATES)
one_df_txt
df_txt_dates_final = pd.concat([one_df_txt, df_txt_dates],axis=1)


df_txt_dates_final.columns=['Date','Text','CampaignId','Id']
df_txt_dates_final.tail(50)
df_txt_dates_final['Date'] = df_txt_dates_final['Date'].replace(np.nan, 'I am NaN')
#df_txt_dates_final[df_txt_dates_final['Date'].isnull()]

result = []
if len(df_txt_dates_final) > 0:
    
    for item in df_txt_dates_final['Date']:    
        x = find_matches2(d2_days, d1_month, item)        
        if str(x) < tomorrow2 or "NaN" in str(x) or str(x) > nextmonth2:
                y =  item  + ' => Replace Me!'
                result.append(y)
        else: 
                result.append('OK')
    df_txt_dates_final['Date']  =  result 


    df_txt_dates_final = df_txt_dates_final[~df_txt_dates_final[('Date')].str.contains('OK')]
    if len(df_txt_dates_final) == 0:
        df_txt_dates_final = pd.DataFrame({'Date':['Dates are ОК']}) 
else:
    df_txt_dates_final = pd.DataFrame({'Date':['No dates here']})
    

df_txt_dates_final2 = df_txt_dates_final[df_txt_dates_final[('Date')].str.contains('REPLACE')]
#df_txt_dates_final

print('Checked the texts')

#TITLES

df_title = df1.filter(items = ['Title','CampaignId','Id'])


df_title_dates = df_title[df_title['Title'].str.contains(FIND_DATES, regex= True, na=False)]
len(df_title)
df_title_dates_col = df_title_dates['Title']
one_df_title = df_title_dates_col.str.extract(CUT_DATES)
one_df_title
df_title_dates_final = pd.concat([one_df_title, df_title_dates],axis=1)


df_title_dates_final.columns=['Date','Title','CampaignId','Id']
df_title_dates_final.tail(50)
df_title_dates_final['Date'] = df_title_dates_final['Date'].replace(np.nan, 'I am NaN')
#df_title_dates_final[df_title_dates_final['Date'].isnull()]

result = []
if len(df_title_dates_final) > 0:
    
    for item in df_title_dates_final['Date']:    
        x = find_matches2(d2_days, d1_month, item)        
        if str(x) < tomorrow2 or "NaN" in str(x) or str(x) > nextmonth2:
                y =  item  + ' => Замени меня скорей!'
                result.append(y)
        else: 
                result.append('OK')
    df_title_dates_final['Date']  =  result 


    df_title_dates_final = df_title_dates_final[~df_title_dates_final[('Date')].str.contains('OK')]
    if len(df_title_dates_final) == 0:
        df_title_dates_final = pd.DataFrame({'Date':['Dates are OK']}) 
else:
    df_title_dates_final = pd.DataFrame({'Date':['No dates here']})
    

df_title_dates_final2 = df_title_dates_final[df_title_dates_final[('Date')].str.contains('REPLACE')]

#df_title_dates_final

print('Checked the titles')

#Subtitles

df_title2 = df1.filter(items = ['Title2','CampaignId','Id'])

[.....]

print(' ')

df_Grande_Finale = pd.DataFrame(
    {'Field': ['1.Titles', #1
              '2.Subtitles', #2
              '3.Texts', #3
              '4.Extensions', #4
              '5.Links Titles', #5
              '6.Extensions Links',
              '===============',#6

              'Parsing time: ',
              'Login:'
             ], 
     'The Old Dates': [len(df_title_dates_final2), #1
                     len(df_title2_dates_final2), #2
                     len(df_txt_dates_final2), #3
                     len(df_exten_dates_final2), #4  
                     len(df_sl_titles_dates_final2), #5
                     len(df_sl_description_dates_final2),#6
                     '================', 
                     df_mytime,
                     LOGIN
                    ]})

df_Grande_Finale

## Then load results into Excel file or into Google Sheets (https://github.com/d-k-git/scripts-for-diff-APIs/blob/main/loading-dataframes-into-Google-Sheets.py)

print('DONE!')



