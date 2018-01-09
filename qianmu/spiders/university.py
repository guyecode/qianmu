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
    allowed_domains = ['qianmu.iguye.com']
    start_urls = ['http://qianmu.iguye.com/2018USNEWS世界大学排名']

    def __init__(self, max_num=0, *args, **kwargs):
        super(UniversitySpider, self).__init__(*args, **kwargs)
        self.max_num = int(max_num)

    def parse(self, response):
        links = response.xpath("//div[@id='content']//tr[position()>1]/td[2]/a/@href").extract()
        for i, link in enumerate(links):
            if self.max_num and i >= self.max_num:
                break
            if not link.startswith('http://'):
                link = 'http://qianmu.iguye.com/%s' % link
            request = Request(link, callback=self.parse_university)
            request.meta['rank'] = i + 1
            yield request

    def parse_university(self, response):
        response = response.replace(body=filter(response.body))
        wiki_content = response.xpath('//div[@id="wikiContent"]')[0]
        item = UniversityItem(
            name=wiki_content.xpath('./h1[@class="wikiTitle"]/text()').get(),
            rank=response.meta['rank'])
        keys = wiki_content.xpath('./div[@class="infobox"]/table//tr/td[1]/p/text()').extract()
        cols = wiki_content.xpath('./div[@class="infobox"]/table//tr/td[2]')
        values = [','.join(col.xpath('.//text()').extract()) for col in cols]
        data = dict(zip(keys, values))
        item['country'] = data.get(u'国家', '')
        item['state'] = data.get(u'州省', '')
        item['city'] = data.get(u'城市', '')
        item['undergraduate_num'] = data.get(u'本科生人数', '')
        item['postgraduate_num'] = data.get(u'研究生人数', '')
        item['website'] = data.get(u'网址', '')
        self.logger.info(u'%s scraped' % item['name'])
        yield item
