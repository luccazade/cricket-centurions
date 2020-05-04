#! /usr/bin/env python3

from selenium import webdriver
import re
import sys
import bs4
import requests


def get_player_ID(name):
    browser = webdriver.Firefox(executable_path='/Library/Frameworks/Python.framework/Versions/3.8/bin/geckodriver')
    browser.get('http://www.howstat.com/cricket/Statistics/Players/PlayerMenu.asp')
    searchBox = browser.find_element_by_css_selector('#txtPlayer')
    searchBox.send_keys(name)
    searchButton = browser.find_element_by_css_selector('#find > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > input:nth-child(3)')
    searchButton.click()
    htmlElem = browser.find_element_by_class_name('LinkNormal').get_attribute('href')
    idRegex = re.compile(r'\d{4}')
    moID = idRegex.search(htmlElem)
    playerID = moID.group()
    return str(playerID)


player = ' '.join(sys.argv[1:])

res = requests.get('http://www.howstat.com/cricket/Statistics/Players/PlayerNotables.asp?PlayerID=' + get_player_ID(player) + '&s=2')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, features="html.parser")