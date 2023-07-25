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



#base api which will be used to call
#api_base = "https://api.github.com/search/repositories?q=Aarch64:created:"
endDate = datetime.today().strftime('%Y-%m-%d')



#By default the connected is initialized as false stating its not-connected
connected = False
#to catch exception when connecting to database 
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



#this function will check if the keyword is already present in table 
#if the keyword is present then it will return the status and 
#if the keyword is not present in table then the keyword will be inserted and a new id will be generated along with the timestamp
def check_keyword(ckeyword):
    try:
        cursor = con.cursor()
        if connected:
            #query to check if the keyword is already present,passing keyword as parameter
            check_query = "SELECT keyword_id FROM searched_keyword WHERE keyword_title = '"+ckeyword+"'"
            cursor.execute(check_query)
            result = cursor.fetchone() is None
            #if the returned result is FALSE then the keyword is PRESENT and if the result is TRUE then the keyword is ABSENT 
            #print (result)
            if result:
                loop = True
                while loop == True:
                    rand_id = random.randint(10000000, 99999999)#generate random number (8 digits)
                    try:
                        cursor.execute('SELECT * FROM searched_keyword WHERE keyword_id = ?',(rand_id,))#select the row in the users table where id == the rand_id variable
                        r_id = cursor.fetchone()[0]#r_id = the first column from that row ## this is just here to throw the error
                        print (r_id)
                    except:
                        #cursor.execute('INSERT INTO users (id, username, password1) VALUES (?, ?, ?)',(rand_id, usernamex, password1x))#make a new row, and put in ID, username and password1 in their respective places
                        insert_keyword_query = "INSERT INTO searched_keyword(keyword_id,keyword_title,last_updated_date) VALUES(%s,%s,%s)"
                        value = (rand_id,ckeyword,endDate)
                        cursor.execute(insert_keyword_query,value)
                        con.commit()
                        loop = False#break the loop
    
        # The below code is performing two SQL queries.
        last_date_query = "SELECT last_updated_date FROM searched_keyword WHERE keyword_title = '"+ckeyword+"'"
        keyword_query = "SELECT keyword_id FROM searched_keyword WHERE keyword_title = '"+ckeyword+"'"
        # The below code is executing a SQL query using a cursor object. The specific query being
        # executed is stored in the variable `last_date_query`.
        cursor.execute(last_date_query)
        # The below code is fetching the value of the first column from the result of a database query
        # using the `fetchone()` method and assigning it to the variable `last_date`.
        last_date = cursor.fetchone()[0]
        '''for date in last_date:
            last_date = date[0]'''
        
        # The below code is executing a SQL query using a cursor object. It is fetching the first row
        # of the result set and retrieving the value at index 0. This value is then assigned to the
        # variable keyword_id.
        cursor.execute(keyword_query)
        keyword_id = cursor.fetchone()[0]
        print (last_date)
        print(keyword_id)
        # The below code is defining a Python function that returns two variables, `last_date` and
        # `keyword_id`. The function does not have a name, so it cannot be called directly.
        return last_date,keyword_id
    finally:
        con.close()
       



#ckww = 'Trial3'
#result = check_keyword(ckww)    
#if (result == False):
#    print("Present")
#else:
#    print("Not Present")


#incomplete
#in stage 1 collection the data will be ready available data will be collected and stored in data base
#will return the last date and if the last date is not same as current date then it means that all the data 
def stage1_collection(keyword): 
    if connected:
        api_base2="https://api.github.com/search/repositories?q="
        cursor = con.cursor()
        for beg in pd.date_range('2020-01-01',endDate,freq='MS'):
            response = requests.get(api_base2+keyword+':created:'+beg.strftime("%Y-%m-%d")+'..'+(beg+MonthEnd(1)).strftime("%Y-%m-%d"))
            for item in response.json()['items']:
                keyword_id = 1001
                id = item['id']                 #repository id 
                node_id = item['node_id']       #repository node id
                name = item['name']             #repostory name 
                full_name = item['full_name']   #owner name and repository name 
                description = item['description']
                url = item['url']               #repository url
                commits_url = item['commits_url'] # all commits url
                downloads_url = item['downloads_url'] #all downloads url
                issues_url = item['issues_url'] #all issues URL
                pulls_url = item['pulls_url']   #All the pulls url

                #repo_url = 
                #languages_url = 
                #comments_url = 

                created_at = item['created_at'] #stores the created date
                language = item['language']     #Primary language used in repository
                if (language == ' '):
                    language = 'not available'    
                forks = item['forks']           #Numbers of forks
                repo_size = item['size']
                watchers = item['watchers']
                query = "INSERT INTO keyword_search_data(keyword_id,id,node_id,name,full_name,description,repo_url,commits_url,downloads_url,pulls_url,created_at,repo_size,language,watchers) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                value = (keyword_id,id,node_id,name,full_name,description,url,commits_url,downloads_url,pulls_url,created_at,repo_size,language,watchers)
                cursor.execute(query,value)
                con.commit()
                print("inserted")
            last_date = (beg + MonthEnd(1)).strftime("%Y-%m-%d")
            time.sleep(60)
        con.close()
        print ('Data inserted into database unitil '+last_date)
    return last_date

#DRY Running the function 
#kww = 'Xampp'
#stage1_collection(kww)


