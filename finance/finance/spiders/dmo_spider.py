import scrapy
import re
import json

from finance.items import StockAccountStatisticsInfoItem

# 保留两位小数
def keep_two_decimal_places(num):
    try:
        return str(num).split('.')[0] + '.' + str(num).split('.')[1][:2]
    except:
        return num
def percentage(num):
    return ('%s%%' % (str(num)) )

class DmoSpider(scrapy.Spider):
    name = "finance"
    start_urls = [
        "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=GPKHData&token=894050c76af8597a853f5b408b759f5d&st=SDATE&sr=-1&p=1&ps=10000&js=var%20PdHyZRkj={pages:(tp),data:(x)}&rt=52632393",
    ]

    def parse(self, response):
        print("start")
        # print(response)
        # print(response.text)
        data = response.text
        matchObj = re.search( r'\[.*\]', data, re.M|re.I)
        if matchObj:
            # print("matchObj.group() : ", matchObj.group())
            data = json.loads(matchObj.group())
        else:
            print("No match!!")

        for item in data:
            fi = StockAccountStatisticsInfoItem()

            fi["SDATE"] = item["SDATE"]    # 数据日期
            # 新增投资者
            fi["XZSL"] = keep_two_decimal_places(item["XZSL"])     # 数量(万户)
            fi["XZHB"] = percentage(keep_two_decimal_places(item["XZHB"]))    # 环比
            fi["XZTB"] = percentage(keep_two_decimal_places(item["XZTB"]))    # 同比
            # 期末投资者(万户)
            fi["QMSL"] = keep_two_decimal_places(item["QMSL"])     # 总量
            fi["QMSL_A"] = keep_two_decimal_places(item["QMSL_A"])   # A股账户
            fi["QMSL_B"] = keep_two_decimal_places(item["QMSL_B"])   # B股账户

            # 上证指数
            fi["SZZS"] = keep_two_decimal_places(item["SZZS"])     # 收盘
            fi["SZZDF"] = keep_two_decimal_places(item["SZZDF"])   # 涨跌幅

            fi["HSZSZ"] = keep_two_decimal_places(item["HSZSZ"])    # 沪深总市值(万亿)
            fi["HJZSZ"] = keep_two_decimal_places(item["HJZSZ"])    # 沪深户均市值(万)

            yield fi
            # print("{}   {}   {}   {}   {}   {}   {}   {}   {}   {}万亿   {}万".format(SDATE, XZSL, XZHB, XZTB, QMSL, QMSL_A, QMSL_B, SZZS, SZZDF, HSZSZ, HJZSZ))

        print("end")