import requests 
import time 
import random
from MySQLdb import MySQLError
import requests 
import mysql.connector
import pandas as pd
from pandas.tseries.offsets import MonthEnd,SemiMonthEnd,SemiMonthBegin,WeekOfMonth,Week
from datetime import datetime,timedelta
import time
#import urllib.request
import json
import sqlite3


'''
try:
    #connection to the database 
    con = mysql.connector.connect(
        user = 'root',
        password = '',
        host = 'localhost',
        database = 'search_data_storage'
    )
    #when no exception arrises the connection status changes to True 
    connected = True
except MySQLError as er:
    #to print the error when exception arises
    print ('Error connecting to database '+er)
'''

token = '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'
username = 'rn468'
endDate = datetime.today().strftime('%Y-%m-%d')
api_base="https://api.github.com/search/repositories?q="
#response = requests.get(api_base+keyword+':created:'+beg.strftime("%Y-%m-%d")+'..'+(beg+MonthEnd(1)).strftime("%Y-%m-%d"),auth=(username,token))
#last_date = (beg + MonthEnd(1)).strftime("%Y-%m-%d")

#startdate = '2022-07-01'
total_count  = 0

def optmiseSpeed(keyword,startdate):#keyword,startdate
    response = requests.get(api_base+keyword+':created:'+startdate+'..'+(beg+Week()).strftime("%Y-%m-%d"),auth=(username,token))
    time.sleep(6)
    response_count = response.json()['total_count']
    print(startdate+'-'+(beg+Week()).strftime("%Y-%m-%d"))
    if(response_count<=30):
        return response_count,response,'W'
    elif(response_count>30):
        return response_count,response,'D'

kw = 'Pycharm'

for beg in pd.date_range('2023-06-01',endDate,freq='W'):
    inner_loop_startdate = (beg+timedelta(days=1)).strftime("%Y-%m-%d")
    frequency_counter,json_response,freq = optmiseSpeed(kw,inner_loop_startdate)
    print(str(frequency_counter) + " : " + str(json_response.json()['total_count']) + " : " +  str(freq))
    total_count = total_count + frequency_counter
    
if(freq == 'D'):
    print ('Week '+ inner_loop_startdate + ' : ' + (beg+Week()).strftime("%Y-%m-%d"))
    for beg in pd.date_range(inner_loop_startdate,(beg+Week()).strftime("%Y-%m-%d"),freq='D'):
        response = requests.get(api_base+kw+':created:'+beg.strftime("%Y-%m-%d")+'..'+beg.strftime("%Y-%m-%d"),auth=(username,token))
        print ('Total Count : '+ str(response.json()['total_count']) + ' : ' + beg.strftime("%Y-%m-%d")+'-'+beg.strftime("%Y-%m-%d"))
        time.sleep(6)
else:
        print('Week')

print ('Total Count = '+ str(total_count))
'''for beg in pd.date_range('2022-07-01',endDate,freq='W'):
    inner_loop_startdate = (beg+timedelta(days=1)).strftime("%Y-%m-%d")
    print (inner_loop_startdate,(beg+Week()).strftime("%Y-%m-%d"))
'''

'''def optmiseSpeed(startdate):#keyword,startdate
    resonse_count = 0
    #for beg in pd.date_range(startdate,endDate,freq='MS'):
    for beg in pd.date_range(startdate,endDate):
        response = requests.get(api_base+'pycharm'+':created:'+beg.strftime("%Y-%m-%d")+'..'+(beg+MonthEnd(1)).strftime("%Y-%m-%d"),auth=(username,token))
        time.sleep(6)
        resonse_count = response.json()['total_count']
        print(str(resonse_count)+' : '+beg.strftime("%Y-%m-%d")+'-'+(beg+MonthEnd(1)).strftime("%Y-%m-%d"))
        if(resonse_count<=30):
            return 30,response,
        elif(resonse_count>30 and 60<=resonse_count):
            response = requests.get(api_base+'pycharm:created:'+beg.strftime("%Y-%m-%d")+'..'+(beg+ pd.offsets.SemiMonthEnd()).strftime("%Y-%m-%d"),auth=(username,token))
            time.sleep(6)
            resonse_count = response.json()['total_count']
            print(str(resonse_count)+' : '+beg.strftime("%Y-%m-%d")+'-'+(beg+ pd.offsets.SemiMonthEnd()).strftime("%Y-%m-%d"))
            if(resonse_count<=30):
                return 15,response
        elif(resonse_count>60 and 120<=resonse_count):
            response = requests.get(api_base+'pycharm:created:'+beg.strftime("%Y-%m-%d")+'..'+(beg+timedelta(days=7)).strftime("%Y-%m-%d"),auth=(username,token))
            time.sleep(6)
            resonse_count = response.json()['total_count']
            print(str(resonse_count)+' : '+beg.strftime("%Y-%m-%d")+'-'+(beg+timedelta(days=7)).strftime("%Y-%m-%d"))
            if(resonse_count<=30):
                return 7,response
        else:
            return 1
'''

