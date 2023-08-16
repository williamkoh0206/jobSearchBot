from jobsdb_bot import jobsdbBot

domain = "https://hk.jobsdb.com/"
job_keyword = "programmer" #keyword to search
locations = ['Eastern','Wan Chai'] 
dates = ['1 day']
#format = "" #excel or csv

bot = jobsdbBot(domain, job_keyword,locations,dates)
bot.start()
#python3 jobsearch.py
#Max 5 locations 
"""
All
Central & Western
Cheung Chau
Eastern
Kowloon City
Kwai Tsing
Kwun Tong
Lantau Island
Northern NT
Sai Kung
Sham Shui Po
Shatin
Southern
Tai Po
Tsuen Wan
Tuen Mun
Wan Chai
Wong Tai Sin
Yau Tsim Mong
Yuen Long
"""
