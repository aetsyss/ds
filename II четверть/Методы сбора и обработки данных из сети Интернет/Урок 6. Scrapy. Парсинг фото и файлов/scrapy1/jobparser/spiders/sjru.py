import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']
    source = 'https://superjob.ru/'

    def parse(self, response: HtmlResponse):
        links = response.xpath('//div[@class="f-test-search-result-item"]//a[contains(@href, "vakansii")]/@href').extract()
        next_page = response.xpath('//a[@rel="next"][2]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name_data = response.xpath('//h1/text()').extract_first()
        salary_data = "1000" # TODO
        url_data = response.url
        yield JobparserItem(name=name_data, salary=salary_data, url=url_data, source=self.source)