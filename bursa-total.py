#!/usr/bin/env python3

import requests
import pdfplumber
import os


def download_file(url):
    local_filename = url.split('/')[-1]

    with requests.get(url) as r:
        with open(local_filename, 'wb') as f:
            f.write(r.content)

    return local_filename


def create_pdf_and_get_text(local_filename, date):
    try:
        with pdfplumber.open(local_filename) as pdf:
            page = pdf.pages[2]
            text = page.extract_text()
    except:
        print('\n' + '=' * 50 + '\n')
        print('Error: File does not exist for the date {}.'.format(date))
        print('\n' + '=' * 50 + '\n')
        os.remove(local_filename)
        exit()
    return text


def output_grand_total(data):
    for row in data.splitlines():
        if row.startswith('Grand Total : Market Transaction'):
            numbers = row.split()[5:]
            return numbers[0], numbers[-1]


def pretty_print(volume, value, date):
    print('\n' + '=' * 50 + '\n')
    print('Grand Total: Market Transaction\n')
    print('Date: ', date, '\n')
    print("Volume ('000 units):", volume)
    print("Value (RM '000):", value)
    print('\n' + '=' * 50 + '\n')


if __name__ == '__main__':
    bursa_site = 'https://www.bursamalaysia.com/misc/missftp/securities/securities_equities_'
    print()
    day = input('Date (YYYY-MM-DD): ')
    securities_url = bursa_site + day + '.pdf'

    securities = download_file(securities_url)
    page_with_grand_total_text = create_pdf_and_get_text(securities, day)
    Vol, Val = output_grand_total(page_with_grand_total_text)
    pretty_print(Vol, Val, day)

    os.remove(securities)
