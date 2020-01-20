#-*- coding: UTF-8 -*-

import scrapy
import re
import json
import time

from finance.items import StockAccountStatisticsInfoItem

# 保留两位小数
def keep_two_decimal_places(num):
    try:
        return str(num).split('.')[0] + '.' + str(num).split('.')[1][:2]
    except:
        return num
def percentage(num):
    return ('%s%%' % (str(num)) )

def match(pattern, data):
    matchObj = re.search( pattern, data, re.M|re.I)
    if matchObj:
        # print("matchObj.group() : ", matchObj.group())
        return json.loads(matchObj.group())
    else:
        return ""
        # print("No match!!")

class FundRankSpider(scrapy.Spider):
    name = "fund_rank"

    def start_requests(self):
        # fund_type = ["pg", "gp", "hh", "zq", "zs", "qdii"] # 偏股票型 股票型 混合型 债券型 指数型 QDII
        # time_span = ["z", "v", "3y", "6y", "1n", "2n", "3n", "jn", "ln"] # 1周 1月 3月 6月 1年 2年 3年 今年 成立
        fund_type = ["pg"] # 偏股票型 股票型 混合型 债券型 指数型 QDII
        time_span = ["z"] # 1周 1月 3月 6月 1年 2年 3年 今年 成立
        for ftype in fund_type:
            for tspan in time_span:
                url = "https://fundapi.eastmoney.com/fundtradenew.aspx?ft={}&sc={}&st=desc&pi=1&pn=100&cp=&ct=&cd=&ms=&fr=&plevel=&fst=&ftype=&fr1=&fl=0&isab=1".format(ftype, tspan)
                headers = {
                    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                    "Accept-Encoding":"gzip, deflate",
                    "Referer":"http://fund.eastmoney.com/trade/{}.html".format(ftype),
                }

                yield scrapy.Request(url=url, headers=headers, meta={"fund_type": ftype, "time_span": tspan}, callback=self.parse_fund_rank)

    # 基金排名解析
    def parse_fund_rank(self, response):
        meta = response.meta
        # print(response.text)
        data = match(r"\[.*\]", response.text)
        
        # 取前五个数据
        data = data[0:5]
        rank = 1
        for fund in data:
            meta["fund"] = fund
            meta["rank"] = rank
            rank = rank + 1

            info = fund.split("|")
            fund_code = info[0]                         # 基金代码
            meta["fund_code"] = fund_code

            url = "http://fund.eastmoney.com/{}.html".format(fund_code)
            headers = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding":"gzip, deflate",
                "Referer":"http://fund.eastmoney.com/{}.html".format(fund_code),
            }
            yield scrapy.Request(url=url, headers=headers, meta=meta, callback=self.parse_fund)


    # 基金主页解析
    def parse_fund(self, response):
        meta = response.meta

        meta["established_date"] = response.xpath('//*[@class="infoOfFund"]//tr[2]/td[1]/text()').extract_first().strip('：')   # 成立日期
        # print(established_date)

        fund_position_end_date = response.xpath('//div[@id="quotationItem_DataTable"]//li[@id="position_shares"]//span[@class="end_date"]/text()').extract_first().strip('持仓截止日期: ') # 持仓截止日期
        url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={}&topline=10&year={}&month=".format(meta["fund_code"],fund_position_end_date.split("-")[0])
        headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding":"gzip, deflate",
            "Referer":"http://fundf10.eastmoney.com/ccmx_{}.html".format(meta["fund_code"]),
        }
        yield scrapy.Request(url=url, headers=headers, meta=meta, callback=self.parse_fund_position)

    # 基金持仓解析
    def parse_fund_position(self, response):
        meta = response.meta
        # print(response.text)

        fund_position = []
        # 基金季度持仓
        for fund_quarter_position in response.xpath('//body/div[@class="box"]'):
            quarter = fund_quarter_position.xpath('.//label[@class="left"]/text()').extract_first().strip()
            date = fund_quarter_position.xpath('.//label[@class="right lab2 xq505"]/font[@class="px12"]/text()').extract_first()
            quarter = "{}   时间: {}".format(quarter, date)
            # print(str(quarter))

            stock_table = []
            for item in fund_quarter_position.xpath('.//table[@class="w782 comm tzxq"]/tbody/tr'):
                rank = item.xpath('./td[1]/text()').extract_first()                                             # 持仓排行
                stock_code = item.xpath('./td[2]/a/text()').extract_first()                                     # 股票代号
                stock_name = item.xpath('./td[@class="tol"]/a/text()').extract_first()                          # 股票名称
                shareholding_proportion = item.xpath('./td[@class="tor"][last()-2]/text()').extract_first()     # 持股比例
                shareholding_number = item.xpath('./td[@class="tor"][last()-1]/text()').extract_first()         # 持股数(万股)
                shareholding_market_value = item.xpath('./td[@class="tor"][last()]/text()').extract_first()     # 持股市值(万元)

                # print("{} {} {} {} {} {}".format(rank, stock_code, stock_name, shareholding_proportion, shareholding_number, shareholding_market_value))
                stock_table.append("{}|{}|{}|{}|{}|{}".format(rank, stock_code, stock_name, shareholding_proportion, shareholding_number, shareholding_market_value))

            info = {
                "quarter" : quarter,
                "stock_table" : stock_table,
            }
            fund_position.append(info)
        
        # 基金季度持仓
        # [{"quarter" : quarter, "stock_table" : stock_table}]
        # stock_table = [{持仓排行|股票代号|股票名称|持股比例|持股数(万股)|持股市值(万元)}]
        meta["fund_position"] = fund_position
        

        url = "http://fund.eastmoney.com/pingzhongdata/{}.js".format(meta["fund_code"])
        headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding":"gzip, deflate",
            "Referer":"http://fund.eastmoney.com/{}.html".format(meta["fund_code"]),
        }
        yield scrapy.Request(url=url, headers=headers, meta=meta, callback=self.parse_fund_info)


    # 基金详情解析
    def parse_fund_info(self, response):
        fund = response.meta["fund"]
        fund_type = response.meta["fund_type"]  # 基金类型
        time_span = response.meta["time_span"]
        rank = response.meta["rank"]
        fund_position = response.meta["fund_position"]
        print("start")
        # print(json.dumps(response.meta,ensure_ascii=False))
        # print(response.text)

        # response.text 解析
        info = response.text.split(";")
        # idx = 0
        # for item in info:
        #     print("{} {}".format(idx, item))
        #     idx = idx +1

        fund_position_measure = match(r"\[.*\]", info[14])  # 基金仓位预测
        # print(fund_position_measure)

        fund_similar_ranking_trends = match(r"\[.*\]", info[18])  # 基金同类排名走势
        # print(fund_similar_ranking_trends)
        fund_similar_ranking_percentage = match(r"\[.*\]", info[19])  # 基金同类排名百分比
        # print(fund_similar_ranking_percentage)


        fund_code = fund[0]                         # 基金代码
        fund_name = fund[1]                         # 基金名称
        fund_type = fund[2]                         # 基金类型
        inquire_date = fund[3]                      # 查询日期
        net_asset_value = fund[4]                   # 单位净值
        daily_growth_rate = percentage(fund[5])     # 日增长率
        nearly_a_week = percentage(fund[6])         # 近1周
        nearly_a_month = percentage(fund[7])        # 近1月
        nearly_three_month = percentage(fund[8])    # 近3月
        nearly_six_month = percentage(fund[9])      # 近6月
        nearly_a_year = percentage(fund[10])        # 近1年
        nearly_two_year = percentage(fund[11])      # 近2年
        nearly_three_year = percentage(fund[12])    # 近3年
        since_this_year = percentage(fund[13])      # 今年来
        since_established = percentage(fund[14])    # 成立来


        print("end")