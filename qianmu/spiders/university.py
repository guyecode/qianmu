# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from w3lib.html import remove_tags
from qianmu.items import UniversityItem

def filter(html):
    """过滤网页源码中的特殊符号和sup标签"""
    return remove_tags(html, which_ones=('sup',)).replace('\n', '')\
    .replace('\r', '').replace('\t', '')


class UniversitySpider(scrapy.Spider):
    name = 'university'
    # 定义允许访问的域名列表，任何不符合以下域名的链接都不会被下载
    allowed_domains = ['qianmu.iguye.com']
    # 入口页面的URL
    start_urls = ['http://qianmu.iguye.com/2018USNEWS世界大学排名']

    def __init__(self, max_num=0, *args, **kwargs):
        # 重载父类的构造函数，先调用父类的构造函数
        super(UniversitySpider, self).__init__(*args, **kwargs)
        # 然后执行自己的操作， 设置自定义传入的参数
        self.max_num = int(max_num)

    def parse(self, response):
        # 选择出排名表格里第2行开始的所有行的第2列里的超链接，也就是所有大学的链接
        links = response.xpath("//div[@id='content']//tr[position()>1]/td[2]/a/@href").extract()
        # 循环这些链接，同时使用enumerate函数，列出每一个链接在列表中的索引
        for i, link in enumerate(links):
            # 根据自定义的参数判断，如果抓取的链接数量超过max_num，则不再抓取
            if self.max_num and i >= self.max_num:
                break
            # 有个别坏掉的链接，加一下判断
            if not link.startswith('http://'):
                link = 'http://qianmu.iguye.com/%s' % link
            # 创建一个request对象，并将parse_university设置为它的回调函数
            request = Request(link, callback=self.parse_university)
            # 使用meta属性在函数之间传递参数
            request.meta['rank'] = i + 1
            yield request

    def parse_university(self, response):
        # 使用filter函数过滤网页中的特殊符号，因为response的属性是只读的，所以我们使用replace方法来重新生成一个response对象
        response = response.replace(body=filter(response.body))
        # 选择出父节点，缩减xpath表达式的重复编码
        wiki_content = response.xpath('//div[@id="wikiContent"]')[0]
        # 定义一个Item对象，并设置name,rank的值
        item = UniversityItem(
            name=wiki_content.xpath('./h1[@class="wikiTitle"]/text()').get(),
            rank=response.meta['rank'])
        # 取出表格中左列的文本
        keys = wiki_content.xpath('./div[@class="infobox"]/table//tr/td[1]/p/text()').extract()
        # 取出表格中右列单元格节点list
        cols = wiki_content.xpath('./div[@class="infobox"]/table//tr/td[2]')
        # 循环上步得到的单元格节点list，并取出每个单元格中的文本，这样做是为了解决有些单元格存在多个p标签的问题
        values = [','.join(col.xpath('.//text()').extract()) for col in cols]
        # 将左、右单元格组成一个字典
        data = dict(zip(keys, values))
        # 从字典中的值设置到item相应的属性中
        item['country'] = data.get(u'国家', '')
        item['state'] = data.get(u'州省', '')
        item['city'] = data.get(u'城市', '')
        item['undergraduate_num'] = data.get(u'本科生人数', '')
        item['postgraduate_num'] = data.get(u'研究生人数', '')
        item['website'] = data.get(u'网址', '')
        # 使用内置logger对象记录日志
        self.logger.info(u'%s scraped' % item['name'])
        yield item
