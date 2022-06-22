import re

import scrapy
from scrapy.loader.processors import MapCompose


def parse_java(value):
    pattern = re.findall(
        # r"(http://rocknation\.su/upload/mp3/\w*\s*\w*\s*\w*\s*\w*\s*/\d+ - \w+\s*\w*\s*\w*\s*\w*\s*[\w+'\w+]*\s*\w*/\S+.mp3)",
        r'http://rocknation\.su/upload/mp3/.+\.mp3',
        value
    )
    return pattern


def split_java(value):
    pattern = re.split(r'"},{title: "\d+. \w+\s*\w+\s*\w*\s*",free: true, mp3:', value)  # FIXME
    return pattern


class MetallParserItem(scrapy.Item):
    url = scrapy.Field()
    group_name = scrapy.Field()
    album_name = scrapy.Field()
    download_ref = scrapy.Field(
        input_processor=MapCompose(parse_java, split_java),
    )
