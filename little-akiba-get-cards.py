from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import sys


with open("series.json", "r") as read_file:
    series = json.load(read_file)

base_url = "https://littleakiba.com/tcg/weiss-schwarz/"
series_id_url = "browse.php?series_id="
final_url = base_url + series_id_url + list(series[0])[0]

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options)

driver.get(final_url)

title = driver.find_element_by_tag_name("h2").text
print(title)




