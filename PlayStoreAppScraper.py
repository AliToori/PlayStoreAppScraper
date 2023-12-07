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
        actions = ActionChains(self.driver)
        self.driver.get(url+app_category+country)
        sleep(1)
        try:
            self.driver.find_element_by_class_name('W9yFB').click()
            sleep(0.3)
        except:
            pass
        for scroll in range(12):
            self.driver.find_element_by_tag_name('html').send_keys(Keys.END)
            sleep(0.5)
            try:
                self.driver.find_element_by_css_selector('.RveJvd.snByac').click()
                sleep(0.3)
                self.driver.find_element_by_tag_name('html').send_keys(Keys.END)
            except: pass

        # Select(self.driver.find_element_by_name('field-binding_browse-bin')).select_by_visible_text(app_category)
        # Select(self.driver.find_element_by_name('node')).select_by_index(subject)
        product_links = {title: [p.find_element_by_tag_name('a').get_attribute('href') for p in self.driver.find_elements_by_css_selector('.b8cIId.ReQCgd.Q9MA7b')]}
        df = pd.DataFrame.from_dict(product_links)
        print('Apps:', len(df))
        # if file does not exist write header
        if not os.path.isfile(title + 'links.csv'):
            df.to_csv(title + 'links.csv', index=None)
        else:  # else if exists so append without writing the header
            df.to_csv(title + 'links.csv', mode='a', header=False, index=None)
        #     # button_next = self.driver.find_element_by_link_text('Next')
        #     button_next = self.driver.find_element_by_class_name('a-last')
        #     actions.move_to_element(button_next)
        #     button_next.click()
        #     sleep(1)
        return len(df)

    def get_dev_emails(self, url, title):
        df = pd.read_csv(title + "links.csv", index_col=None)
        for index, row in df.iterrows():
            developer = {}
            french_developer = {}
            print('Product number:', index)
            self.driver.get(url=row[title])
            sleep(1)
            try:
                developer_element = self.driver.find_elements_by_class_name('htlgb')[22]
            except:
                try:
                    developer_element = self.driver.find_elements_by_class_name('htlgb')[21]
                except:
                    try:
                        developer_element = self.driver.find_elements_by_class_name('htlgb')[20]
                    except:
                        try:
                            developer_element = self.driver.find_elements_by_class_name('htlgb')[19]
                        except: continue
            developer_text = developer_element.text
            developer_email = self.driver.find_element_by_css_selector('.hrTbp.euBY6b').text
            print('Developer text:', developer_text)
            # print('Developer email:', developer_email)
            if 'France' in developer_text or 'FRANCE' in developer_text or 'Paris' in developer_text or 'PARIS' in developer_text or 'FR' in developer_text or 'Fr' in developer_text or developer_text == '':
                print('$$$$$$$$$$$$$$$     French Developer Found     $$$$$$$$$$$$$$$')
                developer["Developer Email"] = [developer_email]
                print(developer)
                french_developer['French Url'] = [row[title]]
                df = pd.DataFrame.from_dict(developer)
                # if file does not exist write header
                if not os.path.isfile(title + 'Developer.csv'):
                    df.to_csv(title + 'Developer.csv', index=None)
                else:  # else if exists so append without writing the header
                    df.to_csv(title + 'Developer.csv', mode='a', header=False, index=None)
                df_french_dev = pd.DataFrame.from_dict(french_developer)
                # if file does not exist write header
                if not os.path.isfile('Applinks_French.csv'):
                    df_french_dev.to_csv('Applinks_French.csv', index=None)
                else:  # else if exists so append without writing the header
                    df_french_dev.to_csv('Applinks_French.csv', mode='a', header=False, index=None)
            else:
                continue

    def finish(self):
        self.driver.close()
        self.driver.quit()


def main():
    play_url = 'https://play.google.com/store/apps/category/'
    appscraper = PlayStoreScraper()
    title = 'App'
    scraped_done = 0
    pre_country = '?gl='
    total_apps = 0
    # for url in urls:
    #     appscraper.get_app_links(url=url, app_category='category', title=title)
    # for key, category in constants.categories.items():
    #     for country in countries:
    #         print('Category:', category, 'Country:', country)
    #         total_apps += appscraper.get_app_links(url=play_url, app_category=category, title=title, country=pre_country+country)
    #         print('Apps Scraped so far:', total_apps)
    appscraper.get_dev_emails(url=play_url, title=title)
    appscraper.finish()


if __name__ == '__main__':
    main()