#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

what_to_search = input('Search for: ')

driver = webdriver.Safari()
driver.get('https://www.youtube.com')

homepage_title = driver.title

search = driver.find_element_by_xpath('//*[@id="search"]')
search.send_keys(what_to_search)
search.send_keys(Keys.RETURN)

while driver.title == homepage_title:
    time.sleep(1)

videos = driver.find_elements_by_id('title-wrapper')
videos[0].click()
