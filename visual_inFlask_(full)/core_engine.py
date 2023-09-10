import json
import sqlalchemy as sa
import requests
import time 
import pymysql
import os.path
import sqlalchemy
import mysql.connector
import pandas as pd
from flask import Flask, render_template ,jsonify ,Response
from sqlalchemy import create_engine, text
from datetime import datetime,date,timedelta
from flask_mysqldb import MySQL
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdatesimport ,random  #
from MySQLdb import MySQLError  #
from pandas.tseries.offsets import MonthEnd,Week
import sqlite3

from database import register_access

startdate = '2008-04-01'
endDate = datetime.today().strftime('%Y-%m-%d')
token = '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' #new token
username = 'rn468'
api_base="https://api.github.com/search/repositories?q="


# creating a connection engine to a MySQL database using the `pymysql` library. It
# specifies the database URL, username, password, and database name. The `create_engine` function is
# used to create the engine object that will be used to interact with the database.
engine = create_engine("mysql+pymysql://ridha:@localhost/search_data_storage?charset=utf8mb4")


def check_keyword(ckeyword):
    conn = engine.raw_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    ckeyword = ckeyword.upper()
    check_query ="SELECT keyword_id FROM searched_keyword WHERE keyword_title='%s'"%(ckeyword)
    cursor.execute(check_query)
    result = cursor.fetchone() is None
    if result:   
        loop = True
        while loop == True:
            rand_id = random.randint(10000000, 99999999)#generate random number (8 digits)
            try:
                cursor.execute("SELECT * FROM searched_keyword WHERE keyword_id =%s"%str(rand_id))
                r_id = cursor.fetchone()[0]
                print (r_id)
            except:
                insert_keyword_query = "INSERT INTO searched_keyword(keyword_id,keyword_title,last_updated_date,last_data_fetched_at) VALUES(%s,%s,%s,%s)"
                value = (rand_id,ckeyword,endDate,startdate)
                cursor.execute(insert_keyword_query,value)
                conn.commit()
                loop = False#break the loop
    last_date_query = "SELECT last_data_fetched_at FROM searched_keyword WHERE keyword_title ='%s'"%str(ckeyword)
    cursor.execute(last_date_query)
    last_date = cursor.fetchone()
    keyword_query = "SELECT keyword_id FROM searched_keyword WHERE keyword_title ='%s'"%str(ckeyword)
    cursor.execute(keyword_query)
    keyword_id = cursor.fetchone()
    #print ('complete')
    ldate = last_date['last_data_fetched_at']
    keyword_id = keyword_id['keyword_id']
    print (ckeyword,ldate,keyword_id,result)
    return ckeyword,last_date,keyword_id,result


