#import mysql.connector

import requests
# module for fetching URLs (Uniform Resource Locators) or it defines functions and classes which help in opening URLs
import urllib.request  
import json 

#api url for retrieving the data 
url = ('https://api.github.com/search/repositories?q=Aarch64') 


#this is to open the URL url, which can be either a string or a Request object
response = urllib.request.urlopen(url)

#we need to read the data and decode it into UTF-8 
data = response.read().decode('UTF-8')

#open the file and write data in it,open() returns a file object
file = open("data.json","w")
#write() is to write the data into file
file.write(data)

#after the decoded the response, load the data in another variable using json.loads() this is used convert str data to object
new_data = json.loads(data)
#/get_articles = new_data['articles']

#to convert we use json.dumps() used to convert object to str
new_data_articles = json.dumps(new_data)


 #to open and read the data from the file
f = open('data.json')
rdata = json.load(f)

#for i in rdata['items.id']:
#    print

f.close()



