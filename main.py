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

locations1 = driver.find_element(By.XPATH, ("//label[@for='Select-0-166']")).click()
# locations2 = driver.find_element(By.XPATH, ("//label[@for='Select-0-130']")).click()
# locations3 = driver.find_element(By.XPATH, ("//label[@for='Select-0-146']")).click()
searchButton = driver.find_element(By.XPATH, ("//button[@type='submit']")).click()
time.sleep(3)

datePostButton = driver.find_element(By.XPATH, ("//button[normalize-space()='Date posted']")).click()
dateOption = driver.find_element(By.XPATH, ("//span[normalize-space()='Last 7 days']")).click()
dateApplyButton = driver.find_element(By.XPATH, ("//button[normalize-space()='Apply']")).click()
time.sleep(2)

#Jobs Description and Jobs Requirements
page = driver.page_source
soup = BeautifulSoup(page, 'lxml')
jobDesSection = soup.select("div[data-automation='jobDescription']")
resHead = soup.select("span.z1s6m00 div.z1s6m00 >span")
reqList = soup.select("span.z1s6m00 div.z1s6m00:has(ul) li") #Found from jobDesSection
companyName = soup.select("article div.z1s6m00 span.z1s6m00 a[data-automation='jobCardCompanyLink']")
position = soup.select("article div.z1s6m00 h1.z1s6m00 span.z1s6m00")
url = soup.select("div[data-automation='jobDetailsLinkNewTab'] a")
jobPosts = soup.select("article.z1s6m00")
postArticles = driver.find_elements(By.TAG_NAME, "article")

try:
    for i in range(len(position)):
        info = postArticles[i]

        try:
            info.click()

            wait = WebDriverWait(driver, 10)
            reqList = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.z1s6m00 div.z1s6m00:has(ul) li")))

            for el in reqList:
                print(el.text)
        
        except:
            print("Cannot find job description related elements")
            traceback.print_exc()
            continue
        
        jobPositionContent = position[i].text
        companiesName = companyName[i].text
        jobRequirements = reqList[i].text

        print("JobPost:", jobPositionContent)
        print("Company:", companiesName)
        print("Requirements:", jobRequirements)
        print("=" * 70)

except:
    print("Timeout occurred while waiting for reqList element. Skipping...")
    traceback.print_exc()

driver.quit()


#Eastern Area: label id="Select-0-166"
#Kwun Tong Area: label id="Select-0-130"
#Wan Chai Area: label id="Select-0-146"


