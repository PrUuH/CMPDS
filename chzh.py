from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import string
import random
import time
from concurrent.futures.thread import ThreadPoolExecutor


options = Options()
options.headless = True

browser = webdriver.Firefox(options=options)

# button = browser.find_element(By.CSS_SELECTOR, "html body.home.page-template-default.page.page-id-76.wp-custom-logo.ast-desktop.ast-page-builder-template.ast-no-sidebar.astra-4.6.7.ast-single-post.ast-inherit-site-logo-transparent.ast-theme-transparent-header.ast-hfb-header.ast-full-width-primary-header.ast-full-width-layout.elementor-page-481.elementor-page-90.elementor-default.elementor-template-full-width.elementor-kit-11.astra-addon-4.5.1.seraph-accel-view-cmn.lzl-ed.e--ua-firefox.dialog-body.dialog-lightbox-body.dialog-container.dialog-lightbox-container.lzl-cached div#elementor-popup-modal-603.dialog-widget.dialog-lightbox-widget.dialog-type-buttons.dialog-type-lightbox.elementor-popup-modal div.dialog-widget-content.dialog-lightbox-widget-content.animated div.dialog-message.dialog-lightbox-message div.elementor.elementor-603.elementor-location-popup div.elementor-element.elementor-element-3b3d4a0.e-flex.e-con-boxed.e-con.e-parent div.e-con-inner div.elementor-element.elementor-element-931f2fd.elementor-align-justify.close-popup.elementor-widget.elementor-widget-button div.elementor-widget-container div.elementor-button-wrapper a#yesclick.elementor-button.elementor-size-sm")
# print(button.text)

# button.click()

def generate_random_string(lenght):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(lenght))
    return rand_string

def scraper(url):
    browser = webdriver.Firefox(options=options)
    browser.get(url)
    button = browser.find_element(By.CSS_SELECTOR, "#yesclick")
    button.click()
    browser.quit()

urls = ["https://garem54.ru/"] * 100

executor = ThreadPoolExecutor(50)

for url in urls:
    executor.submit(scraper, url + "/" + generate_random_string(10))