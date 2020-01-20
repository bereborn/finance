# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from finance.items import StockAccountStatisticsInfoItem

class FinancePipeline(object):
    def process_item(self, item, spider):
        return item

class StockAccountStatisticsInfoPipeline(object):
    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if isinstance(item, StockAccountStatisticsInfoItem):
            print("{}   {}   {}   {}   {}   {}   {}   {}   {}   {}万亿   {}万".format(item["SDATE"], item["XZSL"], item["XZHB"], item["XZTB"], item["QMSL"], item["QMSL_A"], item["QMSL_B"], item["SZZS"], item["SZZDF"], item["HSZSZ"], item["HJZSZ"]))