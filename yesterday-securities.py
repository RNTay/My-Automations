#!/usr/bin/env python3

import requests
import pdfplumber
import datetime as dt
import os


def download_file(url):
    local_filename = url.split('/')[-1]

    with requests.get(url) as r:
        with open(local_filename, 'wb') as f:
            f.write(r.content)

    return local_filename


bursa_site = 'https://www.bursamalaysia.com/misc/missftp/securities/securities_equities_'
yesterday = str(dt.datetime.now() - dt.timedelta(days=1))[:10]
securities_url = bursa_site + yesterday + '.pdf'

securities = download_file(securities_url)

with pdfplumber.open(securities) as pdf:
    page = pdf.pages[2]
    text = page.extract_text()

for row in text.splitlines():
    if row.startswith('Grand Total : Market Transaction'):
        numbers = row.split()[5:]
        print("Volume ('000 units):", numbers[0])
        print("Value (RM '000):", numbers[-1])

os.remove(securities)
