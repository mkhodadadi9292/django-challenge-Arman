from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver
driver = webdriver.Chrome()

# Navigate to the desired page
driver.get("https://debank.com/profile/0x6982508145454ce325ddbe47a25d4ec3d2311933")

try:
    # Wait for the body element to be present
    body = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    import time
    time.sleep(10)
    # Once the body element is present, fetch its content
    body_content = body.text
    print(body_content)

finally:
    # Remember to close the WebDriver after use
    driver.quit()
