import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from dzprivatbank.items import Article


class DzprivatbankSpider(scrapy.Spider):
    name = 'dzprivatbank'
    start_urls = ['https://www.dz-privatbank.com/dzpb/de/pressemeldungen.html']

    def parse(self, response):
        links = response.xpath('//a[@class="btn btn-primary btn-small mt-3"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h2[@class="h2 heading"]/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//p[@class="overline"]/text()').get()
        if date:
            date = " ".join(date.strip().split()[1:])

        content = response.xpath('//div[@class="module text-img"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