'''for beg in pd.date_range('2022-07-01',endDate,freq='D'):
        #print(beg.strftime("%Y-%m-%d"))
        #response = requests.get(api_base+'Aarch64'+':created:'+beg.strftime("%Y-%m-%d")+'..'+(beg+MonthEnd(1)).strftime("%Y-%m-%d"),auth=(username,token))
        #print(response.json()['total_count'])
        print (beg.strftime("%Y-%m-%d")+'-'+(beg+timedelta(days=1)).strftime("%Y-%m-%d"))
        time.sleep(1)
        #response = requests.get(api,auth=(username,token))
        #total_count = response.json()['total_count']
        #if(total_count>30):
        #    continue
        #else:
        #    break
'''

'''response = json.loads(response.text)
response = json.dumps(response)
print(response)
'''

'''last_date = datetime.today().strftime('%Y-%m-%d')
keyword_id = 46092586
cursor = con.cursor()
cursor.execute("UPDATE searched_keyword SET completion_status=1, last_data_fetched_at=%s WHERE keyword_id = %s",(last_date,keyword_id,))
con.commit()

'''

'''start_time = time.time()
for i in range(0,100):
    time.sleep(0.74)
    end_time = time.time()
    print(i,end_time-start_time)

print(end_time-start_time)
'''


'''

api = 'https://api.github.com/search/repositories?q=Pycharm:created:2020-01-01..2020-01-05'
response = requests.get(api,auth=(username,token))
response = json.loads(response.text)
response = json.dumps(response)
print(response)

'''


#api_base = "https://api.github.com/search/repositories?q=Aarch64";
#api_base = "http://dw.euro.who.int/api/v3/data_sets/HFAMDB/HFAMDB_8"

'''with open("sdata.csv","w") as outfile:
    outfile.write("id,name,full_name,url,created_at,language\n") #,description
    response = requests.get(api_base)
    for item in response.json()['items']:
        id = item['id']
        name = item['name']
        full_name = item['full_name']
     #   description = item['description']
        url = item['url']
        created_at = item['created_at'] 
        language = item['language']
        outfile.write("{},{},{},{},{},{}\n".format(id,name,full_name,url,created_at,language))#,description
'''


'''
with open("population.csv", "w") as outfile:
#    outfile.write("country,year,group,fullname,count\n")
    outfile.write("year,fullname,count\n")
    for i in range(32,33):
        response = requests.get(api_base+str(i))
        print(api_base+str(i))

        for observation in response.json()['data']:
            count = observation["value"]["numeric"]
            country = observation["dimensions"]["COUNTRY"]
            year = observation["dimensions"]["YEAR"]
            group = observation["dimensions"]["AGE_GRP_6"]
            fullGroupName = response.json()['full_name']
            if observation["dimensions"]["SEX"] == "ALL":
                outfile.write("{},{},{},{},{}\n".format(country, year, group, fullGroupName, count))  
'''
                

'''        data = response.json()
        for observation in data['data']:
            fullGroupName = data['full_name']
            year = observation["dimensions"]["YEAR"]
            count = observation["value"]["numeric"]
            outfile.write("{},{},{}\n".format(year,fullGroupName,count))
'''

