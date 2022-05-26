from scrapy.exporters import CsvItemExporter, JsonItemExporter


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
        file = open('datas.csv', 'w+b')
        self.exporter = CsvItemExporter(file)

    def spider_opened(self, spider):
        self.exporter.fields_to_export = ['city', 'description', ]
        self.exporter.start_exporting()

    @classmethod
    def spider_closed(self, cls, spider):
        self.exporter.finish_exporting()
        cls.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
