import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = "https://bloknot-taganrog.ru/?ysclid=m7rn2l9uga977283728"

try:
    num_pages_to_parse = int(input("Enter your num of pages to parse:"))
    if num_pages_to_parse <= 0:
        print("Num of pages should be more than 0")
        exit()
except ValueError:
    print("Incorrect input. Num of pages must be an integer")
    exit()

driver = webdriver.Firefox()

try:
    driver.get(url)
    time.sleep(2)

    with open('data_blocknot.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Заголовок', 'Краткое описание', 'Дата', 'Кол-во комментариев'])

        page_number = 1
        while page_number <= num_pages_to_parse:
            print(f"Page {page_number}")

            bigline_block = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'bigline'))
            )

            news_items = bigline_block.find_elements(By.XPATH, './/*[contains(@id, "bx_3218110189_")]')
            print(f"Found {len(news_items)} news items on page {page_number}")

            for idx, item in enumerate(news_items, start=1):
                try:
                    title_element = item.find_element(By.CSS_SELECTOR, 'a:nth-child(2)')
                    title = title_element.text.strip()

                    description_element = item.find_element(By.CSS_SELECTOR, 'a:nth-child(3)')
                    description = description_element.text.strip()

                    date_element = item.find_element(By.CSS_SELECTOR, 'span:nth-child(4)')
                    full_date = date_element.text.strip()
                    date = full_date.split()[0]  

                    comment_element = item.find_element(By.CSS_SELECTOR, 'span:nth-child(4) > a:nth-child(2)')
                    comment = comment_element.get_attribute('href')

                    writer.writerow([title, description, date, comment])
                except Exception as e:
                    print(f"Fatal error for news {idx}: {e}")

            try:
                next_page_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#navigation_1_next_page'))
                )
                next_page_link = next_page_button.get_attribute('href')
                if next_page_link and page_number < num_pages_to_parse:
                    driver.get(next_page_link)
                    time.sleep(3)
                    page_number += 1
                else:
                    print("Page not found or limit reached")
                    break
            except Exception as e:
                print("Pagination failed or page doesn't exist", e)
                break

finally:
    driver.quit()