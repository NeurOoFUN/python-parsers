from scrapy.loader.processors import Compose, Join
import scrapy


def correct_description(value):
    for i in value:
        yield i.strip()


class PriemkaScraperItem(scrapy.Item):
    city = scrapy.Field()
    description = scrapy.Field(
        input_processor=Compose(correct_description),
        output_processor=Join()
    )
