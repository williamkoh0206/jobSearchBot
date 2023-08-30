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
1. All 全部
2. 1 day 1日前刊登
3. 3 days 3日前刊登
4. 7 days 7日前刊登
5. 14 days 14日前刊登
6. 30 days 30日前刊登
====================================
Please input dates index:""")
dates = [int(x) for x in dates.split(',')]
jobtypes = input("""
====================================
1. Full Time 全職  
2. Part Time 兼職  
3. Permanent 長期工作  
4. Temporary 臨時工作  
5. Contract 合約
6. Intern 實習
7. Freelance 自由職業
====================================
Please input jobtypes index:""")
jobtypes = [int(x) for x in jobtypes.split(',')]
jobfunctions = input("""
====================================
1:All 全部
2:Accounting 會計
3:Admin & HR 行政及人力資源 
4:Banking / Finance 銀行/金融
5:Beauty / Health 美容/健康
6:Building & Construction 建築與施工
7:Design 設計
8:E-commerce 電子商務
9:Education 教育
10:Enginnering 工程
11:Hospitality / F & B 酒店/餐飲
12:IT 資訊科技
13:Insurance 保險
14:Management 管理
15:Manfacturing 製造
16:Marketing / PR 營銷/公關
17:Media / Ads 媒體/廣告
18:Medical Services 醫療服務
19:Merchant & Purchase 商戶採購
20:Professional Service 專業服務
21:Property / Real Estate 財產/房地產
22:Public / Civil 公共/民用
23:Sales / CS & Business Devpt 銷售/客戶服務和業務開發
24:Sciences, Lab, R&D 科學、實驗室、研發
25:Transportation & Logistics 運輸與物流
26:Others 其他
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