from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import numpy as np
import pickle
import re
#=====================Class Role, allows to search and filter out roles we want from those we aren't interested in=====================#


class Role:
    def __init__(self, must, thresh):
        self.must = must
        self.score = 0
        self.thresh = thresh

    def check_role(self, role):
        regex_expressions = [fr"(?=.*\b{i.lower()}\b)" for i in self.must]
        self.score = sum([bool(re.search(m, role)) for m in regex_expressions])
        return self.score
#=====================Primary Scraping class, allows for scarping of role urls and for scraping proper description =====================#


class Scraper:
    def __init__(self, path_to_driver, options):
        self.driver = webdriver.Chrome(path_to_driver, options=options)

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
    def get_job_data(self, Role, job_urls={}, debug=False):
        i = 1
        while True:
            try:
                element = f'//*[@id="main-content"]/section[2]/ul/li[{i}]/div/div[2]/'
                role = self.driver.find_element_by_xpath(
                    element + 'h3').text.lower()
                self.scroll_down(element, 'h4/a')
                print(Role.check_role(role) >= Role.thresh)
                if(Role.check_role(role) >= Role.thresh):

                    # Load more jobs button is loaded with page but not interactable
                    # Create exception handler that will click the button once it becomes interactable
                    try:
                        self.driver.find_element_by_xpath(
                            f'//*[@id="main-content"]/section[2]/button').click()
                        print('clicked')
                    except Exception as e:
                        pass

                    # Data Extraction

                    url = self.driver.find_element_by_xpath(
                        element + 'h4/a').get_attribute("href")
                    company = self.driver.find_element_by_xpath(
                        element + 'h4/a').text
                    location = self.driver.find_element_by_xpath(
                        element + 'div/span[1]').text
                    job_urls.update(
                        {url: {'company': company, 'location': location, 'role': role}})
                i += 1
                if(debug == True and i == 50):
                    return job_urls
            # keep going until index is out of range at which point it will return the dictionary
            except Exception as e:
                print(str(e))
                return job_urls

    #+++++++++Automated Scroller+++++++++#
    def get_description(self, job_dict, good):
        fail = []
        # Iterate through the url list to scrape the descriptions
        for url in list(job_dict.keys()):
            if url not in good:
                try:
                    self.driver.get(url)
                    time.sleep(3)
                    if self.driver.current_url != url:
                        print(f'failed at {url}')
                        # remove borken urls
                        job_dict.pop(url)
                        # scrape
                        self.driver.find_element_by_xpath(
                            '//*[@aria-label="Click to see more description"]').click()
                        description = self.driver.find_element_by_xpath(
                            '/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[2]/article/div').text
                        job_dict.get(url).update({"description": description})
                        good.append(url)
                    return job_dict
                except:
                    # keep going if there is a random error in which a div did not load properly but check where we failed
                    print(f"fail {job_dict.get(url)}")
                    fail.append(url)


options = webdriver.ChromeOptions()
role = Role(['Software', 'Engineer'], thresh=2)
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
scrape = Scraper(
    r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', options)
scrape.search("softwareengineer", "canada")
print(scrape.get_job_data(Role=role, debug=True))
