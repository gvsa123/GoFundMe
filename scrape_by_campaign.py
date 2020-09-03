#! /usr/bin/env python3

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import datetime as dt


import pandas as pd
import numpy as np
import time
import os
import sys
import csv
import re

driver = webdriver.Chrome('./WebDriver/chromedriver')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
wait = WebDriverWait(driver, 5)

TITLE = []
PROGRESS = []
STORY = []
STATS = []
M_CAMPAIGN = []
CREATED_DATE = []
URL_INDEX = []
RAISED = []
TARGET = []
DONORS = []
SHARES = []
FOLLOWERS = []

# url_list = open('urllist_master.txt', 'r')
# url_list = url_list.readlines()

url_list = ['https://ca.gofundme.com/f/actions-against-abuse']

def scraped_log(url):
    """Log url that have been scraped"""
    url_text = url
    with open('scraped_log.txt', 'a') as file:
        file.write(url_text)
        file.write('\n')
    print(f"Log: {url}")

def clean_progress(progress):
    """Parse raised and target from progress"""
    str_list = progress.split(' ')
    raised = str_list[0]
    target = str_list[-2]

    RAISED.append(raised)
    TARGET.append(target)

def stats_split(stats):
    """Parse stats into donors, shares, followers"""
    p = re.compile('[\d]')
    sep = ""

    try:
        stats_lst = stats.split()
        stats_str = stats_lst[4:7]

        donors_lst = p.findall(stats_str[0])
        shares_lst = p.findall(stats_str[1])
        followers_lst = p.findall(stats_str[-1])
    except IndexError as IndErr:
        print(IndErr)
    finally:
        donors = sep.join(donors_lst)
        shares = sep.join(shares_lst)
        followers = sep.join(followers_lst)

        DONORS.append(donors)
        SHARES.append(shares)
        FOLLOWERS.append(followers)


def campaign_info():
    """Get campaign_info from data_campaign_links.txt file"""
    x = 0
    for i in url_list: #6000:
        try:
            driver.get(i)
            time.sleep(1)
            driver.get(i)
            time.sleep(1)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Navigate to donate button
            donate_button_list = soup.find_all('a', class_='m-donate-button')
            test = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Donate')))
            text = driver.find_element_by_link_text('Donate')
            ActionChains(driver).move_to_element(text).perform()
            time.sleep(2)

            # Get info
            title = soup.h1.get_text()
            progress = soup.find('h2', class_='m-progress-meter-heading').get_text()
            print(progress)
            story = soup.find('div', class_='o-campaign-story')#.get_text()
            stats = soup.find('div', class_='o-campaign-sidebar-wrapper').get_text()
            m_campaign = soup.find('a', class_='m-campaign-byline-type')
            m_campaign = m_campaign['href'].split('/')

            # Process created_date into datetime object
            created = soup.find(class_='m-campaign-byline-created')
            created_date = created.get_text().split(" ")
            created_date = ("-".join(created_date[1:]))
            created_date = datetime.strptime(created_date, '%d-%B-%Y')

            # Process url as url_index
            url_short_list = i.split('/')# Process url_index
            url_short = url_short_list[-1]

            # Add to list
            URL_INDEX.append(url_short)
            TITLE.append(title)
            PROGRESS.append(progress)
            STORY.append(story)
            #STATS.append(stats)
            M_CAMPAIGN.append(m_campaign[-1])
            CREATED_DATE.append(created_date)

            clean_progress(progress) # Parse text output
            stats_split(stats)
            scraped_log(i)

            print(url_short)
            print(title)
            print(progress)
            print(story)
            # print(story.encode('ascii', 'ignore'))
            print(stats)
            print(m_campaign[-1])
            print(created_date)

        except ValueError as ValErr:
            print(ValErr)
            created_date = created.get_text()#("-".join(created_date))

        except (TimeoutException, KeyboardInterrupt, UnboundLocalError) as err:
            print(err)
            continue

        finally:
            create_df(URL_INDEX, TITLE, RAISED, TARGET, STORY, M_CAMPAIGN, CREATED_DATE,
                    DONORS, SHARES, FOLLOWERS)
            x += 1
            print(f"{x} items | url_list: {len(url_list)}")

def create_df(URL_INDEX, TITLE, RAISED, TARGET, STORY, M_CAMPAIGN, CREATED_DATE, DONORS, SHARES, FOLLOWERS):
    """Create dataframe from campaign_info output"""

    df_main = pd.DataFrame(columns=['url_index', 'title', 'raised', 'target', 'story',
                                    'm_campaign', 'created_date', 'donors', 'shares', 'followers'])
    df = pd.DataFrame()

    print("Creating dataframe...")
    df_main['url_index'] = pd.Series(URL_INDEX)
    df_main['title'] = pd.Series(TITLE)
    df_main['raised'] = pd.Series(RAISED)
    df_main['target'] = pd.Series(TARGET)
    df_main['story'] = pd.Series(STORY)
    df_main['m_campaign'] = pd.Series(M_CAMPAIGN)
    df_main['created_date'] = pd.Series(CREATED_DATE)
    df_main['donors'] = pd.Series(DONORS)
    df_main['shares'] = pd.Series(SHARES)
    df_main['followers'] = pd.Series(FOLLOWERS)
    df_main['scrape_date'] = pd.to_datetime(datetime.now(), format='%d-%B-%Y')
    print("############\n")

    i = 0
    while os.path.exists("cart%s.csv" % i): # Increment filename
        i += 1

    print("New file created: gofund_data%s.csv" % i)
    FILENAME = ("gofund_data%s.csv" % i)

    df_main.to_csv(FILENAME, encoding="utf-8", index=True) #_test_7
    print("Data created...")

campaign_info()
