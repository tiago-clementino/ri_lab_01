# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem
from scrapy.exporters import CsvItemExporter

class RiLab01Pipeline(object):

    def __init__(self):
        self.file = open("output/results.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, unicode)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.format_item(item)
        self.exporter.export_item(item)
        return item
    
    def format_item(self, item):
        for key, value in item.items():
            if value is None or len(value) == 0:
                value = "Não encontrado"
            else:
                if key == "texto":
                    value = "".join(value)
                if key == "data":
                    value = value[1:11]

            item[key] = value.replace(',', '')