def stage1(keyword,keyword_id): 
    try:
        print("stage1")
        #keyword_id = keyword_id['keyword_id']
        print(keyword)
        last_date = '2008-04-01'
        loop_start_date = startdate
        #print(type(loop_start_date))
        conn = engine.raw_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        #run the api one tine and fetch total count and store it in db 
        print(api_base+keyword+' created:2008-04-01'+'..'+datetime.today().strftime('%Y-%m-%d'))
        response = requests.get(api_base+keyword)
        print(response.json())
        time.sleep(6)
        total_count  = response.json()['total_count']
        print("Stage 1 : ",total_count)
        update_query = "UPDATE searched_keyword SET total_count =%s"%(total_count)+" WHERE keyword_id =%s"%str(keyword_id)
        print("Stage 1 : ",update_query)
        cursor.execute(update_query)
        conn.commit()
        #print(response.json())
        if (total_count <= 30):
            print("Lesst than 30 ")
            counter = 0
            for item in response.json()['items']:
                null = None
                id = item['id']                 #repository id 
                node_id = item['node_id']       #repository node id
                name = item['name']             #repostory name 
                full_name = item['full_name']   #owner name and repository name
                description = item['description']
                url = item['url']               #repository url                  # url is repo_url
                commits_url = item['commits_url'] # all commits ur
                downloads_url = item['downloads_url'] #all downloads url
                issues_url = item['issues_url'] #all issues URL
                pulls_url = item['pulls_url']   #All the pulls url
                created_at = item['created_at'] #stores the created date
                language = item['language']     #Primary language used in repository
                if (language == null):
                    language = "Not Available"       
                forks = item['forks']           #Numbers of forks
                repo_size = item['size']
                watchers = item['watchers']
                try:
                    print("try 1")
                    query11 = "INSERT INTO keyword_search_data(keyword_id,id,node_id,name,full_name,description,repo_url,commits_url,downloads_url,pulls_url,created_at,repo_size,language,watchers,forks_count) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    value11 = (keyword_id,id,node_id,name,full_name,description,url,commits_url,downloads_url,pulls_url,created_at,repo_size,language,watchers,forks)
                    print(value11)
                    cursor.execute(query11,value11)
                    #cursor.execute(query1,value1)
                    print("Try commit")
                    conn.commit()
                    counter +=1
                except (sqlalchemy.exc.IntegrityError, pymysql.err.IntegrityError) as errr:
                    print("Continue.... st1",errr)
                    continue
                if(total_count == counter):
                    print()
                    cursor.execute("UPDATE searched_keyword SET completion_status=1, last_data_fetched_at='%s'"%(endDate)+" WHERE keyword_id = %s"%str(keyword_id))
                    conn.commit()
            return datetime.today().strftime('%Y-%m-%d')
        elif (total_count == 0):
            print("There is no Data s1")
            cursor.execute("UPDATE searched_keyword SET completion_status=1, last_data_fetched_at='%s'"%(endDate)+" WHERE keyword_id = %s"%str(keyword_id))
            conn.commit()
            return datetime.today().strftime('%Y-%m-%d')
        else:
            for beg in pd.date_range(loop_start_date,endDate,freq='W'):
                request_query = api_base+keyword+' created:'+beg.strftime("%Y-%m-%d")+'..'+(beg+Week()).strftime("%Y-%m-%d")
                print("Stage 1 : ",request_query)
                try:
                    response = requests.get(request_query) #(beg+MonthEnd(1)).strftime("%Y-%m-%d"))
                except KeyError:
                    time.sleep(30)
                    continue
                time.sleep(6)
                last_date = (beg+Week()).strftime("%Y-%m-%d")
                print("stage 1 : ",last_date)
                total_count = response.json()['total_count']
                print("Stage 1 : ",total_count)
                if (response.json()['total_count'] != 0):
                    for item in response.json()['items']:
                        id = item['id']                 #repository id 
                        node_id = item['node_id']       #repository node id
                        name = item['name']             #repostory name 
                        full_name = item['full_name']   #owner name and repository name
                        description = item['description']
                        url = item['url']               #repository url                  # url is repo_url
                        commits_url = item['commits_url'] # all commits url
                        downloads_url = item['downloads_url'] #all downloads url
                        issues_url = item['issues_url'] #all issues URL
                        pulls_url = item['pulls_url']   #All the pulls url
                        created_at = item['created_at'] #stores the created date
                        language = item['language']     #Primary language used in repository
                        null = None
                        if (language == null):
                            language = "Not Available"       
                        forks = item['forks']           #Numbers of forks
                        repo_size = item['size']
                        watchers = item['watchers']
                        try:
                            query = "INSERT INTO keyword_search_data(keyword_id,id,node_id,name,full_name,description,repo_url,commits_url,downloads_url,pulls_url,created_at,repo_size,language,watchers,forks_count) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                            value = (keyword_id,id,node_id,name,full_name,description,url,commits_url,downloads_url,pulls_url,created_at,repo_size,language,watchers,forks)
                            cursor.execute(query,value)
                            conn.commit()
                        except (sqlalchemy.exc.IntegrityError, pymysql.err.IntegrityError):
                            print("Continue....")
                            continue
                        last_date = (beg+Week()).strftime("%Y-%m-%d")
                        if(beg.strftime("%Y-%m-%d") == endDate):
                            print ('Data inserted into database unitil '+endDate)
                            print ('Data collection process is Completed')
                            #status_update_query = "UPDATE searched_keyword SET completion_status=0 WHERE keyword_id = ?"#+keyword_id
                            cursor.execute("UPDATE searched_keyword SET completion_status=1, last_data_fetched_at='%s'"%(endDate)+" WHERE keyword_id = %s"%str(keyword_id))
                            conn.commit()
                        else:
                            date_update_query = "UPDATE searched_keyword SET completion_status=0, last_data_fetched_at= '%s'"%(last_date)+" WHERE keyword_id = %s"%str(keyword_id)
                            cursor.execute(date_update_query)
                            conn.commit()
                    print("Stage 1 : If inner ")  
        return last_date
    except (KeyboardInterrupt,requests.exceptions.ConnectTimeout,pymysql.err.IntegrityError) as err:
        print ("The collection process is been interupted and data is collected till : " +last_date)
        print ("plesae continue to complete the collection process")
        date_update_query = "UPDATE searched_keyword SET completion_status=0,last_data_fetched_at='%s'"%(last_date)+" WHERE keyword_id = %s"%str(keyword_id)
        cursor.execute(date_update_query)
        conn.commit()
        return last_date
    #except requests.exceptions.ConnectionError: #delete all initial data in this error
        
