import lightbus
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

bus = lightbus.create()

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


class getLantStatus(lightbus.Api):

    class Meta:
        name = 'getLantStatus'

    def get(self):
        driver.get("http://192.168.50.233:13233/#/replica")
        lantern_status_element = driver.find_element(By.ID,"lantern__status_module")
        if lantern_status_element:
            lantern_status_text = lantern_status_element.find_element(By.CLASS_NAME, "text")
            if lantern_status_text:
                #print(lantern_status_text)
                #get_methods(lantern_status_text)
                print(lantern_status_text.text)
                return lantern_status_text.text
            else:
                return "unknown status"
        else:
            return "unknown status"
# Register this API with Lightbus. Lightbus will respond to
# remote procedure calls for registered APIs, as well as allow you
# as the developer to fire events on any registered APIs.
bus.client.register_api(getLantStatus())
