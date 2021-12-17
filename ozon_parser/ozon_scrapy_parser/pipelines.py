# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single inte
import json


from itemadapter import ItemAdapter


class OzonScrapyParserPipeline:
    def process_item(self, item, spider):
        with open('datas.json', 'a') as file:
            line = json.dumps(dict(item), ensure_ascii=False, indent=4)
            file.write(line)
            return item
