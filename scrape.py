#! /usr/bin/env python3
import requests, bs4


def newCompany(company):
    url = 'https://en.wikipedia.org'+company
    res = requests.get(url)
    res.raise_for_status()
    noStarchSoup = bs4.BeautifulSoup(res.text, 'html.parser')

    table = noStarchSoup.find("table", class_="infobox")

    if table.find(href='/wiki/Subsidiary'):
        print(table.find(href='/wiki/Subsidiary').find_parent())
        # print(table.find(href='/wiki/Subsidiary'))
        subLink = table.find(href='/wiki/Subsidiary')
        th = subLink.parent
        td = th.find_next_sibling('td')
        if td.find('div'): # If has multiple subsidiaries
            items = td.find('div').find('ul').find_all('li')
        else: # If only has 1 subsidiary
            items = td
        subsidiaries = {}
        for item in items:
            if item.a:
                subsidiaries[item.a.get('href')] = item.a.string
                # newCompany(item.a.get('href'))
            else:
                subsidiaries[items.index(item)] = item.string

        return subsidiaries

print(newCompany('/wiki/Walmart'))
