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


process = CrawlerProcess()

d = process.crawl(poli.PoliSitemapSpider, start_urls=[start_url], allowed_domains=[domain])
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished


print("Klaar met artikelen genereren.")

