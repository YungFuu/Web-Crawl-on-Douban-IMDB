# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 21:23:00 2021

@author: hp
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 16:03:37 2021

@author: Fu Yangyang
@uid: 3035882158
@introduction:
    These codes can find multiple movies at once and generate a separate csv file with the movie information.If input is "top250", then it will only return one csv file with top250 movies info
    single movie e.g.：
        input： Spider-Man: No Way Home
    multiple movies e.g.:
        input： Eternals,The Harder They Fall,No Time to Die,Spider-Man: No Way Home,Last Night in Soho,Pulp Fiction,Forrest Gump
    Douban top250 e.g.:
        input: top250
    Since IMDB web page will change with browser resolution, so the program will automatically set the browser size after running, please do not change the browser resolution in the middle.
    由于IMDB网页会随着浏览器分辨率变化而变化，因此程序运行后将自动设定浏览器大小，
    不能够中途更改浏览器分辨率，否则会导致数据检索失败。
"""

import os,time,random
from selenium import webdriver
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm

s=Service(r'C:\Users\hp\Desktop\HKU\msedgedriver.exe')
path=r'C:\Users\hp\Desktop\HKU\IMDb'

#global variables
count=0 #save error times
error_film=[] #save error movies
top250_df=pd.DataFrame() #save top250 movies info
lambda_bull = False # misson type
 
USER_AGENTS = [
 "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
 "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
 "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
 "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
 "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
 "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
 "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
 "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
 "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
 "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

#Input
print('-------------------------------------------------------------')
print('')
movies = input('Please enter the movie title， multiple movies please separate by comma， enter "top250" to search IMDb top250 movies info):')

#if input is a movie or movies--->convert into a list,lambda_bull=True
#if input is 'top250'---> search the top250 movie name and save in a list 
if ',' in movies:
    movies=movies.split(',')
elif '，' in movies:        
    movies=movies.split('，')        
elif movies=='top250':
    lambda_bull=True
    list25=[]
    top250=[]
    browser = webdriver.Edge(service=s)
    browser.set_window_size(1024,768)
    browser.get('https://www.imdb.com/chart/top?ref_=nv_mv_250_6')
    top250=browser.find_elements(by=By.XPATH,value='//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[position()>=1]/td[2]/a')
    movies=list(map(lambda x:x.text,top250))
    browser.close()
else:
    cache=movies
    movies=[]
    movies.append(cache)
print('Searching.....')

def movie_webcrawing(movie):
    #used to search a movie or a list of movie
    global count
    global error_film
    
    #random change the headers of webdriver
    random_agent = USER_AGENTS[random.randint(0, len(USER_AGENTS)-1)]    
    opt = webdriver.EdgeOptions()
    opt.add_argument('--user-agent=%s' % random_agent)
    #it's necessary to set browser window size, because the html is dynamics
    browser = webdriver.Edge(service=s,options=opt)
    browser.set_window_size(1024,768)
    browser.get('https://www.imdb.com/video/vi3482434329?ref_=nv_sr_srsg_1')
    #Find the search bar, input the movie name, click the search icon
    searchplace=browser.find_element(by=By.XPATH,value='//*[@id="suggestion-search"]')
    searchplace.send_keys(movie)
    browser.find_element(by=By.XPATH,value='//*[@id="suggestion-search-button"]').click()
    time.sleep(random.randint(15,20)/10)
    browser.find_element(by=By.XPATH,value='//*[@id="main"]/div/div[2]/table/tbody/tr[1]/td[2]/a').click()
    time.sleep(random.randint(15,20)/10)
    
    try:
        #find the info we need
        movie_name = browser.find_element(by=By.XPATH,value='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/h1').text
            
        #No ratings for unreleased movies
        try:
            nscore = browser.find_element(by=By.XPATH,value='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[2]/div/div[1]/a/div/div/div[2]/div[3]').text
        except:
            nscore = np.nan
        try:
            score = browser.find_element(by=By.XPATH,value='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]').text
        except:
            score = np.nan
            
        browser.find_element(by=By.XPATH,value='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div/div[2]/ul/li[1]/a').click()
        time.sleep(random.randint(5,10)/10)
        director=browser.find_elements(by=By.XPATH,value='//*[@id="fullcredits_content"]/table[1]/tbody/tr[position()>=1]/td[1]/a')
        director=str(list(map(lambda x:x.text,director)))
        
        actor=browser.find_elements(by=By.XPATH,value='//*[@id="fullcredits_content"]/table[3]/tbody/tr[position()>=2]/td[2]/a')
        actor=str(list(map(lambda x:x.text,actor)))
        
        browser.find_element(by=By.XPATH,value='//*[@id="sidebar"]/div[3]/ul/li[2]/a').click()
        time.sleep(random.randint(5,10)/10)
        release_date=browser.find_element(by=By.XPATH,value='//*[@id="releaseinfo_content"]/table[1]/tbody/tr[1]/td[2]').text
        
        browser.find_element(by=By.XPATH,value='//*[@id="sidebar"]/div[3]/div[2]').click()
        browser.find_element(by=By.XPATH,value='//*[@id="full_subnav"]/ul[1]/li[2]/a').click()

        try:
            intro=browser.find_element(by=By.XPATH,value='//*[@id="plot-summaries-content"]').text
        except:
            intro=np.nan
            
        #save all info into df
        df=pd.Series({
            'movie_name':movie_name,
            'release_date':release_date,
            'directors':director,
            'main_actors':actor,
            'average rating score':score,
            'total amount of people who rated the movie':nscore,
            'brief introduction':intro})
        
        #save as xxx.csv
        movie_name=movie_name.replace(':','_')
        df.to_csv(path+os.sep+'{}.csv'.format(movie_name),encoding='utf-8-sig')
        
    except:
        print('Meet a problem when searching {},The program will skip the movie and continue the search'.format(str(movie)))
        count+=1
        error_film.append(movie)
    browser.close()
    

def top250_webcrawing(movie):
    global top250_df
    global count
    global error_film

    random_agent = USER_AGENTS[random.randint(0, len(USER_AGENTS)-1)]
    opt = webdriver.EdgeOptions()
    opt.add_argument('--user-agent=%s' % random_agent)
    
    browser = webdriver.Edge(service=s,options=opt)
    browser.set_window_size(1024,768)
    browser.get('https://www.imdb.com/video/vi3482434329?ref_=nv_sr_srsg_1')
    #Find the search bar, input the movie name, click the search icon
    searchplace=browser.find_element(by=By.XPATH,value='//*[@id="suggestion-search"]')
    searchplace.send_keys(movie)
    browser.find_element(by=By.XPATH,value='//*[@id="suggestion-search-button"]').click()
    time.sleep(random.randint(5,10)/10)
    browser.find_element(by=By.XPATH,value='//*[@id="main"]/div/div[2]/table/tbody/tr[1]/td[2]/a').click()
    time.sleep(random.randint(10,15)/10)
    
    try:
        #find the info we need
        movie_name = browser.find_element(by=By.XPATH,value='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/h1').text
            
        #No ratings for unreleased movies
        try:
            nscore = browser.find_element(by=By.XPATH,value='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[2]/div/div[1]/a/div/div/div[2]/div[3]').text
        except:
            nscore = np.nan
        try:
            score = browser.find_element(by=By.XPATH,value='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]').text
        except:
            score = np.nan
            
        browser.find_element(by=By.XPATH,value='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div/div[2]/ul/li[1]/a').click()
        time.sleep(random.randint(5,10)/10)
        director=browser.find_elements(by=By.XPATH,value='//*[@id="fullcredits_content"]/table[1]/tbody/tr[position()>=1]/td[1]/a')
        director=str(list(map(lambda x:x.text,director)))
        
        actor=browser.find_elements(by=By.XPATH,value='//*[@id="fullcredits_content"]/table[3]/tbody/tr[position()>=2]/td[2]/a')
        actor=str(list(map(lambda x:x.text,actor)))
        
        browser.find_element(by=By.XPATH,value='//*[@id="sidebar"]/div[3]/ul/li[2]/a').click()
        release_date=browser.find_element(by=By.XPATH,value='//*[@id="releaseinfo_content"]/table[1]/tbody/tr[1]/td[2]').text
        
        browser.find_element(by=By.XPATH,value='//*[@id="sidebar"]/div[3]/div[2]').click()
        time.sleep(random.randint(5,10)/10)
        browser.find_element(by=By.XPATH,value='//*[@id="full_subnav"]/ul[1]/li[2]/a').click()
        time.sleep(random.randint(5,10)/10)
        try:
            intro=browser.find_element(by=By.XPATH,value='//*[@id="plot-summaries-content"]').text
        except:
            intro=np.nan
            
         #save all info indf
        df=pd.Series({
            'movie_name':movie_name,
            'release_date':release_date,
            'directors':director,
            'main_actors':actor,
            'average rating score':score,
            'total amount of people who rated the movie':nscore,
            'brief introduction':intro})
        
        #save df in top250_df
        df=df.to_frame()
        top250_df=top250_df.append(df.T)
        
    except:
        print('Meet a problem when searching {},The program will skip the movie and continue the search'.format(str(movie)))
        count+=1
        error_film.append(movie)
        empty_row={'movie_name':[movie]}
        top250_df=top250_df.append(pd.DataFrame(empty_row))
    browser.close()

#run the function and report result according to different misson
if lambda_bull == False:
    start_time = time.time()
    for movie in tqdm(movies):
        movie_webcrawing(movie)
    print('')
    print('Searching completed')
    print('Total Search:{} film(s)'.format(len(movies)))
    sf=len(movies)-count
    print('Successful Search：{} film(s)'.format(sf))
    print('-------------------------------------------------------------')
    if count > 0 :
        print('The following movies were not searched successfully:')
        print(error_film)
    print('Results have been saved to {}'.format(path))
    print("--- %s seconds ---" % (time.time() - start_time))
    
elif lambda_bull == True:
    start_time = time.time()
    for movie in tqdm(movies):
        top250_webcrawing(movie)
    top250_df.to_csv(path+os.sep+'IMDb_top250_movies.csv',encoding='utf-8-sig')
    
    #report the search result
    print('')
    print('Searching completed')
    print('Total Search:{} film(s)'.format(len(movies)))
    sf=len(movies)-count
    print('Successful Search：{} film(s)'.format(sf))
    print('-------------------------------------------------------------')
    if count > 0 :
        print('The following movies were not searched successfully:')
        print(error_film)
    print('Results have been saved to {}'.format(path))
    print("--- %s seconds ---" % (time.time() - start_time))