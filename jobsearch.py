from jobsdb_bot import jobsdbBot

domain = "https://hk.jobsdb.com/"
job_keyword = "programmer" #keyword to search
locations = ['Eastern','Wan Chai','Kwun Tong']
#format = "" #excel or csv
bot = jobsdbBot(domain, job_keyword)
bot.start()
#python3 jobsearch.py