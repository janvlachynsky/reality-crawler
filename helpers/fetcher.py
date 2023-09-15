from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests

from helpers.reality import Reality
from helpers.utils import Utils

def fetch_reality_bazos(main_url, custom_query, ads_per_page):
    """
    Fetches all reality from bazos.cz
    return list of Reality objects
    """
    realities = []

    html = requests.get('{}/prodam/dum{}'.format(main_url, custom_query))
    soup = BeautifulSoup(html.text, 'html.parser')
    main_content = soup.find_all(class_="inzeraty")
    pages = len(soup.find_all(class_="strankovani")[0].find_all('a'))
    print("Total pages: ", pages)
    if pages > 1:
        for page in range(1, pages):
            html = requests.get('{}/prodam/dum/{}{}'.format(main_url, page * ads_per_page, custom_query))
            soup = BeautifulSoup(html.text, 'html.parser')
            main_content += soup.find_all(class_="inzeraty")
    # Process all fetched ads in threads
    pool = ThreadPoolExecutor(max_workers=10)
    futures = [pool.submit(_process_ad, ad, main_url) for ad in main_content]

    for future in futures:
        reality = future.result()
        realities.append(reality)

    return realities


def _process_ad(ad, main_url):
    title = ad.find_all(class_="inzeratynadpis")[0].find('h2').text
    date = ad.find_all(class_="inzeratynadpis")[0].find('span').text[4:-1]
    date = date.split('.')[2] + '-' + date.split('.')[1] + '-' + date.split('.')[0]
    fetched_price = ad.find_all(class_="inzeratycena")[0].text
    if fetched_price == 'Dohodou' or fetched_price == 'V textu':
        price = -1
    else:
        price = fetched_price.replace(' Kč', '').replace(' ', '')
    location = ad.find_all(class_="inzeratylok")[0].text
    url = main_url + ad.find_all(class_="inzeratynadpis")[0].find('a')['href']
    image = ad.find_all(class_="inzeratynadpis")[0].find('img')['src']
    ad_id = Utils.parse_ad_id(url)
    detail_result = BeautifulSoup(requests.get(url).text, 'html.parser')
    description = detail_result.find(class_="popisdetail").text
    # Detail info
    detail_info = detail_result.find(class_='listadvlevo')
    advertiser_name = detail_info.find_all('tr')[0].find_all('td')[1].text
    viewed_count = detail_info.find_all('tr')[3].find_all('td')[1].text.replace(' lidí', '')

    reality = Reality(id=ad_id, title=title, price=price, date=date, url=url, location=location, description=description, advertiser_name=advertiser_name, viewed_count=viewed_count, image=image)
    reality.set_provider(1) # 1 = bazos.cz

    return reality
