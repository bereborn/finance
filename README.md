#+title:
#+author:lizexin

* 概述
  目前爬取的网站有：

  + [[http://www.ygdy8.net/index.html][阳光电影]]

* 部署
  docker build -t finance .


** 部署爬虫
   目前部署在 10.10.136.6

** 执行爬虫
  docker run --rm -it -v /home/root1/lizexin/finance/finance:/usr/local/sandai/finance/ --name finance finance:latest
  cd /usr/local/sandai/finance/
  scrapy crawl finance


* 数据库
  | DB        | Table     | Note                                   |
  |-----------+-----------+----------------------------------------|
  | spider_db | resources | 记录了采集过的资源，用于采集的时候去重 |


* 数据库爬取记录输出日志
  



* 相关资料

** XPath
  | 表达式     | 描述      |
  |-----------+-----------|
  | /         | 从根节点选取 |
  | //        | 从匹配选择的当前节点选择文档中的节点, 而不考虑它们的位置 |
  | .         | 选取当前节点 |
  | ..        | 选取当前节点的父节点 |
  | @         | 选取属性 |