#Returns last date and updates in table if the collection process is complete or not 1 = Completed ,0 = incolplete

def stage2(keyword,keyword_id,starDate):    
    last_date = starDate
    last_date= str(last_date["last_data_fetched_at"])
    print(last_date)
    print(keyword_id)
    conn = engine.raw_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        print("stage2")
        print(keyword)
        loop_start_date = last_date
        check_query = api_base+keyword+' created:'+last_date+'..'+datetime.today().strftime('%Y-%m-%d')
        print("stage 2 : ",check_query)
        response = requests.get(check_query)
        total_count = response.json()['total_count']
        print("Stage 2 : ",total_count)
        if (total_count == 0):
            print("There is no Data")
            cursor.execute("UPDATE searched_keyword SET completion_status=1, last_data_fetched_at='%s'"%(endDate)+" WHERE keyword_id = %s"%str(keyword_id))
            conn.commit()
            return datetime.today().strftime('%Y-%m-%d')
        else:
            for beg in pd.date_range(loop_start_date,endDate,freq='W'):
                try:
                    response = requests.get(api_base+keyword+' created:'+beg.strftime("%Y-%m-%d")+'..'+(beg+Week()).strftime("%Y-%m-%d"))
                    time.sleep(6)
                    last_date = (beg+Week()).strftime("%Y-%m-%d")
                    print("stage 2 date  : ",last_date)
                    print ("Stage 2 inner for : ",response.json()['total_count'])
                except KeyError:
                    time.sleep(30)
                    print("time sleep")
                    continue
                if (response.json()['total_count'] != 0):
                    for item in response.json()['items']:
                        id = item['id']                 #repository id 
                        node_id = item['node_id']       #repository node id
                        name = item['name']             #repostory name 
                        full_name = item['full_name']   #owner name and repository name 
                        description = item['description']
                        url = item['url']               #repository url                      #repo_url
                        commits_url = item['commits_url'] # all commits url
                        downloads_url = item['downloads_url'] #all downloads url
                        issues_url = item['issues_url'] #all issues URL
                        pulls_url = item['pulls_url']   #All the pulls url
                        created_at = item['created_at'] #stores the created date
                        language = item['language']     #Primary language used in repository
                        null = None
                        if (language == null):
                            language = "Not Available"
                        forks = item['forks']           #Numbers of forks
                        repo_size = item['size']
                        watchers = item['watchers']
                        try:
                            query = "INSERT INTO keyword_search_data(keyword_id,id,node_id,name,full_name,description,repo_url,commits_url,downloads_url,pulls_url,created_at,repo_size,language,watchers,forks_count) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                            value = (keyword_id,id,node_id,name,full_name,description,url,commits_url,downloads_url,pulls_url,created_at,repo_size,language,watchers,forks)
                            cursor.execute(query,value)
                            conn.commit()
                        except (sqlalchemy.exc.IntegrityError, pymysql.err.IntegrityError):
                            print("Continue....")
                            continue
                        last_date = (beg+Week()).strftime("%Y-%m-%d")
                        if(beg.strftime("%Y-%m-%d") == endDate):
                            print ('Data inserted into database unitil '+endDate)
                            print ('Data collection process is Completed')
                            #status_update_query = "UPDATE searched_keyword SET completion_status=0 WHERE keyword_id = ?"#+keyword_id
                            cursor.execute("UPDATE searched_keyword SET completion_status=1, last_data_fetched_at='%s'"%(endDate)+" WHERE keyword_id = %s"%str(keyword_id))
                            conn.commit()
                        else:
                            print(type(last_date))
                            date_update_query = "UPDATE searched_keyword SET completion_status=0, last_data_fetched_at= '%s'"%(last_date)+" WHERE keyword_id = %s"%str(keyword_id)
                            cursor.execute(date_update_query)
                            conn.commit()
        return last_date
    except (KeyboardInterrupt ,requests.exceptions.ConnectionError,pymysql.err.ProgrammingError) as err:
        #print(err)
        print ("The collection process is been interupted and data is collected till : " +last_date)
        print ("plesae continue to complete the collection process")
        date_update_query = "UPDATE searched_keyword SET completion_status=0, last_data_fetched_at= '%s'"%(last_date)+" WHERE keyword_id = %s"%str(keyword_id)
        cursor.execute(date_update_query)
        conn.commit()
        return last_date
