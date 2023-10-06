import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
from urllib.parse import parse_qs
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import numpy as np
from django.core.exceptions import ValidationError

def scrape_website(email,password,start_date,end_date):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://restaurant-hub.deliveroo.net/login")


    driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/form/div[2]/label[1]/span/div/input').send_keys(
        email)
    driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/form/div[2]/label[2]/span/div/input').send_keys(
        password)
    driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/form/div[2]/button').click()
    time.sleep(5)

    try:
        x = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/form/div[2]/div[1]').text
        return x
    except NoSuchElementException:
        pass


    weblink = 'https://restaurant-hub.deliveroo.net/orders/refunds?orgId='
    parsed_url = urlparse(driver.current_url)
    orgid = parse_qs(parsed_url.query)['orgId'][0]

    final_urls = weblink + orgid + "&startDate=" + start_date + "&endDate=" + end_date
    driver.get(final_urls)
    time.sleep(5)


    try:
        driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="embeddedIframe17225"]'))
        element = driver.find_element(By.XPATH, '//*[@id="survey-wrapper"]/form/footer/div[1]/div[1]/button')
        element.click()
        print("The element exists.")
    except NoSuchElementException:
        print("The element does not exist.")
    driver.switch_to.default_content()
    button_enabled = True
    ls = []

    while button_enabled:
        try:
            elem = driver.find_elements(By.XPATH,
                                        '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[4]/div/div/div[2]/div')
            for e in elem:
                x = e.text
                q = x.split('\n')
                q.append(e.find_element(By.XPATH, 'div[1]/p/a').get_attribute('href'))
                ls.append(q)
        except NoSuchElementException:
            print("The element does not exist.")

        button_enabled = False
        try:
            button_enabled = driver.find_element(By.XPATH,
                                                 '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[4]/div/div/div[3]/div/button[2]').is_enabled()
        except NoSuchElementException:
            return 'No data available in the date range'
        if button_enabled:
            driver.find_element(By.XPATH,
                                '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[4]/div/div/div[3]/div/button[2]').click()
            time.sleep(5)



    df = pd.DataFrame(np.row_stack(ls), columns=['order_id', 'date and time', 'branch', 'drop', 'status', 'order_total',
                                                 'partner_refund_value', 'reason_link'])
    df = df.drop(['drop'], axis=1)
    df['order_total'] = df['order_total'].str.replace('£', '')
    df['partner_refund_value'] = df['partner_refund_value'].str.replace('£', '')

    return df