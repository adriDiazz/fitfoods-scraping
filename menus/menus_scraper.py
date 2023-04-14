import sys
import json
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import mysql.connector


def scrapeMeal(browser, result, meal):
    div_xpath = ''
    first_div_cal_xpath = ''
    second_div_cal_xpath = ''
    first_div_img = ''
    second_div_img = ''
    if meal == 'breakfast':
        div_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[1]/div[3]/div/ul'
        first_div_cal_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[1]/div[3]/div/ul/li[1]'
        second_div_cal_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[1]/div[3]/div/ul/li[2]'
        first_div_img = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[1]/div[3]/div/ul/li[1]/div/div/div[1]/div'
        second_div_img = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[1]/div[3]/div/ul/li[2]/div/div/div[1]/div'
    elif meal == 'lunch':
        div_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[3]/div[3]/div/ul'
        first_div_cal_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[2]/div[3]/div/ul/li[1]'
        second_div_cal_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[2]/div[3]/div/ul/li[2]'
        first_div_img = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[2]/div[3]/div/ul/li[1]/div/div/div[1]/div'
        second_div_img = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[2]/div[3]/div/ul/li[2]/div/div/div[1]/div'
    elif meal == 'dinner':
        div_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[3]/div[3]/div/ul'
        first_div_cal_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[3]/div[3]/div/ul/li[1]'
        second_div_cal_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[3]/div[3]/div/ul/li[2]'
        first_div_img = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[3]/div[3]/div/ul/li[1]/div/div/div[1]/div'
        second_div_img = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[3]/div[3]/div/ul/li[2]/div/div/div[1]/div'
    else: # Snack
        div_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[4]/div[3]/div/ul'
        first_div_cal_xpath = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[4]/div[3]/div/ul/li'
        second_div_cal_xpath = ''
        first_div_img = '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/div/div/div[4]/div[3]/div/ul/li/div/div/div[1]/div'
        second_div_img = ''
    
    first_food_cal = browser.find_element(By.XPATH, first_div_cal_xpath)
    first_hover = ActionChains(browser).move_to_element(first_food_cal)
    first_hover.perform()
    time.sleep(5)
    first_food_cal = first_food_cal.get_attribute('data-original-title')
    first_food_cal = first_food_cal.split('<div class="tt_macro_amt">')[1].split('</div>')[0]

    first_food_img = browser.find_element(By.XPATH, first_div_img)
    first_food_img = first_food_img.get_attribute('style')
    first_food_img = first_food_img.split("url(")[1]
    first_food_img = first_food_img.split('")')[0]
    print(first_food_img)
    if (second_div_cal_xpath != ''):
        second_food_cal = browser.find_element(By.XPATH, second_div_cal_xpath)
        second_hover = ActionChains(browser).move_to_element(second_food_cal)
        second_hover.perform()
        time.sleep(5)
        second_food_cal = second_food_cal.get_attribute('data-original-title')
        second_food_cal = second_food_cal.split('<div class="tt_macro_amt">')[1].split('</div>')[0]

        second_food_img = browser.find_element(By.XPATH, second_div_img)
        second_food_img = second_food_img.get_attribute('style')
        second_food_img = second_food_img.split("url(")[1]
        second_food_img = second_food_img.split('")')[0]

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
        hundred_grams = 0.0
        try:
            hundred_grams = float(float(grams.split(" ")[0]) + float(grams.split(" ")[1].split("/")[0]) / float(grams.split(" ")[1].split("/")[1]))
        except:
            hundred_grams = grams

        if meal == 'snack':
            first_food_hundred_cal = float(100*float(first_food_cal)/float(hundred_grams))
            result[meal].append({
                    'name': plate,
                    'grams': 100,
                    'cals': round(first_food_hundred_cal, 2),
                    'url': first_food_img
                })
        else:
            if index == 0:
                first_food_hundred_cal = float(100*float(first_food_cal)/float(hundred_grams))
                result[meal].append({
                    'name': plate,
                    'grams': 100,
                    'cals': round(first_food_hundred_cal, 2),
                    'url': first_food_img
                })
            else:
                second_food_hundred_cal = float(100*float(second_food_cal)/float(hundred_grams))
                result[meal].append({
                    'name': plate,
                    'grams': 100,
                    'cals': round(second_food_hundred_cal, 2),
                    'url': second_food_img
                })
            
        index+=1

def scrapeMenu(browser, result):

    regen_btn = browser.find_element(
        By.XPATH, '//*[@id="main_container"]/div/div[4]/div[1]/div[1]/div/div[1]/div/div[2]/div/span')
    TIMES_TO_REGEN = 1
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
    # Conectarse a la base de datos
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="fitfoods2",
        port=3308
    )
    cursor = mydb.cursor()
    for l in result["breakfast"]:
        cursor.execute("INSERT INTO food (name, type, url, calories) VALUES (%s, %s, %s, %s)", (l["name"], "breakfast", l['url'], l["cals"]))
    for l in result["lunch"]:
        cursor.execute("INSERT INTO food (name, type, url, calories) VALUES (%s, %s, %s, %s)", (l["name"], "lunch", l['url'], l["cals"]))
    for l in result["dinner"]:
        cursor.execute("INSERT INTO food (name, type, url, calories) VALUES (%s, %s, %s, %s)", (l["name"], "dinner", l['url'], l["cals"]))
    for l in result["snack"]:
        cursor.execute("INSERT INTO food (name, type, url, calories) VALUES (%s, %s, %s, %s)", (l["name"], "snack", l['url'], l["cals"]))

    # Crear un cursor para ejecutar las consultas SQL
    mydb.commit()
    cursor.close()
    mydb.close()
    with open('menus.json', 'w') as f:
        json.dump(result, f, indent=4)
