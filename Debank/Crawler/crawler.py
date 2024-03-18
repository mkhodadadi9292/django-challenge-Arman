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
        json.dump(output, f, indent=4)
    return output


if __name__ == "__main__":
    from repository import Repository
    with open('wallet_list', 'r') as f:
        try:
            for profile_id in f:
                repo = Repository(db_path='db')
                _profile_id = profile_id.strip()
                text = fetch_page(profile_id=_profile_id)
                convert_to_json(text=text, profile_id=_profile_id)

                # When status code is set to 1, it means that
                # the profile data has already  fetched and processed correctly.

                with repo.connection:
                    repo.write_status(profile_id=_profile_id, status=1)
                logger.info(f"profile_id: {profile_id} fetched successfully")

        except Exception as err:
            with repo.connection:
                repo.write_status(profile_id=_profile_id, status=0)
            logger.error(f"{profile_id=}, error_message={err}")
