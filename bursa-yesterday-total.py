#!/usr/bin/env python3

import requests
import pdfplumber
import os
import datetime as dt
import pdfminer.pdfparser
import pyperclip


def download_file(url: str) -> str:
    """
    Downloads the PDF file from the URL given.
    :param url: URL to the PDF file
    :return: name of the file downloaded
    """
    local_filename = url.split('/')[-1]

    with requests.get(url) as r:
        with open(local_filename, 'wb') as f:
            f.write(r.content)

    return local_filename


def pdf_error(local_filename: str, date: str):
    """
    An error with the PDF has happened.
    Output the error message, delete the PDF file, and exit the program.
    :param local_filename: name of the PDF file
    :param date: date in the name of the file
    :return:
    """
    print('\n' + '=' * 50 + '\n')
    print('Error: File does not exist for previous day, {}.'.format(date))
    print('\n' + '=' * 50 + '\n')
    os.remove(local_filename)
    exit()


def get_text_from_pdf(local_filename: str, date: str) -> str:
    """
    Extracts the text from the page of the PDF which contains the grand total numbers.
    :param local_filename: name of the PDF file
    :param date: the date in the name of the file
    :return: the extracted text from the file
    """
    try:
        with pdfplumber.open(local_filename) as pdf:
            try:
                page = pdf.pages[2]  # Grand total is on the 3rd page
                text = page.extract_text()
            except IndexError:
                # PDF file for the day does not exist, so remove it and exit().
                pdf_error(local_filename, date)
    except pdfminer.pdfparser.PDFSyntaxError:
        # PDF file for the day does not exist, so remove it and exit().
        pdf_error(local_filename, date)
    return text


def relevant_grand_total(data: str) -> tuple[str, str]:
    """
    Gets the relevant grand total numbers, i.e. the volume and value.
    :param data: the text which contains the grand total values
    :return: grand total volume and value
    """
    for row in data.splitlines():
        if row.startswith('Grand Total : Market Transaction'):
            numbers = row.split()[5:]
            return numbers[0], numbers[-1]


def pretty_print(volume: str, value: str, date: str):
    """
    Outputs the grand total numbers.
    :param volume: grand total volume
    :param value: grand total value
    :param date: date of the PDF file
    :return: None
    """
    print('\n' + '=' * 50)
    print('Grand Total: Market Transaction\n')
    print('Date: ', date, '\n')
    print("Volume ('000 units):", volume)
    print("Value (RM '000):", value + '\n')
    value_number = int(value.replace(',', '')) * 1000
    pyperclip.copy(str(value_number))
    print('(Copied grand total value, in RM, to clipboard)')
    print('=' * 50 + '\n')


if __name__ == '__main__':
    bursa_site = 'https://www.bursamalaysia.com/misc/missftp/securities/securities_equities_'
    today = dt.datetime.now()
    day_of_week = today.isoweekday()
    if day_of_week == 1:  # today is Monday; get Friday's numbers
        yesterday = str(today - dt.timedelta(days=3))[:10]
    elif day_of_week == 7:  # today is Sunday; get Friday's numbers
        yesterday = str(today - dt.timedelta(days=2))[:10]
    else:
        yesterday = str(today - dt.timedelta(days=1))[:10]
    securities_url = bursa_site + yesterday + '.pdf'

    securities = download_file(securities_url)
    page_with_grand_total_text = get_text_from_pdf(securities, yesterday)
    Vol, Val = relevant_grand_total(page_with_grand_total_text)
    pretty_print(Vol, Val, yesterday)

    os.remove(securities)


