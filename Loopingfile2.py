import requests 
import mysql.connector
import pandas as pd
from pandas.tseries.offsets import MonthEnd
from datetime import datetime
import time
#import urllib.request
import json


#base api which will be used to call
api_base = "https://api.github.com/search/repositories?q=Aarch64:created:";


#working code for saving data to csv 
#opening a csv file to store the data with "a" append mode or "w" write mode 
with open("sdatadateTEMP.csv","a") as outfile:
    #will create the headers for the columns 
    outfile.write("id,node_id,name,full_name,url,commits_url,downloads_url,issues_url,pulls_url,created_at,language,forks\n") #,description
    #to get the current date and pass it as a varoable to to loop to regulate the iteration
    endDate = datetime.today().strftime('%Y-%m-%d')
    #count = 1
    #opening up a json file to save the data
    #file = open("datajson.json","w")

    #for loop that will run from a given date to current data with frequency "MS" month
    for beg in pd.date_range('2017-09-01', endDate, freq='MS'):
    #    count = count + 1
        #the base api is called with the begining date and end date as parameter
        #the beginning date and end date will slice the data in order to stay within the limit as we only get certain amount of data per call
        response = requests.get(api_base+beg.strftime("%Y-%m-%d")+'..'+(beg + MonthEnd(1)).strftime("%Y-%m-%d"))

        #to save file in json 
        # data = response   
        #file.write(response.read())

        #this loop saves the data recieved in response to the variables so that the variables can be used later on
        for item in response.json()['items']:
            id = item['id']                 #repository id 
            node_id = item['node_id']       #repository node id
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
            #this will insert the data into the csv file into the respective order
            outfile.write("{},{},{},{},{},{},{},{},{},{},{},{}\n".format(id,node_id,name,full_name,url,commits_url,downloads_url,issues_url,pulls_url,created_at,language,forks))#,description
            
            #to save the last date incase if there is an issue and loop stops we have record of the date 
            last_date = (beg + MonthEnd(1)).strftime("%Y-%m-%d")
        #this displays the date in terminal 
        print(beg.strftime("%Y-%m-%d"), (beg + MonthEnd(1)).strftime("%Y-%m-%d"))
        #sleep timer to control the number of calls made as currently we have 60 calls per hour limit and exciding limit will give 503 error
        time.sleep(60)

print ('The last data is : '+last_date)
   # print(count)


#for beg in pd.date_range('2014-01-01', '2014-06-30', freq='MS'):
#    print(beg.strftime("%Y-%m-%d"), (beg + MonthEnd(1)).strftime("%Y-%m-%d"))