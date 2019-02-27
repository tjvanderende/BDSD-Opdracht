from goose3 import Goose
import pandas as pd
import numpy as np
from scrapy import signals
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
import tldextract
import sys
import os
sys.path.append('./scraper/Sitemap')
import poli_sitemap_spider as poli
from argparse import ArgumentParser

import pymongo as mongod

"""
Haal argument "inputwebsite" op.
"""
inputwebsite = os.environ['INPUT']

"""
Haal de domain naam op van de meegegeven website.
"""
start_url = inputwebsite
extracted_domain = tldextract.extract(start_url)
domain = extracted_domain[0]+'.'+extracted_domain[1]+'.'+extracted_domain[2]

print("Start analyse op:", start_url)

print("Verwijder eerst de originele links.csv bestand...")
print("TODO: Evt ondubbelen ipv alles te verwijderen en opnieuw te laten lopen.")
print("test")
client = mongod.MongoClient("mongodb://MONGODB:27017/")


try:

    os.remove("links.json")
except FileNotFoundError:
    print("Nog geen links.json, eerste keer starten")

process = CrawlerProcess({
    'FEED_URI': 'links.json',
    'FEED_FORMAT': 'json'
})

d = process.crawl(poli.PoliSitemapSpider, start_urls=[start_url], allowed_domains=[domain])
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished


print("Klaar met artikelen genereren..")
url_list = pd.read_json('./links.json')

print("Klaar met alles inladen...")
print("Alles wordt nu opgeslagen in de bigdata opslag...")


db = client['admin']
collection = db[domain]

collection.insert_many(url_list.to_dict('records'))
