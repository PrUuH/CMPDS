import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import csv
import requests
import numpy as np


url = "https://garem54.ru/programmy/?ysclid=m7kd7pfvm4290863239"

driver = webdriver.Firefox()

driver.get(url)
time.sleep(2)
button_ager = driver.find_element(By.CSS_SELECTOR, '#yesclick > span:nth-child(1) > span:nth-child(1)')
time.sleep(2)
button_ager.click()

button_crazy = driver.find_element(By.CSS_SELECTOR, '#menu-item-174 > a:nth-child(1)')
time.sleep(2)
button_crazy.click()
time.sleep(2)

blyadi_pack = driver.find_elements(By.CSS_SELECTOR, '.jet-listing-grid__items')
print(blyadi_pack)

blyad = driver.find_elements(By.CSS_SELECTOR, "div.jet-listing-grid__item:nth-child(1)")


blyadi = []
for i in range(1, 10):
    css_selector = f"div.jet-listing-grid__item:nth-child({i})"
    element = driver.find_elements(By.CSS_SELECTOR, css_selector)
    if element:
        blyadi.extend(element)
    else:
        break

with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Услуга", "Цена", "Время", "URL"])  

    for i, element in enumerate(blyadi):
        service_selector = "div.jet-listing-grid__item:nth-child({}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)".format(i+1)
        try:
            service_name = driver.find_element(By.CSS_SELECTOR, service_selector).text
        except:
            service_name = np.nan

        price_selector = "div.jet-listing-grid__item:nth-child({}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1)".format(i+1)
        try:
            price = driver.find_element(By.CSS_SELECTOR, price_selector).text
        except:
            price = np.nan

        time_selector = "div.jet-listing-grid__item:nth-child({}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1)".format(i+1)
        try:
            time_ = driver.find_element(By.CSS_SELECTOR, time_selector).text
        except:
            time_ = np.nan

        img_element = element.find_element(By.XPATH, './/img')
        image_url = img_element.get_attribute('src')

        writer.writerow([service_name, price, time_, image_url])