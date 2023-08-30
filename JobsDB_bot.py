from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import csv
import pandas as pd
import xlsxwriter
import os
import datetime
import sys

class jobsdbBot:
    def __init__(self, _domain, _keywords, _locations, _dates, _jobtypes, _jobfunctions, _format):
        global domain, job_keyword, locations,dates,jobtypes,jobfunctions,format
        domain = _domain
        job_keyword = _keywords
        locations = _locations
        dates = _dates
        jobtypes = _jobtypes
        jobfunctions = _jobfunctions
        format = _format
        self.job_details_list = [] 
    
    def scrape_job_information(self):
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

        for i in range(len(jobs)):
          # Print Job Information
            # print("JobPost:", jobPosition[i].text)
            # if i < len(companyName):
            #     print("Company:", companyName[i].text)
            # if i < len(jobLocation):
            #     print("Location:", jobLocation[i].text)
            # Find and print Job Highlights
            job = jobs[i]
            jobHighlights = job.select("ul.z1s6m00 li")
            job_highlights_list = [highlight.text for highlight in jobHighlights]
            job_highlights_str = '\n'.join(job_highlights_list)
            # print("Job Highlights:")
            # for highlight in jobHighlights:
            #     print("  *", highlight.text)
            # if i < len(postedDate):
            #     print("Posted on:",postedDate[i].text)
            # if i < len(jobUrls):
            #     link = jobUrls[i].get('href')
            #     print("URL:", domain + link)
            #     print("=" * 70)
            job_details = {
                '職位名稱': jobPosition[i].text,
                '公司名稱': companyName[i].text if i < len(companyName) else '',
                '地區': jobLocation[i].text if i < len(jobLocation) else '',
                '工作詳情': job_highlights_str,
                '發佈時間': postedDate[i].text if i < len(postedDate) else '',
                '網址': domain + jobUrls[i].get('href') if i < len(jobUrls) else ''
                }
            self.job_details_list.append(job_details) 
    
    def exportFormat(self,format):
        jobs_data = self.job_details_list
        export_date = datetime.datetime.now().strftime("%d-%m") 
        if getattr(sys, 'frozen', False):
            output_folder = os.path.join(sys._MEIPASS, "工作搜尋結果")
        else:
            output_folder = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(output_folder, exist_ok=True) # Create the output folder if it doesn't exist
        columns_name=['職位名稱','公司名稱','地區','工作詳情','發佈時間','網址']        

        if format in ['csv','all']:
            csv_file = os.path.join(output_folder, f"jobsDB_{job_keyword}_{export_date}.csv")
            modified_jobs_data = []
            for job_details in jobs_data:
                title = job_details['職位名稱']
                joburls = job_details['網址']
                job_details_copy = job_details.copy()
                job_details_copy['網址'] = f'=HYPERLINK("{joburls}", "{title} 工作網址連結")'
                modified_jobs_data.append(job_details_copy)

            df = pd.DataFrame(modified_jobs_data, columns=columns_name)
            df.to_csv(csv_file, index=False, encoding='utf_8_sig')
                

        if format in ['excel', 'all']:
            df = pd.DataFrame(jobs_data)
            excel_file = os.path.join(output_folder, f"jobsDB_{job_keyword}_{export_date}.xlsx")
            df.to_excel(excel_file, index=False)

            writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            url_format = workbook.add_format({'color': 'blue', 'underline': 1})
            url_col = df.columns.get_loc('網址')

            #url can access on the text directly
            for row_num, job_details in enumerate(jobs_data):
                url = df.at[row_num, '網址']
                title = df.at[row_num, '職位名稱']
                job_post_link = f"{title} 工作網址連結"
                worksheet.write_url(row_num + 1, url_col, url, url_format, string=job_post_link)

            # Expand column width
            for col_num, column in enumerate(df.columns):
                #loop through all the columns their maximum length while astype is to make sure the len were matched for all data types
                max_len = max(df[column].astype(str).map(len).max(), len(column)) 
                worksheet.set_column(col_num, col_num, max_len + 1) #The +2 is added to provide some extra padding for better readability.

            # Add filters to rows
            last_col_letter = xlsxwriter.utility.xl_col_to_name(df.shape[1] - 1) #df.shape([0:row | 1: column] - 1: 0 base index)
            worksheet.autofilter(f"A1:{last_col_letter}{len(df) + 1}") #A1{index:5 - python start from 0} to 6

            writer.close()
        print(f"Exported job data in {format.upper()} format.")
    
    def setOption(self):
		#Handle chrome browser version missmatched issue
        global options
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches",["enable-automation"])
        prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)

    def start(self):
        global options
        options = webdriver.ChromeOptions()
        self.setOption()
        # ================ Chrome Browser Automation Start ================     
        global driver
        try:
            options.add_argument("--remote-allow-origins=*")
            driver = webdriver.Chrome(options=options)
        except:
            options = webdriver.EdgeOptions()
            self.setOption()
            options.add_argument("--guest")
            options.add_argument("--disable-features=TranslateUI")
            options.add_argument("--disable-translate")
            options.add_argument("--lang=zh-TW")
            driver = webdriver.Edge(options = options)
        driver.maximize_window()
        driver.implicitly_wait(10)

         # ================ Enter JobsDB ================
        driver.get(domain)
        sleep(1)
        search = driver.find_element(By.ID, "searchKeywordsField")
        search.send_keys(job_keyword)
        search.send_keys(Keys.RETURN)
        driver.find_element(By.CSS_SELECTOR, ".z1s6m00 [data-automation='locationChecklistField']").click()
        location_btn = driver.find_elements(By.CSS_SELECTOR, "div.z1s6m00 input.z1s6m00")

        # ================ Select job locations ================
        for selectBtns in locations:
            if selectBtns >= 1 and selectBtns <= 20: #[1-20] are the hk locations
                sleep(1)
                location_btn[selectBtns].click()
            else:
                print("Selected locations are not in the valid range.")
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ("button[data-automation='searchSubmitButton']")).click()
        sleep(1)

        # ================ Select dates option================
        driver.find_element(By.CSS_SELECTOR, ("button[data-automation='createdAtFilterButton']")).click()
        sleep(1)
        datesBtn = driver.find_elements(By.CSS_SELECTOR,("div[data-automation='SingleCheckboxGroup']"))

        for selectedBtns in dates:
            if selectedBtns <= 6:
                sleep(1)             
                datesBtn[selectedBtns - 1].click()
            else:
                print("Selected date are not in the valid range.")

        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ("button[data-automation='refinementFormApplyButton']")).click()
        sleep(1)

        # ================ Select job type option================
        driver.find_element(By.CSS_SELECTOR,'button[data-automation="jobTypeFilterButton"]').click()
        sleep(1)

        jobTypesBtns = driver.find_elements(By.CSS_SELECTOR,'div.z1s6m00 input[name="jobTypes"]')
        for selectedBtns in jobtypes:
            if selectedBtns <=7:
                sleep(1)
                jobTypesBtns[selectedBtns - 1].click()
            else:
                print("Selected jobTypes are not in the valid range.")

        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ("button[data-automation='refinementFormApplyButton']")).click()
        sleep(1)

        # ================ Select Job Functions ================
        driver.find_elements(By.CSS_SELECTOR,"button._23enrv0")[1].click()
        sleep(1)
        
        jobFunctionBtns = driver.find_elements(By.CSS_SELECTOR,'div.z1s6m00 input.z1s6m00')
        for selectBtns in jobfunctions:
            if selectBtns >=1 and selectBtns <= 26:#[1-26] all are the job functions options
                sleep(1)
                jobFunctionBtns[selectBtns].click()
            else:
                print("Selected job functions are not in the valid range.")
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ("button[data-automation='searchSubmitButton']")).click()
        sleep(1)

        # ================ Search jobs one by one================
        # clickJobPosts = driver.find_elements(By.CSS_SELECTOR,"article.z1s6m00")
        # driver.execute_script("window.scrollBy(0,40);")
        # for el in clickJobPosts:
        #     try:
        #         WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "article.z1s6m00")))
        #         WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "article.z1s6m00")))
        #         el.click()
        #         sleep(0.5)
        #     except:
        #         print("Element is not clickable or not found.")
        # driver.execute_script("window.scrollBy(0,20);")

        # ================ Scraping jobs ================
        try:
            if (driver.find_elements(By.CSS_SELECTOR,("div.z1s6m00[data-automation='pagination'] a"))):
                nextpage_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.z1s6m00[data-automation='pagination'] a")))
                self.scrape_job_information()
                driver.execute_script("arguments[0].click();", nextpage_btn)
                while True:
                    try:                                     
                        next_page_btns = driver.find_elements(By.CSS_SELECTOR, "div.z1s6m00[data-automation='pagination'] a")
                        print(f'elements was found')
                        driver.implicitly_wait(10)
                        if len(next_page_btns) ==2:
                            self.scrape_job_information()
                            driver.execute_script("arguments[0].click();", next_page_btns[1])                                                                             
                            continue
                        elif driver.find_element(By.CSS_SELECTOR,"button.z1s6m00[disabled]"):
                            driver.implicitly_wait(3)
                            endBtn = driver.find_element(By.CSS_SELECTOR,"button.z1s6m00[disabled]")
                            driver.execute_script("arguments[0].click();",endBtn)
                            print("Last page")                        
                        break                                                                                                                                                 
                    except:               
                        print("No more pages to navigate")
                        break
                self.scrape_job_information()
                print("Finished navigating and scraping")
                sleep(3)
                driver.quit()
            else:
                self.scrape_job_information()
                print('Only one page result!')
                sleep(3)
                driver.quit()
        except:
            print("No next page button")
        
        if format == 'excel' or 'Excel':
            self.exportFormat('excel')
        elif  format == 'csv' or 'Csv':
            self.exportFormat('csv')
        elif  format == 'all' or 'All':
            self.exportFormat('all')