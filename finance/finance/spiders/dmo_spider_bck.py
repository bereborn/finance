import scrapy

class DmoSpider(scrapy.Spider):
    name = "finance"
    allowed_domains = ["data.eastmoney.com"]
    start_urls = [
        "http://data.eastmoney.com/cjsj/gpkhsj.html",
    ]

    def __init__(self, *args, **kwargs):
        super(DmoSpider, self).__init__(*args, **kwargs)
        fund_type = ["pg", "gp", "hh", "zq", "zs", "qdii"] # 偏股票型 股票型 混合型 债券型 指数型 QDII
        time_span = ["z", "v", "3y", "6y", "1n", "2n", "3n", "jn", "ln"] # 1周 1月 3月 6月 1年 2年 3年 今年 成立
        for ftype in fund_type:
            for tspan in time_span:
                url = "https://fundapi.eastmoney.com/fundtradenew.aspx?ft={}&sc={}&st=desc&pi=1&pn=100&cp=&ct=&cd=&ms=&fr=&plevel=&fst=&ftype=&fr1=&fl=0&isab=1".format(ftype, tspan)
                self.start_urls.append(url)

    def parse(self, response):
        print("start")
        print(response)
        filename = response.url.split("/")[-2]
        print(filename)
        print(response.xpath('//*[@class="tab1"]/tbody/tr[1]').extract_first())
        # for tr in response.xpath('//*[@class="tab1"]/tbody/tr'):
        #     print(tr)
            # for td in tr.xpath('./td'):
            #     print(td[1])

        print("end")
