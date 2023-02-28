from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import json
import sys


def scrapeMenu(browser, result):

    breakFastDiv = browser.find_element(
        By.XPATH, '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[1]/div[3]/div/ul')

    for li in breakFastDiv.find_elements(By.TAG_NAME, 'li'):
        plate = li.find_element(By.CLASS_NAME, 'print_name').text
        selector = Select(li.find_element(
            By.CLASS_NAME, 'food_units_selector'))

        selector.select_by_index(0)

        time.sleep(4)

        value = li.find_element(
            By.CLASS_NAME, 'amount_input').get_attribute('value')

        result['breakfast'].append({
            'name': plate,
            'value': value
        })
        # result['breakfast']['value'] = li.find_element(
        #     By.XPATH, 'amount_input').get_attribute('value')

    lunchDiv = browser.find_element(
        By.XPATH, '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[3]/div[3]/div/ul')

    for li in lunchDiv.find_elements(By.TAG_NAME, 'li'):
        plate = li.find_element(By.CLASS_NAME, 'print_name').text
        selector = Select(li.find_element(
            By.CLASS_NAME, 'food_units_selector'))

        selector.select_by_index(0)

        time.sleep(2)

        value = li.find_element(
            By.CLASS_NAME, 'amount_input').get_attribute('value')

        result['lunch'].append({
            'name': plate,
            'value': value
        })

    dinnerDiv = browser.find_element(
        By.XPATH, '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[3]/div[3]/div/ul')

    for li in dinnerDiv.find_elements(By.TAG_NAME, 'li'):
        plate = li.find_element(By.CLASS_NAME, 'print_name').text
        selector = Select(li.find_element(
            By.CLASS_NAME, 'food_units_selector'))

        selector.select_by_index(0)

        time.sleep(4)

        value = li.find_element(
            By.CLASS_NAME, 'amount_input').get_attribute('value')

        result['dinner'].append({
            'name': plate,
            'value': value
        })

    snackDiv = browser.find_element(
        By.XPATH, '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[4]/div[3]/div/ul')

    for li in snackDiv.find_elements(By.TAG_NAME, 'li'):
        plate = li.find_element(By.CLASS_NAME, 'print_name').text
        selector = Select(li.find_element(
            By.CLASS_NAME, 'food_units_selector'))

        selector.select_by_index(0)

        time.sleep(4)

        value = li.find_element(
            By.CLASS_NAME, 'amount_input').get_attribute('value')

        result['snack'].append({
            'name': plate,
            'value': value
        })

    regenBtn = browser.find_element(
        By.XPATH, '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[1]/div/div[2]/div/span')

    for i in range(3):
        regenBtn.click()
        time.sleep(4)
        breakFastDiv = browser.find_element(
            By.XPATH, '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[1]/div[3]/div/ul')

        for li in breakFastDiv.find_elements(By.TAG_NAME, 'li'):
            plate = li.find_element(By.CLASS_NAME, 'print_name').text
            selector = Select(li.find_element(
                By.CLASS_NAME, 'food_units_selector'))
            selector.select_by_index(0)

            time.sleep(4)

            value = li.find_element(
                By.CLASS_NAME, 'amount_input').get_attribute('value')
            result['breakfast'].append({
                'name': plate,
                'value': value
            })
        # result['breakfast']['value'] = li.find_element(
        #     By.XPATH, 'amount_input').get_attribute('value')

        lunchDiv = browser.find_element(
            By.XPATH, '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[3]/div[3]/div/ul')

        for li in lunchDiv.find_elements(By.TAG_NAME, 'li'):
            plate = li.find_element(By.CLASS_NAME, 'print_name').text
            selector = Select(li.find_element(
                By.CLASS_NAME, 'food_units_selector'))
            selector.select_by_index(0)

            time.sleep(4)

            value = li.find_element(
                By.CLASS_NAME, 'amount_input').get_attribute('value')
            result['lunch'].append({
                'name': plate,
                'value': value
            })

        dinnerDiv = browser.find_element(
            By.XPATH, '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[3]/div[3]/div/ul')

        for li in dinnerDiv.find_elements(By.TAG_NAME, 'li'):
            plate = li.find_element(By.CLASS_NAME, 'print_name').text
            selector = Select(li.find_element(
                By.CLASS_NAME, 'food_units_selector'))
            selector.select_by_index(0)

            time.sleep(4)

            value = li.find_element(
                By.CLASS_NAME, 'amount_input').get_attribute('value')
            result['dinner'].append({
                'name': plate,
                'value': value
            })

        snackDiv = browser.find_element(
            By.XPATH, '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[4]/div[3]/div/ul')

        for li in snackDiv.find_elements(By.TAG_NAME, 'li'):
            plate = li.find_element(By.CLASS_NAME, 'print_name').text
            selector = Select(li.find_element(
                By.CLASS_NAME, 'food_units_selector'))
            selector.select_by_index(0)

            time.sleep(4)

            value = li.find_element(
                By.CLASS_NAME, 'amount_input').get_attribute('value')

            result['snack'].append({
                'name': plate,
                'value': value
            })

    print(result)


def getDietByCalories(calories, result):

    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')

    browser = webdriver.Chrome()

    browser.get('https://www.eatthismuch.com/')

    caloriasInput = browser.find_element(By.XPATH, '//*[@id="cal_input"]')
    caloriasInput.send_keys(str(calories))

    generateBtn = browser.find_element(
        By.XPATH, '//*[@id="main_container"]/div/div[2]/div[1]/div[2]/div[6]/div/button')

    generateBtn.click()

    time.sleep(7)

    scrapeMenu(browser, result)

    # return json.dumps(result)


if __name__ == '__main__':
    result = {
        'breakfast': [],
        'lunch': [],
        'dinner': [],
        'snack': [],

    }
    getDietByCalories(2000, result)

    # Save to mysql database
