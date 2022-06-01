from scrapy.exporters import CsvItemExporter, JsonItemExporter
from scrapy import signals


class Save_to_json:
    """
    Save to json file.
    """
    def __init__(self):
        file = open('datas.json', 'w+b')
        self.exporter = JsonItemExporter(file, ensure_ascii=False, indent=4)

    def spider_opened(self, spider):
        self.exporter.start_exporting()

    @classmethod
    def spider_closed(self, cls, spider):
        self.exporter.finish_exporting()
        cls.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class Save_to_csv:
    """
    Save to csv file.
    """
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s_datas.csv' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.fields_to_export = [
            'category_name',
            'sub_category_name',
            'product_name',
            'modification',
            'description',
            'characteristics',
            'id',
            'your_price',
            'rrc_and_mrc',
            'url',
        ]
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
