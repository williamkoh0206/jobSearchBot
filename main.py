from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import pandas as pd

fn='jobsDB_Post.csv'
columns_name=['職位名稱','公司名稱','地區','工作詳情','發佈時間','網址']


driver = webdriver.Chrome()
domain = "https://hk.jobsdb.com/"
driver.get(domain)
driver.fullscreen_window()
time.sleep(1)

search = driver.find_element(By.ID, "searchKeywordsField")
search.send_keys("programmer")
search.send_keys(Keys.RETURN)

selectLocation = driver.find_element(By.CSS_SELECTOR, ".z1s6m00 [data-automation='locationChecklistField']").click()


locations = driver.find_elements(By.CSS_SELECTOR, ("div.z1s6m00 input.z1s6m00"))
selectedLocations = [5,8,18]
#Eastern Area: Index:5"
#Kwun Tong Area: Index:8"
#Wan Chai Area: Index:18"

for index in selectedLocations:
    if index < len(locations):
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.z1s6m00 input.z1s6m00")))
            locations[index-1].click()
            time.sleep(1)
        except:
            print("Cannot found the locations")
searchButton = driver.find_element(By.CSS_SELECTOR, ("button[data-automation='searchSubmitButton']")).click()
time.sleep(2)

datePostButton = driver.find_element(By.CSS_SELECTOR, ("button[data-automation='createdAtFilterButton']")).click()
dates = driver.find_element(By.XPATH,("//span[normalize-space()='Last 7 days']")).click()
dateApplyBtn = driver.find_element(By.CSS_SELECTOR, ("button[data-automation='refinementFormApplyButton']")).click()
time.sleep(1)
clickJobPosts = driver.find_elements(By.CSS_SELECTOR,"article.z1s6m00")
driver.execute_script("window.scrollBy(0,25);")
for el in clickJobPosts:
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "article.z1s6m00")))
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "article.z1s6m00")))
        el.click()
        time.sleep(0.5)
    except:
        print("Element is not clickable or not found.")

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-automation='jobDetailsLinkNewTab'] a")))

page = driver.page_source
soup = BeautifulSoup(page, 'lxml')
jobs = soup.select("article.z1s6m00")

companyName = soup.select("article div.z1s6m00 span.z1s6m00 a[data-automation='jobCardCompanyLink']")
jobPosition = soup.select("article div.z1s6m00 h1.z1s6m00 span.z1s6m00")
jobUrls = soup.select("article.z1s6m00 h1.z1s6m00 a")
jobHighlights = soup.select("ul.z1s6m00 li")
jobLocation = soup.select("span.z1s6m00 a[data-automation='jobCardLocationLink']")
postedDate = soup.select("div.z1s6m00 time span")


print("Numbers of jobs: " + str(len(jobs)))
print("=" * 70)

#open the csv file for writing
with open(fn, 'w', newline='',encoding='utf_8_sig') as csvFile:
    dictWriter = csv.DictWriter(csvFile, fieldnames=columns_name)
    dictWriter.writeheader()

    for i in range(len(jobs)):
        # Print Job Information
        print("JobPost:", jobPosition[i].text)
        if i < len(companyName):
            print("Company:", companyName[i].text)
        if i < len(jobLocation):
            print("Location:", jobLocation[i].text)
        # Find and print Job Highlights
        job = jobs[i]
        jobHighlights = job.select("ul.z1s6m00 li")
        print("Job Highlights:")
        for highlight in jobHighlights:
            print("  *", highlight.text)
        if i < len(postedDate):
            print("Posted on:",postedDate[i].text)
        if i < len(jobUrls):
            link = jobUrls[i].get('href')
            print("URL:", domain + link)
        print("=" * 70)

        #Write job details to the CSV file
        dictWriter.writerow(
            {'職位名稱': jobPosition[i].text,
            '公司名稱': companyName[i].text if i < len(companyName) else '',
            '地區': jobLocation[i].text if i < len(jobLocation) else '',
            '工作詳情': '\n'.join([highlight.text for highlight in jobHighlights]),
            '發佈時間': postedDate[i].text if i < len(postedDate) else '',
            '網址': domain + link if i < len(jobUrls) else ''
            }
        )
job_data = []
for data in range(len(jobs)):
    # Find and print Job Highlights (inside the loop)
    job = jobs[data]
    jobHighlights = job.select("ul.z1s6m00 li")
    # Find and print URL (inside the loop)
    link = jobUrls[data].get('href')
    
    jobs_dict = {
        '職位名稱': jobPosition[data].text,
        '公司名稱': companyName[data].text if data < len(companyName) else '',
        '地區': jobLocation[data].text if data < len(jobLocation) else '',
        '工作詳情': '\n'.join([highlight.text for highlight in jobHighlights]),
        '發佈時間': postedDate[data].text if data < len(postedDate) else '',
        '網址': domain + link if data < len(jobUrls) else ''
    }
    job_data.append(jobs_dict)
# Create a pandas DataFrame from the list of dictionaries
df = pd.DataFrame(job_data)

# Save the DataFrame to an Excel file
excel_file = 'jobsDB_Post.xlsx'
df.to_excel(excel_file, index=False)

driver.quit()

