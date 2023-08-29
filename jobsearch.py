from JobsDB_bot import jobsdbBot

domain = "https://hk.jobsdb.com/"
job_keyword = '' #job position e.g programmer
locations = '' , '', ''#locations only 1 location, requires to use [] e.g [Eastern] >1 e.g 'Wan Chai','Eastern' MAX:5 
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
dates = [''] #requires only put ONE input e.g ['1 day']
"""
All
1 day
3 days
7 days
14 days
30 days
"""
jobtypes = [''] #only 1 location, requires to use [] e.g ['FT'] Can select all e.g 'FT', 'PT'...
"""
'FT'
'PT'
'Perm'
'Tem'
'Cont'
'Intern'
'Free'
"""
jobfunctions = [''] #jobfunctions only 1 function, requires to use [] e.g [1] >1 functions e.g '3','5' MAX:5
"""
1:"All"
2:"Accounting"
3:"Admin & HR"
4:"Banking / Finance"
5:"Beauty / Health"
6:"Building & Construction"
7:"Design"
8:"E-commerce"
9:"Education"
10:"Enginnering"
11:"Hospitality / F & B"
12:"IT"
13:"Insurance"
14:"Management"
15:"Manfacturing"
16:"Marketing / PR"
17:"Media / Ads"
18:"Medical Services"
19:"Merchant & Purchase"
20:"Professional Service"
21:"Property / Real Estate"
22:"Public / Civil"
23:"Sales / CS & Business Devpt"
24:"Sciences, Lab, R&D"
25:"Transportation & Logistics"
26:"Others"
"""
format = '' #requires to select one format e.g 'excel'
"""
excel
csv
all
"""
bot = jobsdbBot(domain, job_keyword,locations,dates,jobtypes,jobfunctions,format)
bot.start()
#python3 jobsearch.py

