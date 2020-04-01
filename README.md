# PostgraduateSpider
研招网考研-初试科目信息爬虫

设置要爬取得信息：

修改<code>MasterMajor/spiders/majorSpider.py</code>中<cde>MajorSpider</code>类的<code>base_data</code>属性

属性值从 https://yz.chsi.com.cn/zsml/queryAction.do 的页面源码中获取

启动爬虫：

>scrapy crawl 爬虫名

>scrapy crawl 爬虫名 -o 输出文件名.json

例如，输出到csv文件：

>scrapy crawl majorSpider -s LOG_FILE=all.log -s FEED_EXPORT_ENCODING=UTF-8 -o exam.csv
