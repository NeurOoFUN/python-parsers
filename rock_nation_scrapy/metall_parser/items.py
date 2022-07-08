import re

import scrapy
from scrapy.loader.processors import MapCompose


def parse_java(value):
    pattern = re.findall(
        r'http://rocknation\.su/upload/mp3/.+?\.mp3',
        value
    )
    return pattern


class MetallParserItem(scrapy.Item):
    url = scrapy.Field()
    group_name = scrapy.Field()
    album_name = scrapy.Field()
    download_ref = scrapy.Field(
        input_processor=MapCompose(parse_java),
    )
