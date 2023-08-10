from jobsdb_bot import jobsdbBot

domain = "https://hk.jobsdb.com/"
job_keyword = "programmer" #keyword to search
locations = ['Eastern','Wan Chai','Kwun Tong','Kwai Tsing','Sai Kung']
#format = "" #excel or csv

bot = jobsdbBot(domain, job_keyword,locations)
bot.start()
#python3 jobsearch.py