import scrapy
from scrapy.loader.processors import Compose


class PromledScrapyParserItem(scrapy.Item):

    def take_category_name(value):
        if value[-4] == 'Категории':
            return value[-3]
        else:
            return value[-4]

    def take_sub_category_name(value):
        if value[-4] == 'Категории':
            return 'sub_category_name is not find'
        else:
            return value[-3]

    def take_product_name(value):
        return value[-2]

    category_name = scrapy.Field(
        input_processor=Compose(take_category_name)
    )
    sub_category_name = scrapy.Field(
        input_processor=Compose(take_sub_category_name)
    )
    product_name = scrapy.Field(
        input_processor=Compose(take_product_name)
    )
    modification = scrapy.Field()
