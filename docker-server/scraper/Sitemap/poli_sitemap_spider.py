from scrapy import Request, Item, Field
from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
cached_links = []
class ScraperItem(Item):
    # De bronpagina
    url = Field()
    html = Field()


class PoliSitemapSpider (CrawlSpider):
    name = 'poli-sitemap-spider'
    rules = [
        Rule(
            LxmlLinkExtractor(
                allow=['nieuws', 'news'],
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
        links = LxmlLinkExtractor(allow=['nieuws', 'news'], canonicalize=True, unique=True).extract_links(response)
        # Neem alle links door
        for link in links:
            # Bekijk of het domein van de URL van de link is toegestaan door het domein te vergelijk met de domeinen in allowed_domains
            is_allowed = False
            for allowed_domain in self.start_urls:
                if link.url.startswith(allowed_domain):
                    is_allowed = True
            # Wanneer het is toegestaan wordt een nieuw item gemaakt en toegevoegd aan de lijst van gevonden item
            if is_allowed:
                item = ScraperItem()
                item['html'] = response
                if response.url not in cached_links:
                    item['url'] = response.url
                    items.append(item)
                    cached_links.append(response.url)
                elif link.url not in cached_links:
                    item['url'] = link.url
                    items.append(item)
                    cached_links.append(link.url)

        # Geef alle gevonden items terug
        return items
