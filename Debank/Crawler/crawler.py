import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


def fetch_page():
    url = "https://debank.com/profile/0x6982508145454ce325ddbe47a25d4ec3d2311933"
    # driver = webdriver.Chrome()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(10)
    driver.get(url)

    import time
    time.sleep(15)

    elements = driver.find_elements(By.TAG_NAME, 'body')

    with open('y.http', 'w') as f:
        f.write(elements[0].text)

    result = elements[0].text
    driver.quit()
    # for sub_element in elements:
    #     print(sub_element.text)
    return result


def convert_to_json(text):
    import json
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
    with open('output1.json', 'w') as f:
        json.dump(output, f)
    return output

if __name__ == "__main__":
    convert_to_json(fetch_page())
