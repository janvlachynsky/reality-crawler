from bs4 import BeautifulSoup
import requests
from reality import Reality
from database import Database

BAZOS_REALITY_URL = 'https://reality.bazos.cz'

def parse_ad_id(url):
    return url.split('/')[-2]


# fetch all reality from bazos.cz
# return list of Reality objects
def fetch_reality_bazos():
    realities = []
    html = requests.get('{}/prodam/dum/?hledat=&hlokalita=68604&humkreis=8&cenaod=&cenado=&order='.format(BAZOS_REALITY_URL))
    soup = BeautifulSoup(html.text, 'html.parser')
    maincontent = soup.find_all(class_="inzeraty")
    for i in range(len(maincontent)):
        title = maincontent[i].find_all(class_="inzeratynadpis")[0].find('h2').text
        date = maincontent[i].find_all(class_="inzeratynadpis")[0].find('span').text[4:-1]
        publish_date = date.split('.')[2] + '-' + date.split('.')[1] + '-' + date.split('.')[0]
        fetched_price = maincontent[i].find_all(class_="inzeratycena")[0].text
        if fetched_price == 'Dohodou' or fetched_price == 'V textu':
            price = -1
        else:
            price = fetched_price.replace(' Kč', '').replace(' ', '')
        location = maincontent[i].find_all(class_="inzeratylok")[0].text
        href = BAZOS_REALITY_URL + maincontent[i].find_all(class_="inzeratynadpis")[0].find('a')['href']
        ad_id = parse_ad_id(href)
        detail_result = BeautifulSoup(requests.get(href).text, 'html.parser')
        description = detail_result.find(class_="popisdetail").text
        # Detail info
        detail_info = detail_result.find(class_='listadvlevo')
        # print(detail_info.select('table tr:nth-child(1) td:nth-child(2)'))
        # print(detail_info.select('table tr:nth-child(2) td:nth-child(2)'))
        advertiser_name = detail_info.find_all('tr')[0].find_all('td')[1].text
        viewed_count = detail_info.find_all('tr')[3].find_all('td')[1].text.replace(' lidí', '')

        reality = Reality(id=ad_id, title=title, price=price, publish_date=publish_date, href=href, location=location, description=description, advertiser_name=advertiser_name, viewed_count=viewed_count)
        reality.set_provider('Bazos')

        realities.append(reality)

    return realities

def push_to_db(realities):
    db = Database()
    for count, reality in enumerate(realities):
        if count == 0:
            continue
        # print(reality)
        db.insert_one(reality)
        db.insert_to_history(reality)
    return True

def main():
    realities = fetch_reality_bazos()
    result =push_to_db(realities)
    print("pushed", push_to_db(realities))

if __name__ == '__main__':
    main()
## TODO: pagination
# number of <a> in class "strankovani" is number of pages

## TODO: add to database
## TODO: add sbazar.cz support
