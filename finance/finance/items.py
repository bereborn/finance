# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FinanceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class StockAccountStatisticsInfoItem(scrapy.Item):
    """股票账户统计信息"""

    SDATE = scrapy.Field()    # 数据日期
    # 新增投资者
    XZSL = scrapy.Field()    # 数量(万户)
    XZHB = scrapy.Field()    # 环比
    XZTB = scrapy.Field()    # 同比
    # 期末投资者(万户)
    QMSL = scrapy.Field()     # 总量
    QMSL_A = scrapy.Field()   # A股账户
    QMSL_B = scrapy.Field()   # B股账户

    # 上证指数
    SZZS = scrapy.Field()     # 收盘
    SZZDF = scrapy.Field()   # 涨跌幅

    HSZSZ = scrapy.Field()    # 沪深总市值(万亿)
    HJZSZ = scrapy.Field()    # 沪深户均市值(万)

class FundRankInfoItem(scrapy.Item):
    """基金排行信息"""
    fund_code = scrapy.Field()                          # 基金代码
    fund_name = scrapy.Field()                          # 基金名称
    fund_type = scrapy.Field()                          # 基金类型
    inquire_date = scrapy.Field()                       # 查询日期
    net_asset_value = scrapy.Field()                    # 单位净值
    daily_growth_rate = scrapy.Field()                  # 日增长率
    nearly_a_week = scrapy.Field()                      # 近1周
    nearly_a_month = scrapy.Field()                     # 近1月
    nearly_three_month = scrapy.Field()                 # 近3月
    nearly_six_month = scrapy.Field()                   # 近6月
    nearly_a_year = scrapy.Field()                      # 近1年
    nearly_two_year = scrapy.Field()                    # 近2年
    nearly_three_year = scrapy.Field()                  # 近3年
    since_this_year = scrapy.Field()                    # 今年来
    since_established = scrapy.Field()    # 成立来
