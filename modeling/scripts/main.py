from classes.scraper import *
from classes.Role import *
from classes.DataBase.Mongo import *
import argparse
import yaml
def main(role_terms:str,threshold:str,search:str,location:str) -> None:
    options = webdriver.ChromeOptions()
    client = MongoClient()
    scrape_table = Scraped_Data(client)
    role = Role(role_terms, thresh=threshold)
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    scrape = Scraper(
        r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', collection = scrape_table,options = options)
    scrape.search(search, location)
    time.sleep(1)
    job_dict = scrape.get_job_data(Role=role, debug=True)
    scrape.login(p = open(r".\pass.txt", "r").read())
    final_dict = scrape.get_description(job_dict,[])
    requests = [InsertOne(x) for x in final_dict]
    scrape_table.collection.bulk_write(requests)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="yaml config file for query",
                        type=str)
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.load(f)
    role_terms = config['Role']['role_terms']
    threshold = config['Role']['threshold']
    search = config['Query']['search']
    location = config['Query']['location']
    main(role_terms.split(" "),threshold,search,location)