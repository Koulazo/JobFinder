
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

HEADERS ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}


# def start_driver():
#     driver = webdriver.Chrome(executable_path=str(CHROMEDRIVER))
#     delete_cache(driver)
#     return driver


# def delete_cache(driver):
#     driver.execute_script("window.open('')")  # Create a separate tab than the main one
#     driver.switch_to.window(driver.window_handles[-1])  # Switch window to the second tab
#     driver.get('chrome://settings/clearBrowserData')  # Open your chrome settings.
#     perform_actions(driver, Keys.TAB * 2 + Keys.DOWN * 4 + Keys.TAB * 5 + Keys.ENTER)  # Tab to the time select and key down to say "All Time" then go to the Confirm button and press Enter
#     driver.close()  # Close that window
#     driver.switch_to.window(driver.window_handles[0])  # Switch Selenium controls to the original tab to continue normal functionality.


# def perform_actions(driver, keys):
#     actions = ActionChains(driver)
#     actions.send_keys(keys)
#     time.sleep(2)
#     print('Performing Actions!')
#     actions.perform()


# if __name__ == '__main__':
#     driver = start_driver()



def get_current_url(url, job_title, location):
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
    driver = webdriver.Chrome()


    driver.get(url)
    time.sleep(1)
    # driver.find_element_by_xpath('//*[@id="text-input-what"]').send_keys(job_title)
    driver.find_element("xpath", '//*[@id="text-input-what"]').send_keys(job_title)
    time.sleep(1)

    driver.find_element("xpath", '//*[@id="text-input-where"]').clear()


    # driver.find_element_by_xpath('//*[@id="text-input-where"]').send_keys(location)
    driver.find_element("xpath", '//*[@id="text-input-where"]').send_keys(Keys.CONTROL + "a")
    driver.find_element("xpath", '//*[@id="text-input-where"]').send_keys(Keys.BACKSPACE)
    time.sleep(1)
    driver.find_element("xpath", '//*[@id="text-input-where"]').send_keys(location)

    time.sleep(1)
    # driver.find_element_by_xpath('/html/body/div').click()
    driver.find_element("xpath", '/html/body/div').click()

    time.sleep(1)
    try:
    #     # driver.find_element_by_xpath('//*[@id="jobsearch"]/button').click()        
    #     driver.find_element("xpath",'//*[@id="jobsearch"]/button').click()
        driver.find_element("xpath",'//*[contains(concat( " ", @class, " " ), concat( " ", "yosegi-InlineWhatWhere-primaryButton", " " ))]').click()

    except:
        # driver.find_element_by_xpath('//*[@id="whatWhereFormId"]/div[3]/button').click()
        driver.find_element("xpath",'//*[@id="whatWhereFormId"]/div[3]/button').click()


    # time.sleep(3)
    # driver.find_element("xpath",'//*[@id="filter-radius"]/div[3]/button').click()
    # time.sleep(50)

    current_url = driver.current_url



    
    print("Scraping job details")
    resp = requests.get(current_url, headers=HEADERS)
    content = BeautifulSoup(resp.content, 'lxml')
   
    jobs_list = []    
    print("jobs_list:", jobs_list)
    for post in content.select('.job_seen_beacon'):
        try:
            data = {
                "job_title":post.select('.jobTitle')[0].get_text().strip(),
                "company":post.select('.companyName')[0].get_text().strip(),
                "rating":post.select('.ratingNumber')[0].get_text().strip(),
                "location":post.select('.companyLocation')[0].get_text().strip(),
                "date":post.select('.date')[0].get_text().strip(),
                "job_desc":post.select('.job-snippet')[0].get_text().strip()
                
            }
        except IndexError:
            continue          
        jobs_list.append(data)
    dataframe = pd.DataFrame(jobs_list)
    print("dataframe:", dataframe)
    return current_url, dataframe


current_url = get_current_url('https://www.indeed.com/','Bioinformatics Scientist',"San Francisco, CA")
print(current_url)

