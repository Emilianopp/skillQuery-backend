from .DataBase.Mongo import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
import numpy as np
import sys
sys.path.append("./Database")
#=====================Primary Scraping class, allows for scarping of role urls and for scraping proper description =====================#


class Scraper:
    def __init__(self, path_to_driver, options, collection):
        self.driver = webdriver.Chrome(path_to_driver, options=options)
        self.collection = collection
    #+++++++++Logs you into linkedin+++++++++#

    def login(self, p):
        url = "https://www.linkedin.com/checkpoint/rm/sign-in-another-account?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
        wait = WebDriverWait(self.driver, 1)
        self.driver.get(url)
        username = self.driver.find_element_by_id("username")
        username.send_keys("emilianopp550@gmail.com")
        password = self.driver.find_element_by_id("password")
        password.send_keys(p)
        self.driver.find_element_by_class_name(
            "login__form_action_container").click()

    #+++++++++Searcher for roles, uses linkedin url query engine to find search result+++++++++#
    def search(self, query, loc):
        time.sleep(5)
        self.driver.get(
            f"https://www.linkedin.com/jobs/search/?keywords={query}&location={loc}")

    #+++++++++Automated driver scroller+++++++++#
    def scroll_down(self, element, tag):
        time.sleep(1)
        self.driver.execute_script(
            "return arguments[0].scrollIntoView(true);", self.driver.find_element_by_xpath(element + tag))
        self.driver.execute_script("window.scrollBy(0, -100);")

    #+++++++++Scrapes urls and returns a dictionary of format+++++++++#
    # url:{'company':company,'location':location,'role':role}
    def get_job_data(self, Role, job_urls=[], debug=False):
        time.sleep(5)
        i = 1
        while True:
            try:
                element = f'//*[@id="main-content"]/section[2]/ul/li[{i}]/div/div[2]/'
                role = self.driver.find_element_by_xpath(
                    element + 'h3').text.lower()
                self.scroll_down(element, 'h4/a')
                if(Role.check_role(role) >= Role.thresh):
                    # Load more jobs button is loaded with page but not interactable
                    # Create exception handler that will click the button once it becomes interactable
                    try:
                        self.driver.find_element_by_xpath(
                            f'//*[@id="main-content"]/section[2]/button').click()
                        print("load more clicked")
                    except Exception as e:
                        pass
                    # Data Extraction
                    url = self.driver.find_element_by_xpath(
                        f'//*[@id="main-content"]/section[2]/ul/li[{i}]/div/a').get_attribute("href")
                    company = self.driver.find_element_by_xpath(
                        element + 'h4/a').text
                    location = self.driver.find_element_by_xpath(
                        element + 'div/span[1]').text
                    location_map = location.replace(" ", '').split(",")
                    if len(location_map) == 3:
                        job_urls.append(
                            {"title": Role.title,"url": url, 'location':location,'company': company,
                            'city': location_map[0],'region':location_map[1],"country": location_map[2],
                            'role': role, 'date': datetime.today().strftime('%Y-%m')})
                    else:
                        job_urls.append(
                            {"title": Role.title,"url": url, 'location':location,'company': company,
                            'role': role, 'date': datetime.today().strftime('%Y-%m')})

                i += 1
                #keep going until index is out of range at which point it will return the dictionary
            except Exception as e:
                i += 1
                element = f'//*[@id="main-content"]/section[2]/ul/li[{i-1}]/div/div[2]/'
                self.scroll_down('//*[@id="main-content"]','')
                print(e,'error at i hello = ',i)
            if(debug == True and i == 240):
                return job_urls
    #+++++++++Gathers descriptions for job postings+++++++++#
    def get_description(self, job_dict, good):
        fail = []
        # Iterate through the url list to scrape the descriptions
        for ind in job_dict:
            url = ind['url']
            if url not in good:
                try:
                    self.driver.get(url)
                    time.sleep(3)
                    self.driver.find_element_by_xpath(
                        '/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[2]/footer/button').click()
                    description = self.driver.find_element_by_xpath(
                        '//*[@id="job-details"]/span').text
                    ind.update({"description": description})
                    good.append(url)
                except Exception as e:
                    # keep going if there is a random error in which a div did not load properly but check where we failed
                    print(f"fail {e}")
                    fail.append(url)
        return job_dict
