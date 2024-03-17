from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from typing import Dict, List, Any

def convert_comperes_body_to_dict(compressed_data: Any) -> Dict | List:
    import gzip
    import json

    # Assuming `compressed_data` contains the binary data you provided
    # compressed_data = b'\x1f\x8b\x08\x00\xb4...'
    # Decompress the data
    json_data = gzip.decompress(compressed_data).decode('utf-8')
    # Parse the JSON data
    parsed_json = json.loads(json_data)

    # Now you can work with the parsed JSON data
    print(parsed_json)
    return parsed_json


svc = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=svc)



driver.implicitly_wait(15)

driver.get('https://debank.com/profile/0x6982508145454ce325ddbe47a25d4ec3d2311933')

import time

time.sleep(10)

for req in driver.requests:
    if req.response:
        print(
            req.url,
            req.response.status_code,
            req.headers,
            req.response.headers
        )
