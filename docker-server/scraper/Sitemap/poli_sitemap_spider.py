#!/usr/bin/python

from scrapy import Request, Item, Field
from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from goose3 import Goose

cached_links = []
g = Goose()

class ScraperItem(Item):
    # De bronpagina
    url = Field()
    body = Field()
    title = Field()
    publish_date = Field()


class PoliSitemapSpider (CrawlSpider):
    name = 'poli-sitemap-spider'

    rules = [
        Rule(
            LxmlLinkExtractor(
                allow=[r'nieuws', r'news', r'actueel', r'blog', r'column', r'nu', r'Nieuws', r'standpunten', r'algemeen-nieuws', r'laatste-nieuws'],
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse, dont_filter=True)

      # Methode voor het parsen (inlezen) van items
    def parse_items(self, response):
        # De lijst van items die gevonden zijn op een bepaalde pagina
        items = []
        # Haal alleen unieke links op
        # links = LxmlLinkExtractor(allow=['nieuws', 'news'], canonicalize=True, unique=True).extract_links(response)
        html = response.body.decode('utf-8')
        article = g.extract(raw_html=html)
        item = ScraperItem()
        self.parse_article(article=article, item=item)
        items.append(item)
        # Neem alle links door
        """for link in links:
            # Bekijk of het domein van de URL van de link is toegestaan door het domein te vergelijk met de domeinen in allowed_domains
            is_allowed = False
            for allowed_domain in self.start_urls:
                if link.url.startswith(allowed_domain):
                    is_allowed = True
            # Wanneer het is toegestaan wordt een nieuw item gemaakt en toegevoegd aan de lijst van gevonden item
            if is_allowed:
                item = ScraperItem()
                if response.url not in cached_links:
                    item['url'] = response.url
                    html = response.body.decode('utf-8')
                    article = g.extract(raw_html=html)
                    self.parse_article(article=article, item=item)
                    items.append(item)
                    cached_links.append(response.url)
                elif link.url not in cached_links:
                    item['url'] = link.url
                    article = g.extract(url=link.url)
                    self.parse_article(article=article, item=item)
                    items.append(item)
                    cached_links.append(link.url)

        # Geef alle gevonden items terug"""
        return items

    def parse_article(self, article, item):



        try:
            item['url'] = article.final_url
            item['body'] = article.cleaned_text
            item['title'] = article.title
            item['publish_date'] = article.publish_date
            print("done scraping:", item['title'])
        except ValueError:
            print('Error scraping')

