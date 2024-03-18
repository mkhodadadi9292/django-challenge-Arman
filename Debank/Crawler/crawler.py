import time
import pandas as pd
from selenium.webdriver import Chrome
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from loguru import logger
import sqlite3

def fetch_page(profile_id):
    url = f"https://debank.com/profile/{profile_id}"
    # driver = webdriver.Chrome()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(10)
    driver.get(url)

    time.sleep(15)

    elements = driver.find_elements(By.TAG_NAME, 'body')

    with open(f'output/raw_result/{profile_id}.http', 'w') as f:
        f.write(elements[0].text)

    result = elements[0].text
    driver.quit()
    return result


def convert_to_json(text, profile_id):
    output = []
    indicator = {'token', 'price', 'amount', 'usd value'}
    lines = [line.strip() for line in text.split('\n')]
    target_line_index = 0
    for i in range(len(lines) - 4):
        if set([x.lower() for x in lines[i:i + 4]]) == indicator:
            target_line_index = i
            break
    if target_line_index > 0:
        for j in range(target_line_index, len(lines) - 4, 4):
            output.append([x.strip() for x in lines[j:j + 4]])
    with open(f'output/json_result/{profile_id}.json', 'w') as f:
        json.dump(output, f)
    return output


if __name__ == "__main__":
    with open('wallet_list', 'r') as f:
        try:
            for profile_id in f:
                _profile_id = profile_id.strip()
                text = fetch_page(profile_id=_profile_id)
                convert_to_json(text=text, profile_id=_profile_id)

        except Exception as err:
            logger.error(f"{profile_id=}, error_message={err}")
