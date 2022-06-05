# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 16:03:37 2021

@author: Fu Yangyang
@uid: 3035882158
@introduction:
    These codes can find multiple movies at once and generate a separate csv file with the movie information.If input is "top250", then it will only return one csv file with top250 movies info
    single movie example：
        input： 肖申克的救赎
    multiple movies example:
        input： 肖申克的救赎，复仇者联盟4，冰雪奇缘2，海上钢琴师
    Douban top250 example:
        input: top250    
"""

import os,time,random
import numpy as np
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm

s=Service(r'C:\Users\hp\Desktop\HKU\msedgedriver.exe')
path=r'C:\Users\hp\Desktop\HKU\Douban'

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
movies = input('Please enter the movie title, multiple movies please separate by comma,Enter "top250" to retrieve information of top250 movies on Douban:')

#if input is a movie or movies--->convert into a list
#if input is 'top250'---> search the top250 movie name and save in a list 
if ',' in movies:
    movies=movies.split(',')
elif '，' in movies:        
    movies=movies.split('，')        
elif (movies=='top250') or (movies=='top 250'):
    lambda_bull=True
    list25=[]
    top250=[]
    browser = webdriver.Edge(service=s)
    browser.get('https://movie.douban.com/top250?start=0&filter=')
    for i in range(0,10):
        time.sleep(random.randint(10,15)/10)
        list25=browser.find_elements(by=By.XPATH,value='//*[@id="content"]/div/div[1]/ol/li[position()>=1]/div/div[2]/div[1]/a/span[1]')
        for x in list25:
            top250.append(x.text)
        browser.find_element(by=By.XPATH,value='//*[@id="content"]/div/div[1]/div[2]/span[3]/a').click()
    movies=top250
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

    browser = webdriver.Edge(service=s,options=opt)
    browser.get('https://movie.douban.com/subject/1292052/')
    time.sleep(random.randint(10,15)/10)
    #Find the search bar, input the movie name, click the search icon
    searchplace=browser.find_element(by=By.XPATH,value='//*[@id="inp-query"]')
    searchplace.send_keys(movie)
    browser.find_element(by=By.XPATH,value='//*[@id="db-nav-movie"]/div[1]/div/div[2]/form/fieldset/div[2]/input').click()
    time.sleep(random.randint(10,15)/10)
    browser.find_element(by=By.XPATH,value='//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div/div/div[1]/a').click()
    time.sleep(random.randint(10,15)/10)
        
    try:
        #find the info we need
        movie_name = browser.find_element(by=By.XPATH,value='//*[@id="content"]/h1/span[1]').text
        release_date = browser.find_element(by=By.XPATH,value='//*[@id="info"]/span[11]').text
        score = browser.find_element(by=By.XPATH,value='//*[@id="interest_sectl"]/div[1]/div[2]/strong').text
        intro = browser.find_element(by=By.XPATH,value='//*[@id="link-report"]/span[1]').text
        
        #No ratings for unreleased movies
        try:
            nscore = browser.find_element(by=By.XPATH,value='//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span').text
        except:
            nscore = np.nan
        
        #Places of info may change, so search these info in other ways
        actor_bull = False
        allinfo = browser.find_elements(by=By.TAG_NAME, value= 'span')
        for row in range(0,len(allinfo)):
            if allinfo[row].text=='导演':
                director=allinfo[row+1].text
            elif allinfo[row].text =='主演':
                actor=allinfo[row+1].text
                actor_bull=True
            elif '上映日期' in allinfo[row].text:
                order=i+1
            elif '片长' in allinfo[row].text:
                break
        
        release_date=allinfo[order].text
        #No actors in documentary
        if actor_bull == False:
            actor = np.nan
        else:
            pass
        
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

    browser = webdriver.Edge(service=s)
    browser.get('https://movie.douban.com/subject/1292052/')
    time.sleep(random.randint(10,15)/10)
    #Find the search bar, input the movie name, click the search icon
    searchplace=browser.find_element(by=By.XPATH,value='//*[@id="inp-query"]')
    searchplace.send_keys(movie)
    browser.find_element(by=By.XPATH,value='//*[@id="db-nav-movie"]/div[1]/div/div[2]/form/fieldset/div[2]/input').click()
    time.sleep(random.randint(10,15)/10)
    browser.find_element(by=By.XPATH,value='//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div/div/div[1]/a').click()
    time.sleep(random.randint(10,15)/10)
        
    try:
        #find the info we need
        movie_name = browser.find_element(by=By.XPATH,value='//*[@id="content"]/h1/span[1]').text
        score = browser.find_element(by=By.XPATH,value='//*[@id="interest_sectl"]/div[1]/div[2]/strong').text
        intro = browser.find_element(by=By.XPATH,value='//*[@id="link-report"]/span[1]').text

        #No ratings for unreleased movies
        try:
            nscore = browser.find_element(by=By.XPATH,value='//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span').text
        except:
            nscore = np.nan
        
        #Places of info may change
        actor_bull = False
        allinfo = browser.find_elements(by=By.TAG_NAME, value= 'span')
        for row in range(0,len(allinfo)):
            if allinfo[row].text=='导演':
                director=allinfo[row+1].text
            elif allinfo[row].text =='主演':
                actor=allinfo[row+1].text
                actor_bull = True
            elif '上映日期' in allinfo[row].text:
                order=row+1
            elif '片长' in allinfo[row].text:
                break
        release_date=allinfo[order].text
        #No actors in documentary
        if actor_bull == False:
            actor = np.nan
        else:
            pass

            
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
        top250_df=top250_df.append(df.T,ignore_index=True)
        
    except:
        print('Meet a problem when searching {},The program will skip the movie and continue the search'.format(str(movie)))
        count+=1
        error_film.append(movie)
        empty_row={'movie_name':[movie]}
        top250_df=top250_df.append(pd.DataFrame(empty_row))
    browser.close()
    
def error_searching(movie):
    #Debug: first item is not a movie but an actor,second search
    global error_film
    global count
    global top250_df
    global lambda_bull
     
    random_agent = USER_AGENTS[random.randint(0, len(USER_AGENTS)-1)]    
    opt = webdriver.EdgeOptions()
    opt.add_argument('--user-agent=%s' % random_agent)

    browser = webdriver.Edge(service=s)
    browser.get('https://movie.douban.com/subject/1292052/')
    time.sleep(random.randint(10,15)/10)
    #Find the search bar, input the movie name, click the search icon
    searchplace=browser.find_element(by=By.XPATH,value='//*[@id="inp-query"]')
    searchplace.send_keys(movie)
    browser.find_element(by=By.XPATH,value='//*[@id="db-nav-movie"]/div[1]/div/div[2]/form/fieldset/div[2]/input').click()
    time.sleep(random.randint(10,15)/10)
    #xpath here is different
    browser.find_element(by=By.XPATH,value='//*[@id="root"]/div/div[2]/div[1]/div[1]/div[3]/div/div/div[1]/a').click()
    time.sleep(random.randint(10,15)/10)
        
    try:
        #find the info we need
        movie_name = browser.find_element(by=By.XPATH,value='//*[@id="content"]/h1/span[1]').text
        score = browser.find_element(by=By.XPATH,value='//*[@id="interest_sectl"]/div[1]/div[2]/strong').text
        intro = browser.find_element(by=By.XPATH,value='//*[@id="link-report"]/span[1]').text

        #No ratings for unreleased movies
        try:
            nscore = browser.find_element(by=By.XPATH,value='//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span').text
        except:
            nscore = np.nan
        
        #Places of info may change
        actor_bull = False
        allinfo = browser.find_elements(by=By.TAG_NAME, value= 'span')
        for row in range(0,len(allinfo)):
            if allinfo[row].text=='导演':
                director=allinfo[row+1].text
            elif allinfo[row].text =='主演':
                actor=allinfo[row+1].text
                actor_bull = True
            elif '上映日期' in allinfo[row].text:
                order=row+1
            elif '片长' in allinfo[row].text:
                break
        release_date=allinfo[order].text
        #No actors in documentary
        if actor_bull == False:
            actor = np.nan
        else:
            pass
        
        #debug according to the different misson
        if lambda_bull ==False:
            #save all info indf
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
            count-=1
            error_film.remove(movie)
        
        elif lambda_bull==True:
            #Add complete content
            top250_df[top250_df['movie_name']==movie]=[movie,release_date,director,actor,score,nscore,intro]
            count-=1
            error_film.remove(movie)
            
    except:
        print('Still fail to search {}'.format(str(movie)))
    browser.close()

#run the function and report result according to different misson
if lambda_bull == False:    
    for movie in tqdm(movies):
        movie_webcrawing(movie)
    #report the search result
    print('')
    print('Searching completed')
    total_search=len(movies)
    print('Total Search:{} film(s)'.format(total_search))
    sf=len(movies)-count
    print('Successful Search：{} film(s)'.format(sf))
    print('-------------------------------------------------------------')
    if count > 0 :
        print('Fail to search the following movies:')
        print(error_film)
        print('Try to search again the movies above')
        error_movies=error_film[:]
        for movie in tqdm(error_movies):
            error_searching(movie)
        print('')
        print('Second search completed')
        if count > 0:
            print('Fail to search the following movies:')
            print(error_film)
        else:
            print('All movies have been successfully searched')                
    print('Results have been saved to {}'.format(path))
    
elif lambda_bull == True:
    for movie in tqdm(movies):
        top250_webcrawing(movie)    
    
    #report the search result
    print('')
    print('Searching completed')
    total_search=len(movies)
    print('Total Search:{} film(s)'.format(total_search))
    sf=len(movies)-count
    print('Successful Search：{} film(s)'.format(sf))
    print('-------------------------------------------------------------')
    if count > 0:
        print('Fail to search the following movies:')
        print(error_film)
        print('Try to search again the movies above')
        error_movies=error_film[:]
        for movie in tqdm(error_movies):
            error_searching(movie)
        print('')
        print('Second search completed')
        if count > 0:
            print('Fail to search the following movies:')
            print(error_film)
        else:
            print('All movies have been successfully searched')
    top250_df.to_csv(path+os.sep+'Douban_top250_movies.csv',encoding='utf-8-sig')
    print('Results have been saved to {}'.format(path))
    

