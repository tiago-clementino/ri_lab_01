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
    # def process_item(self, item, spider):
    #     return item

    def __init__(self):
        self.file = open("output/results.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, unicode)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        # self.create_valid_csv(item)
        return item
    
    def create_valid_csv(self, item):
        for key, value in item.items():
            is_string = (isinstance(value, basestring))
            if (is_string and ("," in value.encode('utf-8'))):
                item[key] = "\"" + value + "\""
        
        return item
