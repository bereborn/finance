import urllib.request

# 1月
# http://api.fund.eastmoney.com/pinzhong/LJSYLZS?fundCode=005911&indexcode=000300&type=m&callback=jQuery18305396514868947342_1579143124274&_=1579143351097

# 3月
# http://api.fund.eastmoney.com/pinzhong/LJSYLZS?fundCode=005911&indexcode=000300&type=q&callback=jQuery18305396514868947342_1579143124274&_=1579143363096

# 6月
# http://api.fund.eastmoney.com/pinzhong/LJSYLZS?fundCode=005911&indexcode=000300&type=hy&callback=jQuery18305396514868947342_1579143124274&_=1579143376008

# 1年
# http://api.fund.eastmoney.com/pinzhong/LJSYLZS?fundCode=005911&indexcode=000300&type=y&callback=jQuery18305396514868947342_1579143124274&_=1579143383320

# 3年
# http://api.fund.eastmoney.com/pinzhong/LJSYLZS?fundCode=005911&indexcode=000300&type=try&callback=jQuery18305396514868947342_1579143124274&_=1579143394728

# 5年
# http://api.fund.eastmoney.com/pinzhong/LJSYLZS?fundCode=005911&indexcode=000300&type=fiy&callback=jQuery18305396514868947342_1579143124274&_=1579143404248

# 今年
# http://api.fund.eastmoney.com/pinzhong/LJSYLZS?fundCode=005911&indexcode=000300&type=sy&callback=jQuery18305396514868947342_1579143124274&_=1579143411184

# 最大
# http://api.fund.eastmoney.com/pinzhong/LJSYLZS?fundCode=005911&indexcode=000300&type=se&callback=jQuery18305396514868947342_1579143124274&_=1579143421233

url = "http://api.fund.eastmoney.com/pinzhong/LJSYLZS?fundCode=005911&indexcode=000300&type=m&callback=jQuery"

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Host': 'api.fund.eastmoney.com',
    'Referer': 'http://fund.eastmoney.com/005911.html'
}

req = urllib.request.Request(url,None,headers)
response = urllib.request.urlopen(req)
the_page = response.read()
print(the_page.decode("utf8"))