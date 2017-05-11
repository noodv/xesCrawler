# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider
from xes.items import XesItem

class XesspiderSpider(CrawlSpider):
    name = 'xes'
    allowed_domains = ['www.xueersi.com']
    start_urls = ['http://www.xueersi.com/findcourse/']

    def parse(self, response):
        course_urls =response.xpath('//div[@class="list-course-dd"]/span/a/@href').extract()


        spical_course_urls =['http://www.xueersi.com/chuzhong-shuxue-5/','http://www.xueersi.com/chuzhong-wuli-5/',
     'http://www.xueersi.com/chuzhong-huaxue-5/','http://www.xueersi.com/gaozhong-yingyu-5/','http://www.xueersi.com/xiaodi-shuxue-5/','http://www.xueersi.com/xiaodi-yingyu-5/']

        fanye_urls= [ "http://www.xueersi.com/xiaodi-0-2/","http://www.xueersi.com/xiaogao-0-2/","http://www.xueersi.com/chuzhong-0-2/","http://www.xueersi.com/gaozhong-0-2/"  ]

        course_urls.extend(spical_course_urls)

        for course in course_urls:

            yield scrapy.Request(url=course, callback=self.get_season_entry)

        for course in fanye_urls:
            yield scrapy.Request(url=course,callback=self.get_fanye_course)

    #入口
    def get_season_entry(self,response):

        for season in response.xpath('//div[@class="select-class-course"]/ul/li[@class !="disable-class"]/a/@href').extract():
            yield scrapy.Request(url=season,callback=self.get_province_entry)

    def get_province_entry(self,response):
        for province in response.xpath('//ul[@class="select-list"]/li/a/@href').extract():
            yield scrapy.Request(url=province,callback=self.get_course)


    #抓取明细
    def get_fanye_course(self, response):
        item =XesItem()
        html = response.body.decode()
        prefix_url = re.search("http://www.xueersi.com/.*?-0-2",response.url).group(0)
        all_num = int(re.search("total: (.*?), // 总记录数", html).group(1))
        cur_page = int(re.search("index: (.*?), // 当前页", html).group(1))
        print(all_num,cur_page)
        if all_num > cur_page *30:
            yield scrapy.Request(url="{}-0-0-0-0-0-0-0-0-0-0-1-{}".format(prefix_url,cur_page +1),callback=self.get_fanye_course)
        item['grade'] = response.xpath('//*[@id="module-breadcrumb"]/li/text()').extract_first()
        for ele in response.xpath('.//div[@class="course-list course-test course-test-select"]'):
            item["ID"] = ele.xpath(".//a[@class='title-detail']/@href").re("http://www.xueersi.com/kc/(.*?)\.html")[0]
            item["subject"] =ele.xpath('.//label[@class="course-label course-yellow-label"]/text()').extract_first()
            item["live"] =ele.xpath('.//label[@class="course-label course-green-label"]/text()').extract_first()
            item['title'] =ele.xpath(".//a[@class='title-detail']/text()").extract_first()
            item['price'] =ele.xpath(".//span[@class='money']/text()").extract_first().strip()
            try:
                item["teacher"] =ele.xpath('.//div[@class="course-detail-info"]/a/text()').extract_first()
            except:
                item["teacher"] =""
            desc =ele.xpath(".//p[@class='tip-for']/text()").extract_first()
            item['desc'] =desc.strip()
            yield item

    def get_course(self,response):
        item = XesItem()
        item['grade'] = response.xpath('//*[@id="module-breadcrumb"]/a[1]/text()').extract_first()[1:]
        item['subject'] = response.xpath('//*[@id="module-breadcrumb"]/a[2]/text()').extract_first()[1:]
        for ele in response.xpath("//div[@class='live-course-rank-list']"):
            item["ID"] = ele.xpath(".//a[@title]/@href").re("http://www.xueersi.com/kc/(.*?)\.html")[0]
            item['title'] = ele.xpath(".//p[@class='difficulty']/a/text()").extract_first().strip()
            try:
                item["day_time"] =ele.xpath('.//span[@class="every-time"]/a/text()').extract_first().strip()
            except:
                item["day_time"] =""
            try:
                time_info_list = ele.xpath(".//span[@class='every-day']/a/text()").extract_first().strip().split("-")
                item["begin_time"] =time_info_list[0]
                item['end_time'] =time_info_list[1]
            except:
                item["begin_time"] = ""
                item['end_time'] = ""
            item['teacher'] =ele.xpath(".//div[@class='rank-coach']/span/a/text()").extract_first()
            item['assistant_teacher'] =ele.xpath(".//em[@class='ui-userinfo']/text()").extract_first()
            item['rank_places'] =ele.xpath(".//div[@class='rank-places']/strong/text()").extract_first()
            item['price'] =ele.xpath(".//div[@class='rank-money']/strong/text()").extract_first().strip()
            try:
                item['target'] =ele.xpath(".//span[@class='satisfy']/text()").extract_first().strip()
            except:
                item['target'] =""
            item['live'] = "直播"
            if ele.xpath(".//div[@class='quota-full']").extract():
                item['available'] =False
            else:
                item['available'] =True

            yield item






