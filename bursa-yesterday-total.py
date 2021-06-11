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

try:
    with pdfplumber.open(securities) as pdf:
        page = pdf.pages[2]
        text = page.extract_text()
except:
    print('\n' + '='*50 + '\n')
    print('Error: File does not exist for yesterday, {}.'.format(yesterday))
    print('\n' + '=' * 50 + '\n')
    os.remove(securities)
    exit()

for row in text.splitlines():
    if row.startswith('Grand Total : Market Transaction'):
        numbers = row.split()[5:]
        print('\n' + '='*50 + '\n')
        print('Grand Total: Market Transaction\n')
        print('Date: ', yesterday, '\n')
        print("Volume ('000 units):", numbers[0])
        print("Value (RM '000):", numbers[-1])
        print('\n' + '='*50 + '\n')

os.remove(securities)
