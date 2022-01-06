from scraping.classes.scraper import *
from scraping.classes.Role import *
from scraping.classes.DataBase.Mongo import *
from pymongo.errors import BulkWriteError
import argparse
import yaml
from datetime import date
import pprint

'''
db.collection.find().skip(db.collection.count() - N) get last N records
^^^ integrate this as fail safe in case of needing to restart query after specific doc


==================Main executor file for scraping job==================#
==================Configs are in the ./main_exec.yaml file, to configure a scraping job clone the file and configure==================#
==================Execution from root: ./modeling/scripts/scraping/main.py ./modeling/scripts/scraping/{CLONED MAIN_EXEC.yaml file}==================#
'''
def main(role_terms: str, threshold: str, search: str, location: str,additional_terms:str,iterations) -> None:
    p = open(r"./pass.txt", "r").read()
    mdb = open(r"./mongo.txt", "r").read()
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    client = MongoClient(mdb)
    scrape_table = Mongo(client)
    role = Role(role_terms, thresh=threshold,alternate_tittles= additional_terms)
    try:
        scrape_table.db.Roles.bulk_write([InsertOne({'role':role.title,'thresh':role.thresh})])
        print(f"Role inserted:{role.title}")
    except Exception as e:
        print("Role already inserted")
    options.add_experimental_option(
        'prefs', {'intl.accept_languages': 'en,en_US'})
    scrape = Scraper("/Users/emilianopenaloza/Library/Application Support/Google/chromedriver",collection=scrape_table, options=options,loc = location,iterations=iterations)
    scrape.search(search)
    time.sleep(1)
    job_dict = scrape.get_job_data(Role=role, debug=True)

    scrape.login(p=p)
    try:
        final_dict = scrape.get_description(job_dict, [])
        res = scrape_table.collection.insert_many(final_dict,ordered= False)
        with open("./logs/Output.txt", "a") as text_file:
           text_file.write(f"Inserted {len(res.inserted_ids)} entries of {role_terms} roles in {location}, Date:{date.today()}\n" )
    except BulkWriteError as e:
        #print(e.details['writeErrors'])
        pass
    scrape.driver.close()
    print("Done Scraping")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="yaml config file for query",
                        type=str)
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    role_terms = config['Role']['title']
    additional_terms = config['Role']['additional']
    threshold = config['Role']['threshold']
    search = config['Scraping']['Query']['search']
    location = config['Scraping']['Query']['location']
    iterations = config['Scraping']['iterations']
    main(role_terms, threshold, search, location,additional_terms,iterations=iterations)
