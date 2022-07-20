# File: bus.py
import lightbus
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

bus = lightbus.create()
# instance of Options class allows
# us to configure Headless Chrome
options = Options()

# this parameter tells Chrome that
# it should be run without UI (Headless)
options.headless = True

# initializing webdriver for Chrome with our options
driver = webdriver.Chrome(options=options)


class getLantStatus(lightbus.Api):

    class Meta:
        name = 'getLantStatus'

    def get(self):
    	driver.get('https://www.geeksforgeeks.org')
    	print(driver.title)
    	return driver.title

# Register this API with Lightbus. Lightbus will respond to 
# remote procedure calls for registered APIs, as well as allow you 
# as the developer to fire events on any registered APIs.
bus.client.register_api(getLantStatus())