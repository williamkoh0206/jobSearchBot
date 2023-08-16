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

class jobsdbBot:
    def __init__(self, _domain, _keywords, _locations, _dates):
        global domain, job_keyword, locations,dates,format
        domain = _domain
        job_keyword = _keywords
        locations = _locations
        dates = _dates
        # format = _format 
    
        # ================ Chrome Browser Automation Start ================
    def start(self):
        configChrome = webdriver.ChromeOptions()
        #Disable the detected automation message
        configChrome.add_experimental_option("useAutomationExtension", False)
        configChrome.add_experimental_option("excludeSwitches",["enable-automation"])
        #Disable the password massenger
        prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
        configChrome.add_experimental_option("prefs",prefs)

        global driver
        driver = webdriver.Chrome(options=configChrome)
        driver.maximize_window()
        driver.implicitly_wait(10)

         # ================ Enter JobsDB ================
        driver.get(domain)
        sleep(1)
        search = driver.find_element(By.ID, "searchKeywordsField")
        search.send_keys(job_keyword)
        search.send_keys(Keys.RETURN)
        driver.find_element(By.CSS_SELECTOR, ".z1s6m00 [data-automation='locationChecklistField']").click()
        #location_names = driver.find_elements(By.CSS_SELECTOR, "div.z1s6m00:not([data-automation]) label.z1s6m00:not([data-automation])")
        location_btn = driver.find_elements(By.CSS_SELECTOR, "div.z1s6m00 input.z1s6m00")

        
        selectedLocations = {
            'All': 1,
            'Central & Western': 2,
            'Cheung Chau':3,
            'Eastern':4,
            'Kowloon City':5,
            'Kwai Tsing':6,
            'Kwun Tong':7,
            'Lantau Island':8,
            'Northern NT':9,
            'Sai Kung':10,
            'Sham Shui Po':11,
            'Shatin':12,
            'Southern':13,
            'Tai Po':14,
            'Tsuen Wan':15,
            'Tuen Mun':16,
            'Wan Chai':17,
            'Wong Tai Sin':18,
            'Yau Tsim Mong':19,
            'Yuen Long':20
        }
        # ================ Select job locations ================
        selected_values = []
        for loc in locations:
            if loc in selectedLocations:
                selected_value = selectedLocations[loc] #match the user inputs as the key of the selectedLocations
                selected_values.append(selected_value) #update the corresponding value to the array
        print(selected_values)

        for selectBtns in selected_values:
            if selectBtns in range(1, len(location_btn) - 7): #[1-20] are the hk locations
                location_btn_element = location_btn[selectBtns]
                action = ActionChains(driver)
                action.move_to_element(location_btn_element).click().perform()
                sleep(1)
            else:
                print("Selected value is not in the valid range.")
        driver.find_element(By.CSS_SELECTOR, ("button[data-automation='searchSubmitButton']")).click()
        sleep(1)

        # ================ Select dates option================
        driver.find_element(By.CSS_SELECTOR, ("button[data-automation='createdAtFilterButton']")).click()
        sleep(1)
        datesBtn = driver.find_elements(By.CSS_SELECTOR,("div[data-automation='SingleCheckboxGroup']"))
        selectedDates = {
            'All':0,
            '1 day':1,
            '3 days':2,
            '7 days':3,
            '14 days':4
        }
        date_values = []
        for date in dates:
            if date in selectedDates:
                selected_dates_value = selectedDates[date] #match the user inputs as the key of the selectedDates and store the related value
                date_values.append(selected_dates_value) #update the corresponding value to the array
        print(date_values)

        for selectedBtns in date_values:
            if selectedBtns:
                datesBtn[selectedBtns].click()
                sleep(1)
            else:
                print("Selected value is not in the valid range.")

        driver.find_element(By.CSS_SELECTOR, ("button[data-automation='refinementFormApplyButton']")).click()
        sleep(3)

        # ================ Search jobs one by one================
        clickJobPosts = driver.find_elements(By.CSS_SELECTOR,"article.z1s6m00")
        driver.execute_script("window.scrollBy(0,25);")
        for el in clickJobPosts:
            try:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "article.z1s6m00")))
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "article.z1s6m00")))
                el.click()
                sleep(0.5)
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

              
    """
    output_folder = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_folder, exist_ok=True) # Create the output folder if it doesn't exist



    columns_name=['職位名稱','公司名稱','地區','工作詳情','發佈時間','網址']
    csv_file = os.path.join(output_folder, f"jobsDB_{job_keyword}_Post.csv")


    #open the csv file for writing
    with open(csv_file, 'w', newline='',encoding='utf_8_sig') as csvFile:
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
    excel_file = os.path.join(output_folder, f"jobsDB_{job_keyword}_Post.xlsx")
    df.to_excel(excel_file, index=False)

    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

    # Convert the DataFrame to an XlsxWriter Excel object
    df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Get the XlsxWriter workbook and worksheet objects
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']

    # Add a hyperlink format to be used in the "網址" column
    url_format = workbook.add_format({'color': 'blue', 'underline': 1})
    # Define the "網址" column range
    url_col = df.columns.get_loc('網址') # Add 1 to get the Excel column number (1-indexed)

    # Iterate through the rows and add hyperlinks to the "網址" column
    for row_num in range(len(df)):
        cell_value = df.at[row_num, '網址']
        worksheet.write_url(row_num + 1, url_col, cell_value, url_format)


    # Close the Pandas Excel writer and save the Excel file
    writer.close()
    """