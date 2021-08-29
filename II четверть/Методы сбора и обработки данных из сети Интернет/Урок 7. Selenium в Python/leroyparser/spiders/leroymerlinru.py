import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from leroyparser.items import LeroyparserItem


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@data-qa="product-image"]')

        next_page = response.xpath('//a[contains(@aria-label, "Следующая")]/@href').get()
        if next_page:
            response.follow(next_page, callback=self.parse)

        for link in links:
            yield response.follow(link, callback=self.product_parse)

    def product_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('article', '//span[@slot="article"]/@content')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('images', '//img[@slot="thumbs"]/@src')
        # Product details
        loader.add_xpath('detail_names', '//dt[@class="def-list__term"]/text()')
        loader.add_xpath('detail_values', '//dd[@class="def-list__definition"]/text()')

        yield loader.load_item()
