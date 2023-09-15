
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
    config = configparser.ConfigParser()
    config.read('config.conf')
    db = Database(**dict(config["database"]))

    print("Fetching reality from Bazos.cz ...")
    realities = fetch_reality_bazos(**dict(config["bazos"]))
    print("Pushing to database ...")
    result = push_to_db(db, realities)
    print("DB returned:", result)
    result = db.disable_expired_realities()
    print("Old instances deactivated:", result)

if __name__ == '__main__':
    main()

## TODO: add sbazar.cz support
