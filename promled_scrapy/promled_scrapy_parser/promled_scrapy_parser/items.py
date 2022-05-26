import scrapy
from scrapy.loader.processors import Compose, Join


def take_category_name(value):
    if value[-4] == 'Категории':
        return value[-3]
    else:
        return value[-4]


def take_sub_category_name(value):
    if value[-4] == 'Категории':
        return 'not find'
    else:
        return value[-3]


def take_product_name(value):
    return value[-2]


def split_id(value):
    return value[0].split(': ')[1]


def edit_description_and_characteristics(value):
    for i in value:
        yield i.strip()


class PromledScrapyParserItem(scrapy.Item):
    url = scrapy.Field()
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
    id = scrapy.Field(input_processor=Compose(split_id))
    description = scrapy.Field(
        input_processor=Compose(edit_description_and_characteristics),
        output_processor=Join()
    )
    characteristics = scrapy.Field(
        input_processor=Compose(edit_description_and_characteristics),
        output_processor=Join()
    )
    price = scrapy.Field()
