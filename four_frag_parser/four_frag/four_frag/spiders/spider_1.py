import scrapy


from four_frag.items import FourFragItem


class Spider1Spider(scrapy.Spider):
    """
    Собственно сам паук.
    """
    name = 'spider_1'
    allowed_domains = ['4frag.ru']


    def start_requests(self):
        """
        Ссылки с которых паук начинает обход сайта.
        В данном случае ссылка одна, стартовая страница сайта.
        """
        start_urls = ['https://4frag.ru/', ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_all_category)


    def parse_all_category(self, response):
        """
        Сбор ссылок на все категории товаров. (мышки, клавиатуры и т.д.)
        """
        category_urls = response.xpath('//li[@class="dropdown-submenu"]/a/@href').getall()
        for urls in category_urls:
            yield response.follow(urls, self.parse_product_links)
        last_page = response.xpath('//div[@class="col-pager"]/a/@href').getall()[-1].split('=')[1]
        if last_page is not None:
            for i in range(1, int(last_page) + 1):
                page = urls + f'?page={i}'
                yield response.follow(page, self.parse_product_links)


    def parse_product_links(self, response):
        """
        Сбор ссылок на каждый товар.
        """
        for item in response.xpath('//div[@class="row-viewed col-catalog-grid product-grid"]//div[@class="item-product-inner"]/a/@href').getall():
            yield response.follow(item, self.parse)

    def parse(self, response):
        item = FourFragItem()
        item['url'] = response.url
        item['name'] = response.xpath('//h1[@itemprop="name"]/text()').getall()
        item['price'] = response.xpath('//div[@class="panel-body prices product-info"]//span[@class="item-price"]/text()').getall()
        item['img_link'] = response.xpath('//div[@class="image-inner"]//a[@class="thumbnail"]/img/@src').get()
        yield item
