from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
def  main():

  url =  "https://google.com"
  driver = webdriver.Chrome()
  wait = WebDriverWait(driver, 10)
  driver.get(url)
  username = driver.find_element_by_id("session_key")
  username.send_keys("emilianopp550@gmail.com")
  password = driver.find_element_by_id("session_password")
  password.send_keys("Emilianopp1")
  driver.find_element_by_class_name("sign-in-form__submit-button").click()

def login_to_linkedin(driver):
  username = driver.find_element_by_id("session_key")
  username.send_keys("emilianopp550@gmail.com")
  password = driver.find_element_by_id("session_password")
  password.send_keys("Emilianopp1")
  driver.find_element_by_class_name("sign-in-form__submit-button").click()

main()