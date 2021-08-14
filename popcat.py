#!/usr/bin/env python3

from selenium import webdriver


def main():
    driver = webdriver.Safari()
    driver.get('https://popcat.click')
    cat = driver.find_element_by_xpath('//*[@id="app"]/div')
    
    for _ in range(10):
        cat.send_keys('a bunch of keys'*100)

    driver.quit()


if __name__ == '__main__':
    main()


