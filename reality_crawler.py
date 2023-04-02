from bs4 import BeautifulSoup
import requests
import configparser
from helpers.reality import Reality
from helpers.database import Database

BAZOS_REALITY_URL = 'https://reality.bazos.cz'
CUSTOM_QUERY = '/?hledat=&hlokalita=68604&humkreis=8&cenaod=&cenado=&order='
BAZOS_ADS_PER_PAGE = 20

def parse_ad_id(url):
    return url.split('/')[-2]


# fetch all reality from bazos.cz
# return list of Reality objects
def fetch_reality_bazos():
    realities = []
    html = requests.get('{}/prodam/dum{}'.format(BAZOS_REALITY_URL, CUSTOM_QUERY))
    soup = BeautifulSoup(html.text, 'html.parser')
    maincontent = soup.find_all(class_="inzeraty")
    pages = len(soup.find_all(class_="strankovani")[0].find_all('a'))
    print("pages", pages)
    if pages > 1:
        for page in range(1, pages):
            html = requests.get('{}/prodam/dum/{}{}'.format(BAZOS_REALITY_URL, page * BAZOS_ADS_PER_PAGE, CUSTOM_QUERY))
            soup = BeautifulSoup(html.text, 'html.parser')
            maincontent += soup.find_all(class_="inzeraty")

    for i in range(len(maincontent)):
        title = maincontent[i].find_all(class_="inzeratynadpis")[0].find('h2').text
        date = maincontent[i].find_all(class_="inzeratynadpis")[0].find('span').text[4:-1]
        date = date.split('.')[2] + '-' + date.split('.')[1] + '-' + date.split('.')[0]
        fetched_price = maincontent[i].find_all(class_="inzeratycena")[0].text
        if fetched_price == 'Dohodou' or fetched_price == 'V textu':
            price = -1
        else:
            price = fetched_price.replace(' Kč', '').replace(' ', '')
        location = maincontent[i].find_all(class_="inzeratylok")[0].text
        url = BAZOS_REALITY_URL + maincontent[i].find_all(class_="inzeratynadpis")[0].find('a')['href']
        image = maincontent[i].find_all(class_="inzeratynadpis")[0].find('img')['src']
        ad_id = parse_ad_id(url)
        detail_result = BeautifulSoup(requests.get(url).text, 'html.parser')
        description = detail_result.find(class_="popisdetail")
        # Detail info
        detail_info = detail_result.find(class_='listadvlevo')
        advertiser_name = detail_info.find_all('tr')[0].find_all('td')[1].text
        viewed_count = detail_info.find_all('tr')[3].find_all('td')[1].text.replace(' lidí', '')

        reality = Reality(id=ad_id, title=title, price=price, date=date, url=url, location=location, description=description, advertiser_name=advertiser_name, viewed_count=viewed_count, image=image)
        reality.set_provider(1) # 1 = bazos.cz

        realities.append(reality)

    return realities

def push_to_db(realities):
    # Config MySQL
    config = configparser.ConfigParser()
    config.read('config.conf')
    db = Database(**dict(config["database"]))

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

def deactivate_old_realities():
    config = configparser.ConfigParser()
    config.read('config.conf')
    db = Database(**dict(config["database"]))
    return db.deactivate_old_realities()

def main():
    print("Fetching reality from Bazos.cz ...")
    realities = fetch_reality_bazos()
    print("Pushing to database ...")
    result = push_to_db(realities)
    print("DB returned:", result)
    result = deactivate_old_realities()
    print("Old instances deactivated:", result)

if __name__ == '__main__':
    main()

## TODO: add sbazar.cz support
