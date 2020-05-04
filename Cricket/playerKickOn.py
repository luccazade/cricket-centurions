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


scores = {
    'out': [],
    'in': []
}

outRegex = re.compile(r'\d\d\d')
inRegex = re.compile(r'\d\d\d\*')
scoreRegex = re.compile(r'\d\d\d\*?')

scoresAll = soup.select('td [align="right"]')
for i in range(len(scoresAll) - 1):
    '''moAll = scoreRegex.search(scoresAll[i].getText())
    scoreX = moAll.group()
    scores['all'].append(scoreX)'''
    moIn = inRegex.search(scoresAll[i].getText())
    try:
        scoreY = moIn.group()
        moIn.sub(r'\d\d\d\*', r'\d\d\d', scoreY)
        scores['in'].append(scoreY)
    except AttributeError:
        try:
            moOut = outRegex.search(scoresAll[i].getText())
            scoreX = moOut.group()
            scores['out'].append(scoreX)
        except AttributeError:
            continue


def find_Total():
    total = 0
    notOuts = len(scores['in'])
    outs = len(scores['out'])
    for i in range(outs):
        total += int(scores['out'][i])
    for i in range(notOuts):
        total += int(scores['in'][i])
    return total


def find_Average():
    if find_Total() == 0:
        print('N/A, no centuries scored')
    else:
        average = find_Total() / len(scores['out'])
        return average


print(find_Total())
print(find_Average())

