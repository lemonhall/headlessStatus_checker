import time
  
from selenium import webdriver
  
# initializing webdriver for Chrome
driver = webdriver.Chrome()
  
# getting GeekForGeeks webpage
driver.get('https://www.geeksforgeeks.org')
  
# sleep for 5 seconds just to see that
# the browser was opened indeed
time.sleep(5)
  
# closing browser
driver.close()