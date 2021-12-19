import requests
import pandas as pd
import csv

import json
import numpy as np
from pandas.io.json import json_normalize
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys 

from tqdm import tqdm
chrome_path=ChromeDriverManager().install()


chrome_options = Options()
chrome_options.add_argument("headless")
driver = webdriver.Chrome(chrome_path,options=chrome_options,keep_alive=False)


def main():

	s1 = (all_id())
	s2 = (cty_id())
	s3 = (carnet()[0])
	s4 = (carnet()[1])
	s5 = (carnet()[2])
	s6 = (vma_id())
	s7 = (aav_id())
	s8 = (gma_id())
	s9 = (cma_id())
	s10 = (f3a_id())
	l = [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10]
	start_list =pd.DataFrame(l)
	start_list.to_csv(r'start.csv',index=False)
	


def all_id():
	url ='https://www.allianceauctions.com.au/as_stock.aspx?criteria=&title=CAR%20SEARCH%20RESULTS'
	driver.get(url)
	ids = driver.find_elements_by_xpath("//*[@id='container']/div[5]/table/tbody/tr/td/table/tbody//tr/td[2]/a")
	alliance=[item.get_attribute('href').split('=')[2] for item in ids]
	stock_id = sorted(alliance,reverse = True)
	print('Alliance Latest number: ',stock_id[0])
	return stock_id[0]


def cty_id():
	url ='https://www.citymotorauction.com.au/as_stock.aspx?sitekey=CTY&make=All%20Makes&model=All%20Models&keyword=&fromyear=From%20Any&toyear=To%20Any&body=All%20Body%20Types'
	driver.get(url)
	ids = driver.find_elements_by_xpath("//*[@id='grdVehicles']/tbody//tr/td[2]")
	cty=[item.text for item in ids]
	cty_id = sorted(cty,reverse = True)[1]
	print('CityMotor Latest number: ',cty_id)
	return cty_id


def carnet():
	site_id =[]
	stock_id =[]

	url = 'https://www.carnetauctions.com.au/search_results.aspx?sitekey=All+Locations&make=All+Makes&model=All+Models'
	driver.get(url)
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//option[@value='Order By mvmta desc']")))
	element.click()
	sleep(3)
	ids = driver.find_elements_by_xpath("//*[@id='results-holder']//h4/a")
	for i in ids:	
		site_id.append(i.get_attribute('href').split('=')[1])
		stock_id.append(i.get_attribute('href').split('=')[2].split('&')[0])
	f = pd.DataFrame(list(zip(site_id,stock_id)),columns = ['site_id','stock_id'])
	css = f.loc[f['site_id'] == 'CSS&MTA']
	css_id = css['stock_id'].iloc[0]
	tma = f.loc[f['site_id'] == 'TMA&MTA']
	tma_id = tma['stock_id'].iloc[0]
	caa = f.loc[f['site_id'] == 'CAA&MTA']
	caa_id = caa['stock_id'].iloc[0]
	print('Carnet Auction Latest number: ',caa_id)
	print('Carnet Western Sydney Latest number: ',tma_id)
	print('Carnet Auction SmithField Latest number: ',css_id)
	return caa_id,tma_id,css_id


def vma_id():

	url = 'https://www.valleymotorauctions.com.au/search_results.aspx?sitekey=VMA&make=All+Makes&model=All+Models&keyword=&fromyear=From+Any&toyear=To+Any&body=All+Body+Types'
	driver.get(url)
	driver.find_element_by_xpath("//*[@id='form1']/section/div/div/div/div[1]/div/div[1]/div[2]/div/button").click()
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='form1']/section/div/div/div/div[1]/div/div[1]/div[2]/div/div/ul/li[3]/a/span[1]")))
	element.click()
	sleep(3)
	stock_id = driver.find_element_by_xpath("//*[@id='box-grid']/div/div[1]/div[2]/div[1]/a").get_attribute('href').split('=')[2].split('&')[0]
	print('Valleymotor Latest number: ',stock_id)
	return stock_id


def aav_id():
	url = 'https://auto-auctions.com.au/search_results.aspx?sitekey=AAV&make=All+Makes&model=All+Models&keyword=&fromyear=From+Any&toyear=To+Any&body=All+Body+Types'
	driver.get(url)
	driver.find_element_by_xpath("//*[@id='form1']/section/div/div/div/div[1]/div/div[1]/div[2]/div/button").click()
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='form1']/section/div/div/div/div[1]/div/div[1]/div[2]/div/div/ul/li[4]/a/span[1]")))
	element.click()
	sleep(3)
	stock_id = driver.find_element_by_xpath("//*[@id='gvVehicles']/tbody/tr[1]/td[1]/a").get_attribute('href').split('=')[2].split('&')[0]
	print('AutoAuction Latest number: ',stock_id)
	return stock_id


def gma_id():
	url = 'https://www.uaansw.com.au/search_results.aspx?sitekey=GMA&make=All+Makes&model=All+Models'
	driver.get(url)
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//option[@value='Order By mvmta desc']")))
	element.click()
	sleep(3)
	stock_id = driver.find_element_by_xpath("//*[@id='results-holder']/div[1]/div[1]/a").get_attribute('href').split('=')[2].split('&')[0]
	print('UnitedAuction Latest number: ',stock_id)
	return stock_id

def cma_id():
	url = 'https://www.centralautoauctions.com.au/search_results.aspx?sitekey=CMA&make=All+Makes&model=All+Models'
	driver.get(url)
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//option[@value='Order By mvmta desc']")))
	element.click()
	sleep(3)
	stock_id = driver.find_element_by_xpath("//*[@id='results-holder']/div[1]/div[1]/a").get_attribute('href').split('=')[2].split('&')[0]
	print('CentralAuto Latest number: ',stock_id)
	return stock_id

def f3a_id():
	url = 'https://www.f3motorauctions.com.au/search_results.aspx?sitekey=F3A&make=All+Makes&model=All+Models'
	driver.get(url)
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//option[@value='Order By mvmta desc']")))
	element.click()
	sleep(3)
	stock_id = driver.find_element_by_xpath("//*[@id='results-holder']/div[1]/div[1]/a").get_attribute('href').split('=')[2].split('&')[0]
	print('F3motor Latest number: ',stock_id)
	return stock_id


main()