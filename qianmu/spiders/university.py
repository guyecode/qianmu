# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from w3lib.html import remove_tags


def filter(html):
    """过滤网页源码中的特殊符号和sup标签"""
    return remove_tags(html, which_ones=('sup',)).replace('\n', '')\
    .replace('\r', '').replace('\t', '')


class UniversitySpider(scrapy.Spider):
    name = 'university'
    allowed_domains = ['140.143.192.76']
    start_urls = ['http://140.143.192.76:8002/2018USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D']

    def __init__(self, max_num=0, *args, **kwargs):
        super(UniversitySpider, self).__init__(*args, **kwargs)
        self.max_num = int(max_num)

    def parse(self, response):
        links = response.xpath("//div[@id='content']//tr[position()>1]/td[2]/a/@href").extract()
        for i, link in enumerate(links):
            if self.max_num and i >= self.max_num:
                break
            if not link.startswith('http://'):
                link = 'http://140.143.192.76:8002/%s' % link
            request = Request(link, callback=self.parse_university)
            request.meta['rank'] = i + 1
            yield request

    def parse_university(self, response):
        response = response.replace(body=filter(response.body))
        wiki_content = response.xpath('//div[@id="wikiContent"]')[0]
        item = dict(
            title=wiki_content.xpath('./h1[@class="wikiTitle"]/text()').extract_first(),
            rank=response.meta['rank'])
        keys = wiki_content.xpath('./div[@class="infobox"]/table//tr/td[1]/p/text()').extract()
        cols = wiki_content.xpath('./div[@class="infobox"]/table//tr/td[2]')
        values = [','.join(col.xpath('.//text()').extract()) for col in cols]
        item.update(zip(keys, values))
        self.logger.info(u'%s scraped' % item['title'])
        yield item
