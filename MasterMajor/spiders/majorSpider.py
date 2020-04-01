# -*- coding: utf-8 -*-
import scrapy
from MasterMajor.items import ExamItem
from urllib import parse


class MajorSpider(scrapy.Spider):
    name = 'majorSpider'
    base_url = 'https://yz.chsi.com.cn'
    start_urls = ['https://yz.chsi.com.cn/zsml/queryAction.do']
    base_data = {"ssdm": "", "dwmc": "", "mldm": "zyxw", "mlmc": "", "yjxkdm": "0854", "zymc": "电子信息", "xxfs": "1",
                 "pageno": '1'}

    # 请求学校第一页
    def start_requests(self):
        url = 'https://yz.chsi.com.cn/zsml/queryAction.do'
        data = self.base_data.copy()
        yield scrapy.FormRequest(url=url, formdata=data, callback=self.loopSchoolPage)

    # 请求学校列表
    def loopSchoolPage(self, response):
        pageno = 1
        page_count = int(response.xpath(
            "(((//div[@class='zsml-page-box']//i[@class='iconfont'])[2]/ancestor::li[contains(@class,'lip')])/preceding-sibling::*)[last()]//text()")
                         .extract_first().strip())
        while pageno <= page_count:
            data = self.base_data.copy()
            data['pageno'] = str(pageno)
            url = 'https://yz.chsi.com.cn/zsml/queryAction.do'
            # print(url+'?'+parse.urlencode(data))
            print("Current School List Page:", pageno, page_count)
            yield scrapy.FormRequest(url=url, formdata=data, callback=self.parseSchoolList)
            pageno += 1

    # 请求专业第一页
    def parseSchoolList(self, response):
        # print('parseSchoolList')
        for href in response.xpath("(//table[@class='ch-table']//a[@target='_blank'])/attribute::href").extract():
            url = self.base_url + href
            params = dict([(k, v[0]) for k, v in parse.parse_qs(parse.urlparse(url).query).items()])
            # print(url)
            yield scrapy.Request(url=url, callback=self.loopMajorPage, meta={"data": params})

    # 请求专业列表
    def loopMajorPage(self, response):
        # print('loopMajorPage')
        page_count = int(response.xpath(
            "(((//div[@class='zsml-page-box']//i[@class='iconfont'])[2]/ancestor::li[contains(@class,'lip')])/preceding-sibling::*)[last()]//text()")
                         .extract_first().strip())
        pageno = 1
        while pageno <= page_count:
            data = response.meta['data']
            data['pageno'] = str(pageno)
            url = 'https://yz.chsi.com.cn/zsml/querySchAction.do'
            # print(url + '?' + parse.urlencode(data))
            print("Current Major List Page:", pageno, page_count)
            yield scrapy.FormRequest(url=url, formdata=data, callback=self.majorPage)
            pageno += 1

    def majorPage(self, response):
        # print('majorPage')
        for href in response.xpath("(//a[contains(.,'查看')])/@href").extract():
            url = self.base_url + href
            # print(url)
            yield scrapy.Request(url=url, callback=self.parseMajor)

    # 解析专业详情
    def parseMajor(self, response):
        # print('parseMajor')
        item = ExamItem()
        item['招生单位'] = response.xpath("(//td[@class='zsml-summary'])[1]/text()").extract_first()
        item['院系所'] = response.xpath("(//td[@class='zsml-summary'])[3]/text()").extract_first()
        item['专业'] = response.xpath("(//td[@class='zsml-summary'])[5]/text()").extract_first()
        item['研究方向'] = response.xpath("(//td[@class='zsml-summary'])[7]/text()").extract_first()
        item['拟招人数'] = response.xpath("(//td[@class='zsml-summary'])[9]/text()").extract_first()
        item['考试方式'] = response.xpath("(//td[@class='zsml-summary'])[2]/text()").extract_first()
        item['跨专业'] = response.xpath("(//td[@class='zsml-summary'])[4]/a/text()").extract_first()
        item['学习方式'] = response.xpath("(//td[@class='zsml-summary'])[6]/text()").extract_first()
        item['指导老师'] = response.xpath("(//td[@class='zsml-summary'])[8]/text()").extract_first()
        for tr in response.xpath("(//tbody[@class='zsml-res-items']//tr)"):
            exam = item.copy()
            exam['政治'] = tr.xpath("td[1]/text()").extract_first().strip()
            exam['外语'] = tr.xpath("td[2]/text()").extract_first().strip()
            exam['业务课一'] = tr.xpath("td[3]/text()").extract_first().strip()
            exam['业务课二'] = tr.xpath("td[4]/text()").extract_first().strip()
            # print(exam)
            yield exam
