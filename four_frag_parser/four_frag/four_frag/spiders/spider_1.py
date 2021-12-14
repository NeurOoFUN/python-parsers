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
            yield response.follow(urls, self.pagenation)

    def pagenation(self, response):
        pages_count = response.xpath('//div[@class="col-pager"]/a/@href').getall()[-1].split('=')[1]
        for i in range(1, int(pages_count) + 1):
            url = response.url + f'?page={i}'
            yield response.follow(url, self.parse_product_links)

    def parse_product_links(self, response):
        """
        Сбор ссылок на каждый товар.
        """
        for item in response.xpath('//div[@class="row-viewed col-catalog-grid product-grid"]//div[@class="item-product-inner"]/a/@href').getall():
            yield response.follow(item, self.parse)

    def parse(self, response):
        item = FourFragItem()
        item['category_name'] = response.xpath('//li[@class="dropdown-submenu"]/a/span/text()'.strip()).getall()
        item['url'] = response.url
        item['name'] = response.xpath('//h1[@itemprop="name"]/text()').getall()
        item['price'] = response.xpath('//div[@class="panel-body prices product-info"]//span[@class="item-price"]/text()').getall()
        item['img_link'] = response.xpath('//div[@class="image-inner"]//a[@class="thumbnail"]/img/@src').get()
        item['manufacturer'] = response.xpath('//div[@class="col-xs-60 blockshortinfo"]/strong/text()').get()
        item['specifications'] = response.xpath('//table[@class="table table-striped table-hover"]/tbody/tr/th/text()'.strip()).getall()
        yield item
