import os
from PIL import Image
#!pip install pytesseract
from pytesseract import image_to_string
import numpy as np
import re
import random
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

# writing a debug log file
log_path = os.path.join(os.getcwd(), "chromedriver.log")

#  chrome driver options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("disable-infobars")
# chrome_options.addArguments("--start-maximized")


browser = webdriver.Chrome( 
    chrome_options=chrome_options,
    service_args=['--verbose', f'--log-path={log_path}']
    )


### the start page number
p = 0

def read_queries_list_from_file(filename):

    f = open( filename, mode = 'r', encoding = 'utf-8' )    
    return [x.strip() for x in f]


import time
import datetime
now = datetime.datetime.now()
today = now.date()
from datetime import datetime
my_time = datetime.now().strftime('%H:%M:%S')
q = 1
pos_list = []
zag_list = []
txt_list = []
path_list = []
query_list = []
link_list = []
k_list = []




for query in read_queries_list_from_file('KEYS.txt'):
    #from datetime import datetime
    #my_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = re.sub('\s','%20',query)
    url = 'http://www.google.com/search?q=' + query 
    print (url)
    browser.get(url)
    time.sleep(1)
    height = browser.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )")
    #browser.close()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"--window-size=2300,{height}")
    chrome_options.add_argument("--hide-scrollbars")
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(url)
    my_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    #my_time = datetime.now().strftime('%H-%M-%S')
    #my_time = datetime.now()
#pause 3 second to let page loads
    #time.sleep(3)
#save screenshot
    browser.save_screenshot(r'Скриншоты_ADS/' + my_time + ' ' + re.sub('%20', ' ', query) + '_.png')
    #browser.close()
    #print(my_time)

    
   
    #if ads_all in ads_top:
    for _ in browser.find_elements_by_xpath("//div[(@id='tads')]//div[(@class='abuKkc')]"):
            k_list.append('Наверху')
            
    for _ in browser.find_elements_by_xpath("//div[(@id='bottomads')]//div[(@class='abuKkc')]"):
            k_list.append('Внизу')       
    
    #head
    for _ in browser.find_elements_by_xpath("//div[starts-with(@class, 'cfxYMc')]"):
        print(_.text)  
        zag_list.append(_.text)
        query_list.append(re.sub('%20',' ',query))
            
    #link
    for _ in browser.find_elements_by_xpath("//div[(@class='abuKkc')]//span[starts-with(@class, 'Zu0yb')]"):
        #print(_.text)  
        path_list.append(_.text)    
        link_list.append(url)   
    #text       
    for _ in browser.find_elements_by_xpath("//div[(@data-text-ad='1')]//div[contains(concat(normalize-space(@class), ' '), 'MUxGbd ') and  not(contains(concat(' ', normalize-space(@class), ' '),' aLF0Z ')) and  not(contains(concat(normalize-space(@class), ' '),'cfxYMc '))]"):
        #print(_.text)  
        txt_list.append(_.text)    
        
            


    print ('Query {} from {}'.format(q,len (read_queries_list_from_file('KEYS.txt'))))
    
    print('...')
    print('...')
    print('...')
    
    sleep(1)
    q += 1


# transpose dataframe twice to get around a possible error with the length of the array strings 

a = {   
        'Place: k_list,
        'Head': zag_list,
        'Text': txt_list,
        'Link': path_list,
        'Query': query_list,
        
        
 
}

b = pd.DataFrame.from_dict(a, orient='index')
b.transpose() 
b.replace(to_replace=[None], value=np.nan, inplace=True)
b.to_csv('AdTexts.csv', sep=',', encoding='utf-8')    

df = b.transpose() 
df


### Load into Excel
 
print(' ')
print('Load into Excel...')
print(' ')   
    
writer = pd.ExcelWriter('TEXT_ADS.xlsx', engine='xlsxwriter')


df.to_excel(writer, sheet_name='ADS',index=False)  

writer.save() 

print('')
print('DONE!')
