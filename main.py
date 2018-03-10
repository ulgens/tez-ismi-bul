# coding=utf-8
from __future__ import print_function

import argparse
import mechanize

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

    return map(lambda x: x[1:-1], (web_id, web_no))


if __name__ == "__main__":
    try:
        details = get_details(args.tez_no)
    except:
        print("Tez bulunamadı!")
    else:
        print("ID: %s" % details[0])
        print("NO: %s" % details[1])
        print("URL: https://tez.yok.gov.tr/UlusalTezMerkezi/tezDetay.jsp?id=%s&no=%s" % (details[0], details[1]))