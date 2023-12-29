from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import time


# Your options may be different
options = Options()

# options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
# this parameter tells Chrome that
# it should be run without UI (Headless)
options.headless = True


def get_next_page(driver):

    soup = scroll(driver,5)
    page = next(soup)

    page.find_all('a', {'id': 'video-title'})
    containers = page.find_all('a', {'id': 'video-title'})
    links = [c.attrs['href'] for c in containers]

    return links



def get_all_videos(url='https://www.youtube.com'):
    # Setup the driver. This one uses firefox with some options and a path to the geckodriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # implicitly_wait tells the driver to wait before throwing an exception
    driver.implicitly_wait(30)
    # driver.get(url) opens the page
    driver.get(url)

    return driver
    


def scroll(driver,timeout):
    scroll_pause_time = timeout
    
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    print("s", last_height)
    
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        last_height = new_height
        
        # Once scroll returns bs4 parsers the page_source
        yield BeautifulSoup(driver.page_source, 'html.parser')

