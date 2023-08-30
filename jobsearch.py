from JobsDB_bot import jobsdbBot

domain = "https://hk.jobsdb.com/"
#testing debug
# bot = jobsdbBot(domain, 'business analyst',[4,17,7],[1],[1,2],[1,12,8],'all')
# bot.start()
job_keyword = input("Please input job keyword: ")
locations = input("""
====================================
1.  All 全部
2.  Central & Western 中西區
3.  Cheung Chau 長州
4.  Eastern 東區
5.  Kowloon City 九龍城
6.  Kwai Tsing 葵青
7.  Kwun Tong 觀塘
8.  Lantau Island 大嶼山
9.  Northern NT 新界北
10. Sai Kung 西貢
11. Sham Shui Po 深水埗
12. Shatin 沙田
13. Southern 南區
14. Tai Po 大埔
15. Tsuen Wan 荃灣
16. Tuen Mun 屯門
17. Wan Chai 灣仔
18. Wong Tai Sin 黃大仙
19. Yau Tsim Mong 油尖旺
20. Yuen Long 元朗
====================================
Please input location index:""")
locations = [int(x) for x in locations.split(',')]
dates = input("""
====================================
1. All
2. 1 day
3. 3 days
4. 7 days
5. 14 days
6. 30 days
====================================
Please input dates index:""")
dates = [int(x) for x in dates.split(',')]
jobtypes = input("""
====================================
1. Full Time  
2. Part Time  
3. Permanent  
4. Temporary  
5. Contract
6. Intern
7. Freelance
====================================
Please input jobtypes index:""")
jobtypes = [int(x) for x in jobtypes.split(',')]
jobfunctions = input("""
====================================
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
====================================
Please input jobfunctions index:""")
jobfunctions = [int(x) for x in jobfunctions.split(',')]
format = input("""
====================================               
excel
csv                              
all               
Please input desired formats:""")

bot = jobsdbBot(domain, job_keyword,locations,dates,jobtypes,jobfunctions,format)
bot.start()
#python3 jobsearch.py