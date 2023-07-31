import random
from MySQLdb import MySQLError
import requests 
import mysql.connector
import pandas as pd
from pandas.tseries.offsets import MonthEnd
from datetime import datetime
import time
#import urllib.request
import json
import sqlite3


endDate = datetime.today().strftime('%Y-%m-%d')
token = 'insert token here'
username = 'rn468'

connected = False
try:
    con = mysql.connector.connect(
        user = 'root',
        password = '',
        host = 'localhost',
        database = 'search_data_storage'
    )
    connected = True
except MySQLError as er:
    print ('Error connecting to database '+er)


def optmiseSpeed(keyword,startdate):#keyword,startdate
    response = requests.get(api_base+keyword+':created:'+startdate+'..'+(beg+Week()).strftime("%Y-%m-%d"),auth=(username,token))
    time.sleep(6)
    response_count = response.json()['total_count']
    print(startdate+'-'+(beg+Week()).strftime("%Y-%m-%d"))
    if(response_count<=30):
        return response_count,response,'W'
    elif(response_count>30):
        return response_count,response,'D'
#returns response_count,json response and weekly or daily bit

def check_keyword(ckeyword):
    try:
        cursor = con.cursor()
        if connected:
            ckeyword = ckeyword.upper()
            check_query = "SELECT keyword_id FROM searched_keyword WHERE keyword_title = '"+ckeyword+"'"
            cursor.execute(check_query)
            result = cursor.fetchone() is None #result : FALSE = keyword PRESENT & TRUE = keyword is ABSENT
            if result:
                loop = True
                while loop == True:
                    rand_id = random.randint(10000000, 99999999)#generate random number (8 digits)
                    try:
                        cursor.execute('SELECT * FROM searched_keyword WHERE keyword_id = ?',(rand_id,))
                        r_id = cursor.fetchone()[0]
                        print (r_id)
                    except:
                        insert_keyword_query = "INSERT INTO searched_keyword(keyword_id,keyword_title,last_updated_date) VALUES(%s,%s,%s)"
                        value = (rand_id,ckeyword,endDate)
                        cursor.execute(insert_keyword_query,value)
                        con.commit()
                        loop = False#break the loop
    
        last_date_query = "SELECT last_updated_date FROM searched_keyword WHERE keyword_title = '"+ckeyword+"'"
        keyword_query = "SELECT keyword_id FROM searched_keyword WHERE keyword_title = '"+ckeyword+"'"
        cursor.execute(last_date_query)
        last_date = cursor.fetchone()[0]

        cursor.execute(keyword_query)
        keyword_id = cursor.fetchone()[0]

        print ('complete')
        return ckeyword,last_date,keyword_id,result
    finally:
        print ("Check Keyword")
#Returns keyword ,last date ,keyword ID and result= keyword EXISTED OR NOT



def stage1(keyword,keyword_id): 
    last_date = '2009-04-01'
    try:
        if connected:
            api_base="https://api.github.com/search/repositories?q="
            cursor = con.cursor()
            for beg in pd.date_range('2023-07-01',endDate,freq='MS'):
                response = requests.get(api_base+keyword+':created:'+beg.strftime("%Y-%m-%d")+'..'+(beg+MonthEnd(1)).strftime("%Y-%m-%d"),auth=(username,token))
                last_date = (beg + MonthEnd(1)).strftime("%Y-%m-%d")
                for item in response.json()['items']:
                    id = item['id']                 #repository id 
                    node_id = item['node_id']       #repository node id
                    name = item['name']             #repostory name 
                    full_name = item['full_name']   #owner name and repository name 
                    description = item['description']
                    url = item['url']               #repository url                  # url is repo_url
                    commits_url = item['commits_url'] # all commits url
                    print (url+'/commits')
                    commit_count_response = requests.get(url+'/commits')
                    commit_count_response = json.loads(commit_count_response.text)
                    commit_count_response = json.dumps(commit_count_response) 
                    commit_count = commit_count_response.count('"commit":') #counts number of commits
                    print ('Number of commits : ',commit_count)
                    downloads_url = item['downloads_url'] #all downloads url
                    issues_url = item['issues_url'] #all issues URL
                    pulls_url = item['pulls_url']   #All the pulls url

                    #languages_url = 
                    #comments_url = 

                    created_at = item['created_at'] #stores the created date
                    language = item['language']     #Primary language used in repository
                    null = None
                    if (language == null):
                        language = "Not Available"       
                    forks = item['forks']           #Numbers of forks
                    repo_size = item['size']
                    watchers = item['watchers']
                   # print (name) #remove later
                    query = "INSERT INTO keyword_search_data(keyword_id,id,node_id,name,full_name,description,repo_url,commits_url,downloads_url,pulls_url,created_at,repo_size,language,watchers,forks_count,commits_count) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    value = (keyword_id,id,node_id,name,full_name,description,url,commits_url,downloads_url,pulls_url,created_at,repo_size,language,watchers,forks,commit_count)
                    cursor.execute(query,value)
                    con.commit()
                    time.sleep(60)
                last_date = (beg + MonthEnd(1)).strftime("%Y-%m-%d")
        print ('Data inserted into database unitil '+endDate)
        print ('Data collection process is Completed')
        #status_update_query = "UPDATE searched_keyword SET completion_status=0 WHERE keyword_id = ?"#+keyword_id
        cursor.execute("UPDATE searched_keyword SET completion_status=1, last_data_fetched_at=%s WHERE keyword_id = %s",(endDate,keyword_id,))
        con.commit()
        return last_date
    except KeyboardInterrupt:
        print ("The collection process is been interupted and data is collected till : " +last_date)
        print ("plesae continue to complete the collection process")
        date_update_query = "UPDATE searched_keyword SET completion_status=0,last_data_fetched_at=%s WHERE keyword_id = %s"
        cursor.execute(date_update_query,(last_date,keyword_id,))
        con.commit()
        return last_date
