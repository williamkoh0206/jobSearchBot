from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import traceback

PATH = "C:/Users/William/Desktop/ECJobapply/chromedriver.exe"
driver = webdriver.Chrome()
domain = "https://hk.jobsdb.com/"
driver.get(domain)
driver.fullscreen_window()
time.sleep(1)

search = driver.find_element(By.ID, "searchKeywordsField")
search.send_keys("programmer")
search.send_keys(Keys.RETURN)

selectLocation = driver.find_element(By.CLASS_NAME, "_23enrv0").click()

#Eastern Area: label id="Select-0-166"
#Kwun Tong Area: label id="Select-0-130"
#Wan Chai Area: label id="Select-0-146"

locations1 = driver.find_element(By.XPATH, ("//label[@for='Select-0-166']")).click()
# locations2 = driver.find_element(By.XPATH, ("//label[@for='Select-0-130']")).click()
# locations3 = driver.find_element(By.XPATH, ("//label[@for='Select-0-146']")).click()
searchButton = driver.find_element(By.XPATH, ("//button[@type='submit']")).click()
time.sleep(3)

datePostButton = driver.find_element(By.XPATH, ("//button[normalize-space()='Date posted']")).click()
dateOption = driver.find_element(By.XPATH, ("//span[normalize-space()='Last 7 days']")).click()
dateApplyButton = driver.find_element(By.XPATH, ("//button[normalize-space()='Apply']")).click()
time.sleep(2)
clickJobPosts = driver.find_elements(By.CSS_SELECTOR,"article.z1s6m00")
for el in clickJobPosts:
    el.click()
    time.sleep(0.5)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-automation='jobDetailsLinkNewTab'] a")))

page = driver.page_source
soup = BeautifulSoup(page, 'lxml')
jobs = soup.select("article.z1s6m00")

companyName = soup.select("article div.z1s6m00 span.z1s6m00 a[data-automation='jobCardCompanyLink']")
jobPosition = soup.select("article div.z1s6m00 h1.z1s6m00 span.z1s6m00")
url = soup.select("div[data-automation='jobDetailsLinkNewTab'] a")
jobHighlights = soup.select("ul.z1s6m00 li")
jobLocation = soup.select("span.z1s6m00 a[data-automation='jobCardLocationLink']")


print("Numbers of jobs: " + str(len(jobs)))

for i, job in enumerate(jobs):
    # Print Job Information
    print("JobPost:", jobPosition[i].text)
    if i < len(companyName):
        print("Company:", companyName[i].text)
    if i < len(jobHighlights):
        print("Job Highlights:", jobHighlights[i].text)
    if i < len(jobLocation):
        print("Location:", jobLocation[i].text)
    if i < len(url):
        link = url[i].get('href')
        print("URL:", domain + link)
    print("=" * 70)

driver.quit()


