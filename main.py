# coding=utf-8
from __future__ import print_function

import argparse
import mechanize
import requests

from bs4 import BeautifulSoup

url = "https://tez.yok.gov.tr/UlusalTezMerkezi/tarama.jsp"


parser = argparse.ArgumentParser()
parser.add_argument("tez_no")
args = parser.parse_args()

def get_details(tez_no):
    browser = mechanize.Browser()

    browser.open(url)
    browser.select_form(name="GForm")
    browser["TezNo"] = str(tez_no)

    response = browser.submit()
    content = response.read()

    details_start = content.find("tezDetay('")
    details_end = content.find(")", details_start)

    details = content[details_start + len("tezDetay("):details_end]
    web_id, web_no = details.split(",")
    web_id, web_no = map(lambda x: x[1:-1], (web_id, web_no))
    tez_url = "https://tez.yok.gov.tr/UlusalTezMerkezi/tezDetay.jsp?id=%s&no=%s" % (web_id, web_no)

    page = requests.get(tez_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tez_name = soup.find_all("tr")[1].find_all("td")[2].text.split("Yazar")[0].strip()

    return {
        "id": web_id,
        "no": web_no,
        "url": tez_url,
        "name": tez_name
    }


if __name__ == "__main__":
    try:
        details = get_details(args.tez_no)
    except:
        print("Tez bulunamadı!")
    else:
        print("ID: %s" % details["id"])
        print("NO: %s" % details["no"])
        print("URL: %s" % details["url"])
        print(u"İsim: %s" % details["name"])