#Returns last date and updates in table if the collection process is complete or not 1 = Completed ,0 = incolplete



def check_completion_status(id):
    print("check_completion_status")
    conn = engine.raw_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
        #id = str(id)
    print(id)
    #id = id['keyword_id']
    print(id)
    query1 = "SELECT completion_status FROM searched_keyword WHERE keyword_id =%s"%str(id)
    cursor.execute(query1)
    print("check after")
    completion_status = cursor.fetchone()
    completion_status = completion_status['completion_status']

    print("Completion Status : ",completion_status)
    total_count = "SELECT COUNT(id) FROM keyword_search_data WHERE keyword_id =%s"%str(id)
        
    cursor.execute(total_count)
    total_count = cursor.fetchone()
    total_count = total_count['COUNT(id)']
    print("Total Count : ",total_count)
    #finally:
    return completion_status,total_count
    

#with engine.connect() as conn


def check_database_for_updation():
    conn = engine.raw_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    get_all_id_query = "SELECT keyword_id,keyword_title,last_updated_date FROM searched_keyword"
    cursor.execute(get_all_id_query)
    keyword_id = cursor.fetchall()
    for i in keyword_id:
        id = i[0]
        keyword = i[1]
        date = i[2]
        d2 = datetime.strptime(endDate, "%Y-%m-%d").date()
        print(keyword + " - " +str(id)+ " - " +str(date))
        if(date != d2 and ((d2 - date).days) >= 7):
            print("Last Update "+str((d2 - date).days)+" days ago.")

#check_completion_status(46092586)
def main():
    #check_database_for_updation()
    keyword = input("Please insert the keyword : ")
    keyword,lastdate,keywordID,result = check_keyword(keyword) #result will tell if it is a new keyword or existing one 
    completion_status,total_count = check_completion_status(keywordID)
    register_access(keywordID,keyword)
    
    print (str(result) + ' Checking...')
    
    if (result == False):             #FALSE = keyword PRESENT & TRUE = keyword is ABSENT
        print("checking...m2")
        if (completion_status == 1):                     # 1 = completed ,0 = incomplete 
            print("checking...m3")
            response = requests.get(api_base+keyword+' created:'+startdate+'..'+endDate)
            print (total_count)
            if(total_count == response.json()['total_count']): # to check if there is any update since last run/iteration 
                print('The database is up to date')
        else:
            print("checking...m4")
            lastdate = stage2(keyword,keywordID,lastdate)
    else:
        print("checking...m5")
        lastdate = stage1(keyword,keywordID)

main()