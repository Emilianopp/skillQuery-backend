from classes.scraper import *
from classes.Role import *

options = webdriver.ChromeOptions()
role = Role(['Software', 'Engineer'], thresh=2)
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
scrape = Scraper(
    r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', options)
scrape.search("softwareengineer", "canada")
print(scrape.get_job_data(Role=role, debug=True))
