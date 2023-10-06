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
import json

def remove_iframe(driver):
    try:
        driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="embeddedIframe17225"]'))
        element = driver.find_element(By.XPATH,'//*[@id="survey-wrapper"]/form/footer/div[1]/div[1]/button')
        element.click()
        print("The element exists.")
    except NoSuchElementException:
        print("The element does not exist.")
    driver.switch_to.default_content()

def select_all_sites(driver):
    site = driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[2]/div/div[2]/div/div[1]/div/div[1]/input').get_attribute('value')
    if site != 'All sites':
        driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[2]/div/div[2]/div/div[1]/div/div/input').click()
        driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[2]/div/div[2]/div/div[1]/div/div[2]/ul/li[1]/label').click()
        driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[2]/div/div[2]/div/div[1]/div/div/input').click()
        time.sleep(5)

def scrape_website(email,password,start_date,end_date):
    # create driver here
    options = Options()
    options.add_argument("--headless")
    width = 945
    height = 1020
    driver = webdriver.Chrome(options=options)
    driver.get("https://restaurant-hub.deliveroo.net/login")
    driver.set_window_size(width, height)
    # enter login credentials here
    driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/form/div[2]/label[1]/span/div/input').send_keys(
        email)
    driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/form/div[2]/label[2]/span/div/input').send_keys(
        password)
    driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/form/div[2]/button').click()
    time.sleep(5)

    # check if login was successful
    try:
        x = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/form/div[2]/div[1]').text
        driver.close()
        return x
    except NoSuchElementException:
        pass

    #   redirect to all refunds page
    weblink = 'https://restaurant-hub.deliveroo.net/orders/refunds?orgId='
    parsed_url = urlparse(driver.current_url)
    orgid = parse_qs(parsed_url.query)['orgId'][0]
    final_urls = weblink + orgid + "&startDate=" + start_date + "&endDate=" + end_date
    driver.get(final_urls)
    time.sleep(5)

    remove_iframe(driver)

    if len(driver.find_element(By.XPATH,
                               '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[2]/div').text.split()) == 4:
        main_df = pd.DataFrame(
            columns=['order_id', 'date and time', 'branch', 'restaurant_name', 'status', 'order_total',
                     'partner_refund_value'])
        driver.find_element(By.XPATH,
                            '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[2]/div/div[1]/div/div').click()
        # time.sleep(1)
        restaurants = len(driver.find_element(By.XPATH,
                                              '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[2]/div/div[1]/div/div[2]/ul').text.split(
            '\n'))
        driver.find_element(By.XPATH,
                            '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[2]/div/div[1]/div/div').click()
        for i in range(restaurants):
            driver.find_element(By.XPATH,
                                '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[2]/div/div[1]/div/div').click()
            name_rest = driver.find_element(By.XPATH,
                                      '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[2]/div/div[1]/div/div[2]/ul/li[' + str(
                                          i + 1) + ']').text
            driver.find_element(By.XPATH,
                                '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[2]/div/div[1]/div/div[2]/ul/li[' + str(
                                    i + 1) + ']').click()
            time.sleep(5)
            try:
                site = driver.find_element(By.XPATH,
                                           '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[2]/div/div[3]/div/div[1]/div/div/input').get_attribute(
                    'value')
                if site != 'All sites':
                    driver.find_element(By.XPATH,
                                        '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[2]/div/div[3]/div/div[1]/div/div/input').click()
                    driver.find_element(By.XPATH,
                                        '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[2]/div/div[3]/div/div[1]/div/div[2]/ul/li[1]/label').click()
                    driver.find_element(By.XPATH,
                                        '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[2]/div/div[3]/div/div[1]/div/div/input').click()
                    time.sleep(3)
            except NoSuchElementException:
                pass

            button_enabled = True
            liRes = []
            while button_enabled:
                ls = []
                try:
                    t = driver.find_element(By.XPATH,
                                            '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[4]/div/div/div[2]').text
                    q = t.split('\n')
                    for i in range(0, len(q), 7):
                        liRes.append(",".join(q[i:i + 7]))
                except NoSuchElementException:
                    pass
                button_enabled = False
                try:
                    button_enabled = driver.find_element(By.XPATH,
                                                         '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[4]/div/div/div[3]/div/button[2]').is_enabled()
                except NoSuchElementException:
                    print("The element does not exist.")
                if button_enabled:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    driver.find_element(By.XPATH,
                                        '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[4]/div/div/div[3]/div/button[2]').click()
                    time.sleep(5)

            my_data = [x.split(',') for x in liRes]
            if liRes[0] == "No items to display right now. Try changing the dates you've selected.":
                continue
            df = pd.DataFrame(np.row_stack(my_data),
                              columns=['order_id', 'date and time', 'branch', 'drop', 'status', 'order_total',
                                       'partner_refund_value'])
            df = df.drop(['drop'], axis=1)
            df['restaurant_name'] = name_rest
            df['order_total'] = df['order_total'].str.replace('£', '')
            df['partner_refund_value'] = df['partner_refund_value'].str.replace('£', '')
            main_df = pd.concat([main_df, df])
        driver.close()
        return main_df


    elif len(driver.find_element(By.XPATH,
                               '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[2]/div').text.split()) == 3:
        select_all_sites(driver)
        button_enabled = True
        liRes = []
        while button_enabled:
            ls = []
            try:
                t = driver.find_element(By.XPATH,
                                        '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[4]/div/div/div[2]').text
                q = t.split('\n')
                for i in range(0, len(q), 7):
                    liRes.append(",".join(q[i:i + 7]))
            except NoSuchElementException:
                pass
            button_enabled = False
            try:
                button_enabled = driver.find_element(By.XPATH,
                                                     '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[4]/div/div/div[3]/div/button[2]').is_enabled()
            except NoSuchElementException:
                print("The element does not exist.")
            if button_enabled:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                driver.find_element(By.XPATH,
                                    '//*[@id="__next"]/div[1]/main/div[2]/div/div[3]/div[4]/div/div/div[3]/div/button[2]').click()
                time.sleep(5)

        my_data = [x.split(',') for x in liRes]
        if liRes[0] == "No items to display right now. Try changing the dates you've selected.":
            driver.close()
            return 'No data available in the date range'
        df = pd.DataFrame(np.row_stack(my_data),
                          columns=['order_id', 'date and time', 'branch', 'drop', 'status', 'order_total',
                                   'partner_refund_value'])
        df = df.drop(['drop'], axis=1)
        df['order_total'] = df['order_total'].str.replace('£', '')
        df['partner_refund_value'] = df['partner_refund_value'].str.replace('£', '')
        driver.close()
        return df




