import requests 
import pandas as pd
from pandas.tseries.offsets import MonthEnd
from datetime import datetime
import time
#import urllib.request
import json


api_base = "https://api.github.com/search/repositories?q=Aarch64:created:";

with open("sdatadate.csv","a") as outfile:
    outfile.write("id,node_id,name,full_name,url,commits_url,downloads_url,issues_url,pulls_url,created_at,language,forks\n") #,description
    #to current date and pass it as a varoable to to loop to stop the iteration
    endDate = datetime.today().strftime('%Y-%m-%d')
   # print (endDate,type(endDate),type('2014-02-10'))
   # count = 1
    #opening up a json file to save the data
    file = open("datajson.json","w")

    for beg in pd.date_range('2017-09-01', endDate, freq='MS'):
    #    count = count + 1
        
        response = requests.get(api_base+beg.strftime("%Y-%m-%d")+'..'+(beg + MonthEnd(1)).strftime("%Y-%m-%d"))

        #to save file in json 
        # data = response   
        #file.write(response.read())

        for item in response.json()['items']:
            id = item['id']                 #repository id 
            node_id = item['node_id'] #
            name = item['name']             #repository name 
            full_name = item['full_name']   #owner name and repository name 
        #   description = item['description']
            url = item['url']               #repository url
            commits_url = item['commits_url'] # all commits url
            downloads_url = item['downloads_url'] #all downloads url
            issues_url = item['issues_url'] #all issues URL
            pulls_url = item['pulls_url']   #All the pulls url
          
            created_at = item['created_at'] #stores the created date
            language = item['language']     #Primary language used in repository
            forks = item['forks']           #Numbers of forks
            outfile.write("{},{},{},{},{},{},{},{},{},{},{},{}\n".format(id,node_id,name,full_name,url,commits_url,downloads_url,issues_url,pulls_url,created_at,language,forks))#,description'''
        print(beg.strftime("%Y-%m-%d"), (beg + MonthEnd(1)).strftime("%Y-%m-%d"))
        time.sleep(60)
   # print(count)




#for beg in pd.date_range('2014-01-01', '2014-06-30', freq='MS'):
#    print(beg.strftime("%Y-%m-%d"), (beg + MonthEnd(1)).strftime("%Y-%m-%d"))