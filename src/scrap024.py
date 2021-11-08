#
# https://medium.com/@stevelukis/scraping-an-online-shop-website-with-scrapy-5f88c89c3a83
#
"""
Passos:
1. pip install Scrapy scrapy-user-agents
2. scrapy startproject elextra
3. Edite o criado elextra/settings.py  
    DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}
4. scrapy genspider elextraonline elextraonline.com
5. Edite o criado elextra/items.py
import scrapy


class ElextraItem(scrapy.Item):
    name = scrapy.Field()
    image_link = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
6. Edite elextra/spiders/elextraonline.py (delete a linha allowed_domain) por:
start_urls = ['https://elextraonline.com/kategori/logitech-products/']
7. Edite elextra/spiders/elextraonline.py para formato abaixo:
8. scrapy crawl elextraonline -o result.csv -t csv
"""

import scrapy
from scrapy import Selector

from ..items import ElextraItem


class ElextraonlineSpider(scrapy.Spider):
    name = 'elextraonline'
    start_urls = ['https://elextraonline.com/kategori/logitech-products/']

    def parse(self, response, **kwargs):
        product_links: list = response.css("p.name.product-title > a::attr(href)")

        for product in product_links:
            href = product.extract()
            yield response.follow(href, callback=self.parse_product)

        # Handling pagination
        next_page: str = response.css("a.next.page-number::attr('href')").get()
        if next_page:
            print(next_page)
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        item: ElextraItem = ElextraItem()
        item['name'] = response.css("h1.product-title.entry-title::text").get().strip()
        item['price'] = response.css("span.woocommerce-Price-amount.amount::text").getall()[-1].strip()
        item['image_link'] = response.css(
            "img.attachment-shop_single.size-shop_single.wp-post-image::attr('src')").get().strip()

        desc_selector = Selector(text=response.css("div#tab-description").get())
        desc_text_list = desc_selector.xpath('//div//text()').getall()
        desc = ''

        for desc_text in desc_text_list:
            desc += desc_text

        desc = desc.replace('DESKRIPSI', '').strip()

        description_result = response.css("div#tab-description > p::text").extract()
        for res in description_result:
            desc += res
        item['description'] = desc

        return item
