#!/usr/bin/env python3
import os
import re
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
import constants
import pyautogui


class PlayStoreScraper:
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    # options.add_argument('--headless')

    def __init__(self):
        self.driver = webdriver.Chrome(options=self.options)

    def get_app_links(self, url, app_category, title, country):
        self.driver.get(url+app_category+country)
        sleep(1)
        try:
            self.driver.find_element_by_class_name('W9yFB').click()
            sleep(0.3)
        except: pass
        for scroll in range(16):
            self.driver.find_element_by_tag_name('html').send_keys(Keys.END)
            sleep(0.7)
            try:
                self.driver.find_element_by_css_selector('.RveJvd.snByac').click()
                sleep(0.3)
                self.driver.find_element_by_tag_name('html').send_keys(Keys.END)
            except: pass
        product_links = {title: [p.find_element_by_tag_name('a').get_attribute('href') for p in self.driver.find_elements_by_css_selector('.b8cIId.ReQCgd.Q9MA7b')]}
        df = pd.DataFrame.from_dict(product_links)
        print('Apps in the category:', len(df))
        # if file does not exist write header
        if not os.path.isfile(title + 'links.csv'):
            df.to_csv(title + 'links.csv', index=None)
        else:  # else if exists so append without writing the header
            df.to_csv(title + 'links.csv', mode='a', header=False, index=None)
        return len(df)

    def finish(self):
        self.driver.close()
        self.driver.quit()


def main():
    play_url = 'https://play.google.com/store/apps/category/'
    appscraper = PlayStoreScraper()
    title = 'App'
    pre_country = '?gl='
    language = '&hl=fr'
    total_apps = 304620
    for key, category in constants.categories.items():
        for country, k in constants.COUNTRIES.items():
            print('Category:', category, 'Country:', country.lower())
            total_apps += appscraper.get_app_links(url=play_url, app_category=category, title=title, country=pre_country+country.lower()+language)
            print('Apps Scraped so far:', total_apps)
    appscraper.finish()


if __name__ == '__main__':
    main()