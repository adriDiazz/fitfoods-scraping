import sys
import json
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

def scrapeMeal(browser, result, meal):
    div_xpath = ''
    first_div_cal_xpath = ''
    second_div_cal_xpath = ''
    if meal == 'breakfast':
        div_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[1]/div[3]/div/ul'
        first_div_cal_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[1]/div[3]/div/ul/li[1]'
        second_div_cal_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[1]/div[3]/div/ul/li[2]'
    elif meal == 'lunch':
        div_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[3]/div[3]/div/ul'
        first_div_cal_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[2]/div[3]/div/ul/li[1]'
        second_div_cal_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[2]/div[3]/div/ul/li[2]'
    elif meal == 'dinner':
        div_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[3]/div[3]/div/ul'
        first_div_cal_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[3]/div[3]/div/ul/li[1]'
        second_div_cal_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[3]/div[3]/div/ul/li[2]'
    else: # Snack
        div_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[4]/div[3]/div/ul'
        first_div_cal_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[4]/div[3]/div/ul/li'
        second_div_cal_xpath = ''

    
    first_food_cal = browser.find_element(By.XPATH, first_div_cal_xpath)
    first_hover = ActionChains(browser).move_to_element(first_food_cal)
    first_hover.perform()
    time.sleep(5)
    first_food_cal = first_food_cal.get_attribute('data-original-title')
    first_food_cal = first_food_cal.split('<div class="tt_macro_amt">')[1].split('</div>')[0]
    if (second_div_cal_xpath != ''):
        second_food_cal = browser.find_element(By.XPATH, second_div_cal_xpath)
        second_hover = ActionChains(browser).move_to_element(second_food_cal)
        second_hover.perform()
        time.sleep(5)
        second_food_cal = second_food_cal.get_attribute('data-original-title')
        second_food_cal = second_food_cal.split('<div class="tt_macro_amt">')[1].split('</div>')[0]

    meal_div = browser.find_element(
        By.XPATH, div_xpath)

    time.sleep(1)
    index = 0
    for li in meal_div.find_elements(By.TAG_NAME, 'li'):
        plate = li.find_element(By.CLASS_NAME, 'print_name').text
        selector = Select(li.find_element(
            By.CLASS_NAME, 'food_units_selector'))

        selector.select_by_index(0)

        time.sleep(4)

        grams = li.find_element(
            By.CLASS_NAME, 'amount_input').get_attribute('value')

        if meal == 'snack':
            result[meal].append({
                    'name': plate,
                    'grams': grams,
                    'cals': first_food_cal
                })
        else:
            if index == 0:
                result[meal].append({
                    'name': plate,
                    'grams': grams,
                    'cals': first_food_cal
                })
            else:
                result[meal].append({
                    'name': plate,
                    'grams': grams,
                    'cals': second_food_cal
                })
            
        index+=1

def scrapeMenu(browser, result):

    regen_btn = browser.find_element(
        By.XPATH, '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[1]/div/div[2]/div/span')
    TIMES_TO_REGEN = 5
    for i in range(TIMES_TO_REGEN):
        regen_btn.click()
        time.sleep(8)
        scrapeMeal(browser, result, 'breakfast')
        scrapeMeal(browser, result, 'lunch')
        scrapeMeal(browser, result, 'dinner')
        scrapeMeal(browser, result, 'snack')

    print(result)


def getDietByCalories(calories, result):

    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    s=Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=s)

    browser.get('https://www.eatthismuch.com/')

    caloriasInput = browser.find_element(By.XPATH, '//*[@id="cal_input"]')
    caloriasInput.send_keys(str(calories))

    generateBtn = browser.find_element(
        By.XPATH, '//*[@id="main_container"]/div/div[2]/div[1]/div[2]/div[6]/div/button')

    generateBtn.click()

    time.sleep(7)

    scrapeMenu(browser, result)

if __name__ == '__main__':
    result = {
        'breakfast': [],
        'lunch': [],
        'dinner': [],
        'snack': [],

    }

    CALORIES = 2000

    getDietByCalories(CALORIES, result)
    with open('menus.json', 'w') as f:
        json.dump(result, f, indent=4)
