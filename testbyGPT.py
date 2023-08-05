import os
import csv
import pandas as pd
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class JobsDBScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.domain = "https://hk.jobsdb.com/"
        self.output_folder = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(self.output_folder, exist_ok=True)  # Create the output folder if it doesn't exist

    def scrape_jobs(self, job_keyword):
        self._search_jobs(job_keyword)
        self._apply_filters()
        self._click_on_job_posts()
        self._wait_for_job_details()
        job_data = self._extract_job_data()
        df = pd.DataFrame(job_data)
        self._save_to_csv(df, job_keyword)
        self._save_to_excel(df, job_keyword)
        self.driver.quit()

    def _search_jobs(self, job_keyword):
        search = self.driver.find_element(By.ID, "searchKeywordsField")
        search.send_keys(job_keyword)
        search.send_keys(Keys.RETURN)
        selectLocation = self.driver.find_element(By.CSS_SELECTOR, ".z1s6m00 [data-automation='locationChecklistField']").click()
        locations = self.driver.find_elements(By.CSS_SELECTOR, ("div.z1s6m00 input.z1s6m00"))
        selectedLocations = [5, 8, 18]
        for index in selectedLocations:
            if index < len(locations): #index must smaller the total number of locations
                try:
                    WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.z1s6m00 input.z1s6m00")))
                    locations[index-1].click()
                    time.sleep(1)
                except:
                    print("Cannot found the locations")

    def _apply_filters(self):
        searchButton = self.driver.find_element(By.CSS_SELECTOR, ("button[data-automation='searchSubmitButton']")).click()
        time.sleep(2)
        datePostButton = self.driver.find_element(By.CSS_SELECTOR, ("button[data-automation='createdAtFilterButton']")).click()
        dates = self.driver.find_element(By.XPATH,("//span[normalize-space()='Last 7 days']")).click()
        dateApplyBtn = self.driver.find_element(By.CSS_SELECTOR, ("button[data-automation='refinementFormApplyButton']")).click()
        time.sleep(1)    

    def _click_on_job_posts(self):
        clickJobPosts = self.driver.find_elements(By.CSS_SELECTOR,"article.z1s6m00")
        self.driver.execute_script("window.scrollBy(0,25);")
        for el in clickJobPosts:
            try:
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "article.z1s6m00")))
                WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "article.z1s6m00")))
                el.click()
                time.sleep(0.5)
            except:
                print("Element is not clickable or not found.")

    def _wait_for_job_details(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-automation='jobDetailsLinkNewTab'] a")))

    def _extract_job_data(self):
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        jobs = soup.select("article.z1s6m00")

        companyName = soup.select("article div.z1s6m00 span.z1s6m00 a[data-automation='jobCardCompanyLink']")
        jobPosition = soup.select("article div.z1s6m00 h1.z1s6m00 span.z1s6m00")
        jobUrls = soup.select("article.z1s6m00 h1.z1s6m00 a")
        jobHighlights = soup.select("ul.z1s6m00 li")
        jobLocation = soup.select("span.z1s6m00 a[data-automation='jobCardLocationLink']")
        postedDate = soup.select("div.z1s6m00 time span")
        print("Numbers of jobs: " + str(len(jobs)))
        
        # Prepare job data as a list of dictionaries
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
                '網址': self.domain + link if data < len(jobUrls) else ''
            }
            job_data.append(jobs_dict)
        
        return job_data

    def _save_to_csv(self, df, job_keyword):
        csv_file = os.path.join(self.output_folder, f"jobsDB_{job_keyword}_post.csv")
        df.to_csv(csv_file, index=False, encoding='utf-8-sig') #Check if there is an output folder created or not

    def _save_to_excel(self, df, job_keyword):
        excel_file = os.path.join(self.output_folder, f"jobsDB_{job_keyword}_post.xlsx")
        df.to_excel(excel_file, index=False)
        # Create a Pandas Excel writer using XlsxWriter as the engine
        writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
         # Convert the DataFrame to an XlsxWriter Excel object
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        # Get the XlsxWriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        # Add a hyperlink format to be used in the "網址" column
        url_format = workbook.add_format({'color': 'blue', 'underline': 1})
        # Define the "網址" column range
        url_col = df.columns.get_loc('網址')  # Add 1 to get the Excel column number (1-indexed)

        # Iterate through the rows and add hyperlinks to the "網址" column
        for row_num in range(len(df)):
            cell_value = df.at[row_num, '網址']
            worksheet.write_url(row_num + 1, url_col, cell_value, url_format)
        # Close the Pandas Excel writer and save the Excel file
        writer.close()
