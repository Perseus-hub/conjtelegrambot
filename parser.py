import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import logging

ua = UserAgent()
URL = "https://www.babla.ru/%D1%81%D0%BF%D1%80%D1%8F%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F/%D0%B8%D1%81%D0%BF%D0%B0%D0%BD%D1%81%D0%BA%D0%B8%D0%B9/"
headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/99.0.4844.47 Mobile/15E148 Safari/604.1"}
#headers = {
#    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#    'accept-encoding': 'gzip, deflate, br',
#    'accept-language': 'uk,en-US;q=0.9,en;q=0.8,ru;q=0.7',
#    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
#    'sec-ch-ua-mobile': '?0',
#    'sec-fetch-dest': 'document',
#    'sec-fetch-mode': 'navigate',
#    'sec-fetch-site': 'none',
#    'sec-fetch-user': '?1',
#    'upgrade-insecure-requests': '1',
#    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
#}

def parse(mood, tense, word):
    r = requests.get(URL + word, headers=headers)

    result_list = {}
    logging.basicConfig(level=logging.INFO)
    logging.info(f"{mood}, {tense}, {word}, {r.status_code}")
    if r.status_code == 200:
        soup = bs(r.text, "html.parser")
        all_tenses = soup.find_all('div', class_="conj-tense-wrapper")

        for item in all_tenses:
            if item.find("h3").text == mood:
                for i in item.find_all("div", class_="conj-tense-block"):
                    if i.find("h3").text == tense:
                        for j in i.find_all("div", class_="conj-item"):
                            result_list[j.find("div", class_="conj-person").text] = j.find("div",
                                                                                           class_="conj-result").text

    else:
        return None

    return result_list
