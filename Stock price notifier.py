from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import yagmail

def get_driver():
  options = webdriver.ChromeOptions()
  options.add_argument('disable-infobars')
  options.add_argument('start-maximized')
  options.add_argument('disable-dev-shm-usage')
  options.add_argument('no-sandbox')
  options.add_experimental_option('excludeSwitches', ['enable-automation'])
  options.add_argument('disable-blink=AutomationControlled')
  driver = webdriver.Chrome(options = options)
  driver.get('https://zse.hr/en/indeks-366/365?isin=HRZB00ICBEX6')
  return driver

def clean_value(initial):
    return float(initial[1:-2]) if initial[0] == '+' else float(initial[:-2])

def get_value():
    driver = get_driver()
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app_indeks"]/section[1]/div/div/div[2]/span[2]')))
    return clean_value(element.text)

sender = 'sender@gmail.com'
receiver = 'jerasod834@ekcsoft.com'
subject = 'CROBEX ALERT'
contents = "CBX is below -0.1 %"

yag = yagmail.SMTP(user=sender, password='PASSWORD')
while True:
    if get_value() <= -0.1:
        yag.send(to=receiver, subject=subject, contents=contents)
        print('email sent')
    time.sleep(3600)
