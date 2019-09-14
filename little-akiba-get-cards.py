from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import sys
import xml.etree.ElementTree as ET
import pdb
from xml.dom import minidom
import csv
import time
import os
import urllib.request

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

card_elements = driver.find_elements_by_xpath("//div[@class='card_list short']/ul/li/a")
card_urls = []
for element in card_elements:
    card_urls.append(element.get_attribute("href"))
title = driver.find_element_by_tag_name("h2").text

with open(title+'.csv', 'w', newline='') as csvfile:
    fieldnames = ["card_id", "name_jp", "type", "color", "level", "cost", "trigger", "power", "soul", "trait1_en",
                  "trait1_jp", "trait2_en", "trait2_jp", "effect_en", "effect_jp", "flavor_jp", "image", "url"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # card_url = card_urls[0]
    card_url = "https://littleakiba.com/tcg/weiss-schwarz/card.php?card_id=6619"
    driver.get(card_url)
    card_dict = {}
    card_dict["card_id"] = driver.find_element_by_xpath("//*[@id='content']/div/div[4]/div[2]/small").text
    card_dict["name_jp"] = driver.find_element_by_xpath("//*[@id='content']/div/div[4]/div[2]/h4").text
    card_dict["type"] = driver.find_element_by_xpath("//*[@id='content']/div/div[4]/div[2]/ul/li[1]").text[7:]
    card_dict["color"] = driver.find_element_by_xpath("//*[@id='content']/div/div[4]/div[2]/ul/li[2]").text[8:]
    card_dict["level"] = driver.find_element_by_xpath("//*[@id='content']/div/div[4]/div[2]/ul/li[3]").text[8:]
    card_dict["cost"] = driver.find_element_by_xpath("//*[@id='content']/div/div[4]/div[2]/ul/li[4]").text[7:]
    card_dict["trigger"] = driver.find_element_by_xpath("//*[@id='content']/div/div[4]/div[2]/ul/li[5]").text[10:]
    card_dict["power"] = driver.find_element_by_xpath("//*[@id='content']/div/div[4]/div[2]/ul/li[6]").text[8:]
    if card_dict["type"] == "Character":
        card_dict["soul"] = driver.find_element_by_xpath("//*[@id='content']/div/div[4]/div[2]/ul/li[7]").text[7:]

        # trait logic
        trait_element = driver.find_element_by_xpath("//*[@id='content']/div/div[4]/div[2]/ul/li[8]/div/div")
        trait_array = trait_element.text.split('《')
        # 2 traits
        if len(trait_array) == 3:
            card_dict["trait1_en"] = trait_array[0].strip()
            trait_array2 = trait_array[1].split('》')
            card_dict["trait1_jp"] = driver.find_element_by_xpath("//*[@id='showTraitCards1']").text
            card_dict["trait2_en"] = trait_array2[1][1:]
            card_dict["trait2_jp"] = driver.find_element_by_xpath("//*[@id='showTraitCards2']").text
        elif len(trait_array) == 2:
            card_dict["trait1_en"] = trait_array[0].strip()
            card_dict["trait1_jp"] = driver.find_element_by_xpath("//*[@id='showTraitCards1']").text
            card_dict["trait2_en"] = "N/A"
            card_dict["trait2_jp"] = "N/A"
        else:
            card_dict["trait1_en"] = "N/A"
            card_dict["trait1_jp"] = "N/A"
            card_dict["trait2_en"] = "N/A"
            card_dict["trait2_jp"] = "N/A"

    effect_en = driver.find_element_by_xpath("//*[@id='content']/div/div[4]/div[2]/p[2]").text
    if effect_en != "":
        card_dict["effect_en"] = effect_en
        card_dict["effect_jp"] = driver.find_element_by_xpath("//*[@id='content']/div/div[4]/div[2]/p[3]").text
    else:
        card_dict["effect_en"] = "N/A"
        card_dict["effect_jp"] = "N/A"

    flavor_jp = driver.find_element_by_xpath("//*[@id='content']/div/div[4]/div[2]/p[6]").text
    if flavor_jp != "":
        card_dict["flavor_jp"] = flavor_jp
    else:
        card_dict["flavor_jp"] = "N/A"

    card_dict["image"] = driver.find_element_by_xpath("//*[@id='content']/div/div[4]/div[1]/a").get_attribute("href")
    card_dict["url"] = card_url

    os.mkdir("images/cards/"+title)
    urllib.request.urlretrieve(card_dict["image"], card_dict["set_id"]+".jpg")

    print(card_dict)

    # for card_url in card_urls:
    #     # retrieve card info
    #     driver.get(card_url)
    #     card_dict = {}
    #     card_dict["set_id"] = driver.find_element_by_xpath("//*[@id='content']/div/div[4]/div[2]/h4/text()")
    #     time.sleep(60)










