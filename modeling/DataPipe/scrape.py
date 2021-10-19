from scraping.classes.scraper import *
from scraping.classes.Role import *
from scraping.classes.DataBase.Mongo import *
import argparse
import yaml
'''
db.collection.find().skip(db.collection.count() - N) get last N records
^^^ integrate this as fail safe in case of needing to restart query after specific doc


==================Main executor file for scraping job==================#
==================Configs are in the ./main_exec.yaml file, to configure a scraping job clone the file and configure==================#
==================Execution from root: ./modeling/scripts/scraping/main.py ./modeling/scripts/scraping/{CLONED MAIN_EXEC.yaml file}==================#
'''
def main(role_terms: str, threshold: str, search: str, location: str) -> None:
    options = webdriver.ChromeOptions()
    client = MongoClient()
    scrape_table = Mongo(client)
    role = Role(role_terms, thresh=threshold)
    options.add_experimental_option(
        'prefs', {'intl.accept_languages': 'en,en_US'})
    scrape = Scraper(
        r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', collection=scrape_table, options=options)
    scrape.search(search, location)
    time.sleep(1)
    job_dict = scrape.get_job_data(Role=role, debug=True)
    scrape.login(p=open(r".\pass.txt", "r").read())
    final_dict = scrape.get_description(job_dict, [])
    requests = [InsertOne(x) for x in final_dict]
    scrape_table.collection.bulk_write(requests)
    scrape.driver.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="yaml config file for query",
                        type=str)
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    role_terms = config['Role']['title']
    threshold = config['Role']['threshold']
    search = config['Scraping']['Query']['search']
    location = config['Scraping']['Query']['location']
    main(role_terms, threshold, search, location)
