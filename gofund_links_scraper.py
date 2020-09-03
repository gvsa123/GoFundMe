#! /usr/bin/env python3

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

import pandas as pd
import numpy as np
import time
import os
import sys
import csv

url = 'https://ca.gofundme.com/discover'
driver = webdriver.Chrome('./WebDriver/chromedriver')
webpage = driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
wait = WebDriverWait(driver, 5)

CATEGORIES = []
CAMPAIGNS = []
M_CAMPAIGN = []
TITLE = []
PROGRESS = []
STORY = []
STATS = []
CREATED_DATE = []

def show_all_categories():
	"""Make sure all categories are loaded on page"""
	try:
		test = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Show all categories')))
		show_all = driver.find_element_by_link_text('Show all categories')
		ActionChains(driver).move_to_element(show_all).click(show_all).perform()
		print("All categories loaded.")
	except TimeoutException:
		pass

show_all_categories()

def get_category_links():
	"""Create function to get all CATEGORY links from url"""

	for a in soup.find_all('div', class_='no-focus'):
		for i in a.find_all('div', class_='section-categories'):
			for link in i.find_all('a', class_='section-categories-icon'):
				CATEGORIES.append(url[:-9]+ link['href'])
	for i in CATEGORIES:
		print(i)
	print(f"\nTotal {len(CATEGORIES)} CATEGORIES\n")

get_category_links()

def show_more_campaigns():
	"""Show more items button"""
	test = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Show More')))
	show_all =driver.find_element_by_link_text('Show More')
	ActionChains(driver).move_to_element(show_all).click(show_all).perform()

def get_campaign_links(i):
	"""Get individual get_campaign_links"""

	print(f"\n{i[33:].upper()} links:")
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser') # Create new bs4 object

	for t in soup.find_all('div', class_="fund-item"): #react-campaign-tile
		for a in t.find_all('a', href=True):
			CAMPAIGNS.append(a['href']) # get all links to campaign
			print(a['href'])

	print(f"{len(CAMPAIGNS)} loaded")

def save_links():
	"""Save links to text."""

	with open("test_data.txt", "a") as file:#_campaign
		for i in CAMPAIGNS:
			file.write(i)
			file.write("\n")

	print(f"\nSaved {len(CAMPAIGNS)} links\n")


def load_campaign():
	"""Load all campaigns under each CATEGORY"""

	for i in CATEGORIES: #CATEGORIES IS A LIST OF URLS
		x = 0
		driver.get(i)
		test = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Show More')))
		print(f"\nLoading: {i}:")
		try:
			while x < 20:
				show_more_campaigns() # load all of the campaigns in the category
				x += 1
				print(x)
		except TimeoutException:
			continue
		finally:
			get_campaign_links(i)
			save_links()

def scraped_log(url):
	"""Log url that have been scraped"""
	url_text = url
	with open('test_scraped_log.txt', 'a') as file:
		file.write(url_text)
		file.write('\n')

def campaign_info():
	"""Get campaign_info after loading campaign page"""

	print(f"\nLoading campaigns...\n")
	with open('test_info.txt', 'a') as file:
		for i in CAMPAIGNS:
			try:
				driver.get(i)
				time.sleep(1)
				driver.get(i)
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
				story = soup.find('div', class_='o-campaign-story').get_text()
				stats = soup.find('div', class_='o-campaign-sidebar-wrapper').get_text()
				m_campaign = soup.find('a', class_='m-campaign-byline-type')
				m_campaign = m_campaign['href'].split('/')
				created = soup.find(class_='m-campaign-byline-created')
				created_date = created.get_text().split(" ")
				created_date = (" ".join(created_date[1:]))
				time.sleep(1)

				TITLE.append(title)
				PROGRESS.append(progress)
				STORY.append(story)
				STATS.append(stats)
				M_CAMPAIGN.append(m_campaign)
				CREATED_DATE.append(created_date)

				file.write(title)
				file.write('\n')
				file.write(progress)
				file.write('\n')
				file.write(story)
				file.write('\n')
				file.write(stats)
				file.write('\n')
				file.write(', '.join(m_campaign))
				file.write('\n')
				file.write(created_date)
				file.write('\n')

				print(title)
				print(progress)
				print(story)
				print(stats)
				print(m_campaign[-1:])
				print(created_date)

				scraped_log(i)

			except (TimeoutException, KeyboardInterrupt) as err:
				with open('error_log.txt', 'w+') as file:
					file.write(err)
				print(err)
				continue

			else:
				continue

			finally:
				print("...\n")


def create_df(TITLE, PROGRESS, STORY, STATS, M_CAMPAIGN, CREATED_DATE):
	"""Create dataframe from campaign_info output"""

	df_main = pd.DataFrame(columns=['title', 'progress', 'story', 'stats', 'm_campaign', 'created_date'])
	df = pd.DataFrame()

	# for i in CAMPAIGNS:
	print("\n############")
	print("Creating dataframe...")
	df_main['title'] = pd.Series(TITLE).transpose()
	df_main['progress'] = pd.Series(PROGRESS).transpose()
	df_main['story'] = pd.Series(STORY).transpose()
	df_main['stats'] = pd.Series(STATS).transpose()
	df_main['m_campaign'] = pd.Series(M_CAMPAIGN).transpose()
	df_main['created_date'] = pd.Series(CREATED_DATE).transpose()
	print("############\n")

	df_main.to_csv("test_data_gofund.csv", encoding="utf-8", index=True) #_test_7
	print("Data created...")

load_campaign()
#campaign_info()
#create_df(TITLE, PROGRESS, STORY, STATS, M_CAMPAIGN, CREATED_DATE)

driver.close()
