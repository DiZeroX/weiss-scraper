import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
from langdetect import detect
from lxml import html

import json

# from dicttoxml import dicttoxml
# from xml.dom.minidom import parseString

base_url = "https://littleakiba.com/tcg/weiss-schwarz/"
series_id_url = "browse.php?series_id="

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options)

driver.get(base_url)
series_elements = driver.find_elements_by_xpath("//a[contains(@href,'browse.php?series_id=')]")

series_ids = []
titles = []
# reverse array of elements, find series_id and title
for element in series_elements[::-1]:
    html = element.get_attribute("outerHTML")
    series_id = re.search('href=\\"browse\\.php\\?series_id=(\\d+)\\"', html)
    series_ids.append(series_id.group(1))
    title = re.search('title=\\"([^//"]+)', html)
    titles.append(title.group(1))

# convert to array of dicts with key:value of series_id: title
series_id_dicts = []
for i, series_id in enumerate(series_ids):
    series_id_dicts.append({series_ids[i]: titles[i]})

with open("series.json", "w") as fout:
    json.dump(series_id_dicts, fout)

# xml = dicttoxml(series_id_dicts)
# dom = parseString(xml)
# xml = dom.toprettyxml()

# xml_file = open("series_ids.xml", "w", encoding="utf-8")
# xml_file.write(xml)
# xml_file.close()
