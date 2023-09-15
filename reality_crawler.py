
import configparser
import os
import logging
from helpers.reality import Reality
from helpers.database import Database
from helpers.fetcher import fetch_reality_bazos

BAZOS_REALITY_URL = 'https://reality.bazos.cz'
CUSTOM_QUERY = '/?hledat=&hlokalita=68604&humkreis=8&cenaod=&cenado=&order='
BAZOS_ADS_PER_PAGE = 20

def push_to_db(db, realities):
    for count, reality in enumerate(realities):
        if count == 0:
            continue
        res = db.insert_one(reality)
        if (res == False):
            raise Exception("Error while inserting reality to DB")
        res = db.insert_to_history(reality)
        if (res == False):
            raise Exception("Error while inserting reality to history")
    return True

def main():
    project_dir = os.path.dirname(__file__)
    logging.basicConfig(filename=os.path.join(project_dir,'logs','reality_crawler.log'), level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

    config = configparser.ConfigParser()
    config.read(os.path.join(project_dir,'config.conf'))
    db = Database(**dict(config["database"]))
    # start time measurement
    import time
    start = time.time()

    logging.info("Fetching reality from Bazos.cz ...")
    realities = fetch_reality_bazos(**dict(config["bazos"]))
    end = time.time()
    logging.info("Fetched {} realities in {} seconds".format(len(realities), end - start))
    # TODO: fetch from sbazar.cz
    logging.info("Pushing to database ...")
    # TODO: dont push to db if pushed last 12 hours
    result = push_to_db(db, realities)
    logging.info(f"DB returned: {result}")
    result = db.update_expired_realities()
    logging.info(f"Old instances deactivated: {result}")

if __name__ == '__main__':
    main()

## TODO: add sbazar.cz support