#Returns last date and updates in table if the collection process is complete or not 1 = Completed ,0 = incolplete
    

def stage2(keyword,keyword_id,startDate):
    last_date = '2009-04-01'
    try:
        if connected:
            api_base="https://api.github.com/search/repositories?q="
            cursor = con.cursor()
            for beg in pd.date_range(startDate,endDate,freq='MS'):
                response = requests.get(api_base+keyword+':created:'+beg.strftime("%Y-%m-%d")+'..'+(beg+MonthEnd(1)).strftime("%Y-%m-%d"),auth=(username,token))
                last_date = (beg + MonthEnd(1)).strftime("%Y-%m-%d")
                for item in response.json()['items']:
                    id = item['id']                 #repository id 
                    node_id = item['node_id']       #repository node id
                    name = item['name']             #repostory name 
                    full_name = item['full_name']   #owner name and repository name 
                    description = item['description']
                    url = item['url']               #repository url                      #repo_url
                    commits_url = item['commits_url'] # all commits url
                    commit_count_response = requests.get(url+'/commits')
                    commit_count_response = json.loads(commit_count_response.text)
                    commit_count_response = json.dumps(commit_count_response) 
                    commit_count = commit_count_response.count('"commit":') #counts number of commits
                    downloads_url = item['downloads_url'] #all downloads url
                    issues_url = item['issues_url'] #all issues URL
                    pulls_url = item['pulls_url']   #All the pulls url

                    #languages_url = 
                    #comments_url = 

                    created_at = item['created_at'] #stores the created date
                    language = item['language']     #Primary language used in repository
                    null = None
                    if (language == null):
                        language = "Not Available"
                    forks = item['forks']           #Numbers of forks
                    repo_size = item['size']
                    watchers = item['watchers']
                    query = "INSERT INTO keyword_search_data(keyword_id,id,node_id,name,full_name,description,repo_url,commits_url,downloads_url,pulls_url,created_at,repo_size,language,watchers,forks_count,commits_count) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    value = (keyword_id,id,node_id,name,full_name,description,url,commits_url,downloads_url,pulls_url,created_at,repo_size,language,watchers,forks,commit_count)
                    cursor.execute(query,value)
                    con.commit()
                    time.sleep(60)
                last_date = (beg + MonthEnd(1)).strftime("%Y-%m-%d")
        print ('Data inserted into database unitil '+endDate)
        print ('Data collection process is Completed')
        status_update_query = "UPDATE searched_keyword SET completion_status=1 WHERE keyword_id = ?"#+keyword_id
        cursor.execute("UPDATE searched_keyword SET completion_status=1, last_data_fetched_at=%s WHERE keyword_id = %s",(endDate,keyword_id,))
        con.commit()
        return last_date
    except KeyboardInterrupt:
        print ("The collection process is been interupted and data is collected till : " +last_date)
        print ("plesae continue to complete the collection process")
        date_update_query = "UPDATE searched_keyword SET completion_status=0,last_data_fetched_at=%s WHERE keyword_id = %s"
        cursor.execute(date_update_query,(last_date,keyword_id,))
        con.commit()
        return last_date
#Returns last date and updates in table if the collection process is complete or not 1 = Completed ,0 = incolplete
    

def check_completion_status(id):
    try:
        cursor = con.cursor()
        if connected:
            id = str(id)
            query1 = "SELECT completion_status FROM searched_keyword WHERE keyword_id = "+id
            cursor.execute(query1)
            result = cursor.fetchone()[0]
            print(result)
    finally:
        return result
#Returns result and if last collection cycle was completed  1 = completed ,0 = inncomplete




def main():  
      
      keyword = input("Please insert the keyword : ")
      
      keyword,lastdate,keywordID,result = check_keyword(keyword) #result will tell if it is a new keyword or existing one 
    
      if (result == 0):
          completion_status = check_completion_status(keywordID)
          if (completion_status != 0):
              print ("call")
          else:
              lastdate = stage1(keyword,keywordID)
      
      #lastdate = stage1(keyword,keywordID)

      #
      print (lastdate)

for beg in pd.date_range('2023-06-01',endDate,freq='W'):
    inner_loop_startdate = (beg+timedelta(days=1)).strftime("%Y-%m-%d")
    frequency_counter,json_response,freq = optmiseSpeed(kw,inner_loop_startdate)
    print(str(frequency_counter) + " : " + str(json_response.json()['total_count']) + " : " +  str(freq))
    if(freq == 'D'):
        print ('Week '+ inner_loop_startdate + ' : ' + (beg+Week()).strftime("%Y-%m-%d"))
        for beg in pd.date_range(inner_loop_startdate,(beg+Week()).strftime("%Y-%m-%d"),freq='D'):
            response = requests.get(api_base+kw+':created:'+beg.strftime("%Y-%m-%d")+'..'+beg.strftime("%Y-%m-%d"),auth=(username,token))
            print ('Total Count : '+ str(response.json()['total_count']) + ' : ' + beg.strftime("%Y-%m-%d")+'-'+beg.strftime("%Y-%m-%d"))
            time.sleep(6)
    else:
            print('Week')
