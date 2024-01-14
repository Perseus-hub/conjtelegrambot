import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

ua = UserAgent()
URL = "https://www.babla.ru/%D1%81%D0%BF%D1%80%D1%8F%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F/%D0%B8%D1%81%D0%BF%D0%B0%D0%BD%D1%81%D0%BA%D0%B8%D0%B9/"
headers = {
    "User-Agent": ua.chrome}


def parse(mood, tense, word):
    r = requests.get(URL + word, headers=headers)

    result_list = {}

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