#this stage 1 collection with 2 parameters will be called when the stage 1 data is incomplete and the remaining data is collected using these 2 parameters 
# 1. the keyword and 2.last date until which data was collected
# it will return the last date to chech if data is collected till current date. 
    """
    The function `stage1_collection1` collects data from the GitHub API based on a given keyword and
    start date, and inserts the collected data into a database, returning the last date for which data
    was collected.
    
    :param keyword: The keyword parameter is used to specify the search term for the GitHub
    repositories. It is the term that you want to search for in the repository names, descriptions, etc
    :param startDate: The `startDate` parameter is the starting date from which you want to collect
    data. It is used to specify the beginning of the date range for searching repositories on GitHub
    :return: The function will return the last date until which data has been collected and inserted
    into the database.
    """


def stage1_collection1(keyword,startDate):
    if connected:
        api_base2="https://api.github.com/search/repositories?q="
        cursor = con.cursor()
        for beg in pd.date_range(startDate,endDate,freq='MS'):
            response = requests.get(api_base2+keyword+':created:'+beg.strftime("%Y-%m-%d")+'..'+(beg+MonthEnd(1)).strftime("%Y-%m-%d"))
            for item in response.json()['items']:
                keyword_id = 1000
                id = item['id']                 #repository id 
                node_id = item['node_id']       #repository node id
                name = item['name']             #repostory name 
                full_name = item['full_name']   #owner name and repository name 
                description = item['description']
                url = item['url']               #repository url
                commits_url = item['commits_url'] # all commits url
                downloads_url = item['downloads_url'] #all downloads url
                issues_url = item['issues_url'] #all issues URL
                pulls_url = item['pulls_url']   #All the pulls url

                #repo_url = 
                #languages_url = 
                #comments_url = 

                created_at = item['created_at'] #stores the created date
                language = item['language']     #Primary language used in repository
                forks = item['forks']           #Numbers of forks
                repo_size = item['size']
                watchers = item['watchers']
                query = "INSERT INTO keyword_search_data(keyword_id,id,node_id,name,full_name,description,repo_url,commits_url,downloads_url,pulls_url,created_at,repo_size,language,watchers) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                value = (keyword_id,id,node_id,name,full_name,description,url,commits_url,downloads_url,pulls_url,created_at,repo_size,language,watchers)
                cursor.execute(query,value)
                con.commit()
            last_date = (beg + MonthEnd(1)).strftime("%Y-%m-%d")
            time.sleep(60)
        con.close()
        print ('Data inserted into database unitil '+last_date)
    return last_date



#This function is responsible for collecting additional information about repositories from Github API
def stage2_collection(keywordID):
    cursor = con.cursor()
    if connected:
        fetch_url_query = ""


#This function will be responsible for controlling all the functions and also for the user flow
def main():
      #keyword : will store the keyword we are searching for 
      #lastdate : will store the last 
      #status  : will store the completion status ,if the data collection was completed or not 
      keyword = input("Please insert the keyword : ")
      lastdate,keywordID = check_keyword(keyword)
      print (lastdate)
      print (keywordID)

main()


'''

if connected:
    #creating a cursor using cursor object cursor()
    cursor = con.cursor()
    #loop to slice the data set by the means of date ,slice data with one month frequency 'MS'
    for beg in pd.date_range('2020-01-01', endDate, freq='MS'):
        #response = requests.get(api_base+beg.strftime("%Y-%m-%d")+'..'+(beg + MonthEnd(1)).strftime("%Y-%m-%d"))
        response = requests.get(api_base+beg.strftime("%Y-%m-%d")+'..'+(beg + MonthEnd(1)).strftime("%Y-%m-%d"))
        for item in response.json()['items']:
            keyword_id = 1000  #temporary basis lateron we will fetch it form searched keyword tabel 
            id = item['id']                 #repository id 
            node_id = item['node_id']       #repository node id
            name = item['name']             #repostory name 
            full_name = item['full_name']   #owner name and repository name 
            description = item['description']
            url = item['url']               #repository url
            commits_url = item['commits_url'] # all commits url
            downloads_url = item['downloads_url'] #all downloads url
            issues_url = item['issues_url'] #all issues URL
            pulls_url = item['pulls_url']   #All the pulls url

            #repo_url = 
            #languages_url = 
            #comments_url = 

            created_at = item['created_at'] #stores the created date
            language = item['language']     #Primary language used in repository
            forks = item['forks']           #Numbers of forks
            repo_size = item['size']
            watchers = item['watchers']
            query = "INSERT INTO keyword_search_data(keyword_id,id,node_id,name,full_name,description,repo_url,commits_url,downloads_url,pulls_url,created_at,repo_size,language,watchers) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            value = (keyword_id,id,node_id,name,full_name,description,url,commits_url,downloads_url,pulls_url,created_at,repo_size,language,watchers)
            cursor.execute(query,value)
            con.commit()
        last_date = (beg + MonthEnd(1)).strftime("%Y-%m-%d")
        time.sleep(60)
    con.close()
    print ('Data inserted into database unitil '+last_date)
'''
'''    
    #for loop that will run from a given date to current data with frequency "MS" month
#for beg in pd.date_range('2017-09-01', endDate, freq='MS'):
    #    count = count + 1
        #the base api is called with the begining date and end date as parameter
        #the beginning date and end date will slice the data in order to stay within the limit as we only get certain amount of data per call
    #response = requests.get(api_base+beg.strftime("%Y-%m-%d")+'..'+(beg + MonthEnd(1)).strftime("%Y-%m-%d"))

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

#working code for saving data to csv 

#opening a csv file to store the data with "a" append mode or "w" write mode 

with open("sdatadate.csv","a") as outfile:
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

print ('The last data is : '+last_date)'''
   # print(count)


#for beg in pd.date_range('2014-01-01', '2014-06-30', freq='MS'):
#    print(beg.strftime("%Y-%m-%d"), (beg + MonthEnd(1)).strftime("%Y-%m-%d"))