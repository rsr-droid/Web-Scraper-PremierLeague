import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# set up driver to control Chrome browser
driver = webdriver.Chrome("/Users/rajanrai/Documents/chromedriver 2")

# request driver to open URL
# The sleep() function suspends (waits) execution of the current thread for a given number of seconds.
driver.get("https://www.premierleague.com/players?se=363&cl=-1")
time.sleep(1)

elem = driver.find_element_by_tag_name("body")

# set number of pages for browser to scroll down in order to get full list of players
no_of_pagedowns = 60
while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns-=1
    
# Pull URL links for each player
links = [elem.get_attribute("href") for elem in driver.find_elements_by_tag_name('a')]
url_links = [url for url in links if 'https://www.premierleague.com/players/' in url]
base_url = list(map(lambda x: x.replace('/overview',''),url_links))

# Data Frame to store scrapped URLs for each player
df = pd.DataFrame({"URL Links":base_url})
df.to_csv('player_urls.csv', index = False)
print(df, "\n Success")
