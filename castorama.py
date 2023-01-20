import scrapy
from scrapy.http import HtmlResponse
from home_work6.items import HomeWork6Item
from scrapy.loader import ItemLoader


class CastoramaSpider(scrapy.Spider):
    name = 'castorama'
    allowed_domains = ['castorama.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.castorama.ru/catalogsearch/result/?q={kwargs.get("search")}']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@class="product-card__img-link"]')
        for link in links:
            yield response.follow(link, callback=self.parse_ads)


    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=HomeWork6Item(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//span[@class = "price" ]//span//text() | //span[@class="measure"]//text()')
        loader.add_xpath('photos', '//img[@role = "presentation"]/@src')
        loader.add_value('url', response.url)
        yield loader.load_item()


        # name = response.xpath('//h1/text()').get()
        # price = response.xpath('//span[@class = "price" ]//span//text() | //span[@class="measure"]//text()').getall()
        # photos = response.xpath('//img[@role = "presentation"]/@src').get() #Динамика. В Chropath ссылка достается, не извлекается в скрапи из-за JavaSkript, пытался решить через splash, у меня еще и проблемы с Docker:(
        # url = response.url
        # yield HomeWork6Item(name=name, price=price, photos=photos, url=url)


        #'//div[@class="js-zoom-container"]/img[@role="presentation"]/@src'