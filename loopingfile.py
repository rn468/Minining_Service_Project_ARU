import requests 
api_base = "https://api.github.com/search/repositories?q=Aarch64";
#api_base = "http://dw.euro.who.int/api/v3/data_sets/HFAMDB/HFAMDB_8"

with open("sdata.csv","w") as outfile:
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

