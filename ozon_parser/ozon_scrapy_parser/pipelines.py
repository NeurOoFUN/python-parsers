# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single inte
import json

from itemadapter import ItemAdapter
from scrapy import signals
from scrapy.exporters import CsvItemExporter


class Save_to_json:
    def process_item(self, item, spider):
        with open('datas.json', 'a') as file:
            line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False, indent=4)
            file.write(line)
            return item


class CSVPipeline:
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('datas.csv', 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.fields_to_export = ["url", "product_name", "price", "specifications", "img_link", "id", ]
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class CharleschurchPipeline:
    def process_item(self, item, spider):
        return item
