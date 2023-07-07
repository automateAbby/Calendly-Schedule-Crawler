from selenium import webdriver
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(options=chrome_options)

# Now you can start using Selenium

def setSched(email, name, url):
    browser.get(url)
    browser.find_element_by_id("email").send_keys(email)
    browser.find_element_by_id("name").send_keys(name)
    submit_button = browser.find_element_by_css_selector("button[type='submit']")
    submit_button.click()
    return browser.find_element_by_id("result").text