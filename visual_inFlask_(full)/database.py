from flask import jsonify
from sqlalchemy import create_engine, text
import json
import sqlalchemy as sa
import requests
import time
from datetime import datetime,date
import pymysql
import pandas as pd

engine = create_engine("mysql+pymysql://ridha:@localhost/search_data_storage?charset=utf8mb4")

time_ellapsed = time.time()

def register_access(keyword_id,keyword):
    conn = engine.raw_connection()
    cursor = conn.cursor()
    query = "INSERT INTO register(datetime_stamp,keyword_id,keyword_title) VALUES(%s,%s,%s)"
    values = (str(datetime.now()),keyword_id,keyword)
    cursor.execute(query,values)
    conn.commit()
    return None

def get_languages_data_from_db():
    conn = engine.raw_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT language FROM keyword_search_data"
    cursor.execute(query)
    result = cursor.fetchall()
    lang =[]
    for row in result:
        l = row['language']
        lang.append(l)
    l = {x:lang.count(x) for x in lang}
    language, count = l.keys(),l.values()
    return language,count

def get_created_date(keyword_id):
    conn = engine.raw_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT created_at FROM keyword_search_data WHERE keyword_id =%s"%str(keyword_id)
    cursor.execute(query)
    result = cursor.fetchall()
    date = []
    for row in result:
        dates = row['created_at'].strftime("%Y-%m")
        date.append(str(dates))
    d = {x:date.count(x) for x in date}
    dates, count = d.keys(),d.values()
    return dates,count

def get_dashboard_data():
    conn = engine.raw_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query  = "SELECT * FROM searched_keyword ORDER BY keyword_title DESC"
    query2 = "SELECT s.keyword_title FROM keyword_search_data k LEFT JOIN searched_keyword s ON k.keyword_id = s.keyword_id ORDER BY s.keyword_title DESC"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.execute(query2)
    result2 = cursor.fetchall()
    #print(result2)
    label = []
    count = []
    for data in result:
        label.append(data['keyword_title'])
        count.append(data['total_count'])    
    k = []
    for data in result2:
        k.append(data['keyword_title'])

    d = {x:k.count(x) for x in k}
    kw, cou = d.keys(),d.values()
    #  print(" dipak ",d)
    #print (" kw ",cou,count)
    ac_value = []
    for dt in cou:
        ac_value.append(dt)
    
    print (ac_value,count,label)

    return label,count,ac_value

get_dashboard_data()


def load_keywords_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from searched_keyword"))
        keywords_data = [] 
        for roww in result.all():
            keywords_data.append((roww))
        
        return keywords_data
    
    '''    qry = sa.text("select * from keyword_search_data")
        resultset = conn.execute(qry)
        results_as_dict = resultset.mappings().all()
        print(results_as_dict)
        results_as_dict = results_as_dict.__dict__
        print("tyoe ::::")
        print(type(results_as_dict))'''


def load_keyword_all_details(keyword_id):
    with engine.connect() as conn:
        query = sa.text("select * from keyword_search_data where keyword_id ='%s'"%(keyword_id))
        result = conn.execute(query)
        #print(result)
        data = []
        for row in result.all():
            data.append(row)
        return data

def fetch_commits_data_from_github(keyword_id,id):
    conn = engine.raw_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    date_query ="SELECT repo_url FROM keyword_search_data WHERE id ='%s'"%(id)
    cursor.execute(date_query)
    url = cursor.fetchone()
    print(url)
    url = url['repo_url']
    print(url)
    page_count = 1
    total_commit = 0
    count = 0
    while True:
        print("while")
        commit_response = requests.get(url+'/commits?per_page=100&page='+str(page_count))
        commits_date = commit_response
        commit_response = json.loads(commit_response.text)
        commit_response = json.dumps(commit_response)
        commit_count=commit_response.count('"commit":')
        total_commit = total_commit + commit_count
        page_count += 1
        for item in commits_date.json():
            date = item['commit']['author']['date']
            values = (keyword_id,id,date)
            query_date = "INSERT INTO commit_table(keyword_id,id,date) VALUES%s"%str(values)
            cursor.execute(query_date)
            conn.commit()
            count +=1
        if(commit_count < 100 ):
            break
        time.sleep(6)
    insert_query = "UPDATE keyword_search_data SET commits_count=%s"%str(total_commit)+" WHERE id = %s"%(id)
    cursor.execute(insert_query)
    conn.commit()
    #print (" Total Commit : " + str(total_commit))
    return None

#fetch_commits_data_from_github(46092586,2177071)
'''
def clean_commit_data():
    connection = engine.raw_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM commit_table ORDER BY date ASC"
    cursor.execute(query)
    commit_data = cursor.fetchall()
    chk = commit_data[0]
    chk2 = commit_data[1]
    length = len(commit_data)
    newlen,j = 0,0
    for i in range(length):
        j=i+1
        if(j<length):
            if(commit_data[i] == commit_data[j]):
                newlen +=1
                print(commit_data[i])
                #delete_query = "DELETE FROM commit_table WHERE keyword_id=%s"%str(commit_data[j][0]+",id=%s"%str(commit_data[j][1])+",date=%s"%str(commit_data[j][2]))
    print(newlen)



clean_commit_data()'''

def get_commits_date_from_db(ID):
    connection = engine.raw_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    date_query ="SELECT date FROM commit_table WHERE id=%s"%(ID)+" ORDER BY date ASC"
    cursor.execute(date_query)
    result = cursor.fetchall()
    data = []
    print (type(data))
    for row in result:
        datte = row['date']
        datte = str(datte.date())
        #print(datte)
        data.append(datte)
        #data.append(row)    
        #print (type(row))
    #print((data))
    #data = json.dumps(data)
    d = {x:data.count(x) for x in data}
    label, value = d.keys(),d.values()

    return label,value#,start_date,last_date

    #print(min_price)
    #print(value)

    #return label,value
# labels = [row[0] for row in data
#get_commits_date_from_db(4332096)

'''with engine.connect() as conn:
        date_query = sa.text("SELECT date FROM commit_table WHERE id=%s"%(ID))
        result = conn.execute(date_query)
        #result = json.dumps(str(result))
        print(result)
        result = result.mappings().all()
        result = json.dumps(result)
        print(type(result))'''



#get_commits_date(4332096)


#url = "https://api.github.com/repos/donkirkby/live-py-plugin"

#fetch_commits_data_from_github(46092586,15524636)
#kid = 46092586
#load_keyword_all_details(kid)

#SELECT DISTINCT date FROM commit_table WHERE id = 4332096; to get unique date to make graph
'''tc = 1
total_commit = 0
while True:
    print(tc)
    print(url+"/commits?per_page=100&page="+str(tc))
    commit_count_response = requests.get(url+"/commits?per_page=100&page="+str(tc))
    commit_count_response = json.loads(commit_count_response.text)
    commit_count_response = json.dumps(commit_count_response) 
    commit_count = commit_count_response.count('"commit":') #counts number of commits
    print ('Number of commits : ',commit_count)
    total_commit = total_commit + commit_count
    tc += 1
    if(commit_count < 100):
        print ("Break")
        break
print (" Total Commit : " + str(total_commit))'''