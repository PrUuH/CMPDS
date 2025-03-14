import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def convert_relative_date(date_str):
    today = datetime.now().date()
    if "сегодня" in date_str.lower():
        return today
    elif "вчера" in date_str.lower():
        return today - timedelta(days=1)
    elif "назад" in date_str.lower():
        try:
            days_ago = int(date_str.split()[0])
            return today - timedelta(days=days_ago)
        except ValueError:
            pass
    return None


def parse(url, num_pages_to_parse):
    if num_pages_to_parse <= 0:
        raise ValueError("Number of pages should be more than 0")

    driver = webdriver.Firefox()
    data = []

    try:
        driver.get(url)
        time.sleep(2)

        page_number = 1
        while page_number <= num_pages_to_parse:
            print(f"Parsing page {page_number}")

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
                    date = convert_relative_date(full_date)

                    if date is None:
                        print(f"Skipping invalid date: {full_date}")
                        continue

                    comment_element = item.find_element(By.CSS_SELECTOR, 'span:nth-child(4) > a:nth-child(2)')
                    comment = comment_element.get_attribute('href')

                    data.append({
                        "title": title,
                        "description": description,
                        "date": str(date),
                        "comments": comment
                    })
                except Exception as e:
                    print(f"Error parsing news {idx}: {e}")

            try:
                next_page_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#navigation_1_next_page'))
                )
                next_page_link = next_page_button.get_attribute('href')
                if next_page_link and page_number < num_pages_to_parse:
                    driver.get(next_page_link)
                    time.sleep(2)
                    page_number += 1
                else:
                    print("No more pages or limit reached")
                    break
            except Exception as e:
                print("Pagination failed or page doesn't exist", e)
                break

    finally:
        driver.quit()

    return data