from JobsDB_bot import jobsdbBot

domain = "https://hk.jobsdb.com/"
job_keyword = "programmer" #keyword to search
locations = 'Eastern','Wan Chai' 
dates = 'All'
format = 'excel'

bot = jobsdbBot(domain, job_keyword,locations,dates,format)
bot.start()
#python3 jobsearch.py

#Dates
"""
All
1 day
3 days
7 days
14 days
"""

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
