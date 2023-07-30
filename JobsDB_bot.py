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

def jobsDB_scraper(job_keyword):
    output_folder = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_folder, exist_ok=True) # Create the output folder if it doesn't exist
    #Initialize the webdriver
    driver = webdriver.Chrome()
    domain = "https://hk.jobsdb.com/"
    driver.get(domain)
    driver.fullscreen_window()
    time.sleep(0.5)

    #job keyword search
    search = driver.find_element(By.ID, "searchKeywordsField")
    search.send_keys(job_keyword)
    search.send_keys(Keys.RETURN)

    #Select the locations
    selectLocation = driver.find_element(By.CSS_SELECTOR, ".z1s6m00 [data-automation='locationChecklistField']").click()
    locations = driver.find_elements(By.CSS_SELECTOR, ("div.z1s6m00 input.z1s6m00"))
    selectedLocations = [5, 8, 18]
    for index in selectedLocations:
        if index < len(locations): #index must smaller the total number of locations
            try:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.z1s6m00 input.z1s6m00")))
                locations[index-1].click()
                time.sleep(1)
            except:
                print("Cannot found the locations")

    #Apply filters and wait for the page to load
    searchButton = driver.find_element(By.CSS_SELECTOR, ("button[data-automation='searchSubmitButton']")).click()
    time.sleep(2)
    datePostButton = driver.find_element(By.CSS_SELECTOR, ("button[data-automation='createdAtFilterButton']")).click()
    dates = driver.find_element(By.XPATH,("//span[normalize-space()='Last 7 days']")).click()
    dateApplyBtn = driver.find_element(By.CSS_SELECTOR, ("button[data-automation='refinementFormApplyButton']")).click()
    time.sleep(1)

    # Click on job posts to view details
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

    #wait for job details to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-automation='jobDetailsLinkNewTab'] a")))
    
    #Extract job data from the page
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

    #Prepare data for CSV and Excel export
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

    # Save the DataFrame to a CSV file
    csv_file = os.path.join(output_folder, f"jobsDB_{job_keyword}_post.csv")
    df.to_csv(csv_file, index=False, encoding='utf-8-sig') #Check if there is an output folder created or not

    # Save the DataFrame to an Excel file
    excel_file = os.path.join(output_folder, f"jobsDB_{job_keyword}_post.xlsx")
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
    driver.quit()
    