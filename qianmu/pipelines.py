# -*- coding: utf-8 -*-

import json
import pymysql
import pymysql.cursors
import logging
import redis
from twisted.enterprise import adbapi
from scrapy.exceptions import DropItem


logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class CheckPipeline(object):
    """CheckPipeline验证每个item的关键属性是否为空"""

    def open_spider(self, spider):
        """当spider被开启时，这个方法被调用"""
        logger.info('spider %s opened' % spider.name)

    def close_spider(self, spider):
        """当spider被关闭时，这个方法被调用"""
        logger.info('spider %s closed' % spider.name)

    def process_item(self, item, spider):
        """每个item pipeline组件都需要调用该方法，这个方法必须返回一个 Item (或任何继承类)对象，
         或是抛出 DropItem 异常，被丢弃的item将不会被之后的pipeline组件所处理。
         @param item (Item 对象) – 被爬取的item
         @param spider (Spider 对象) – 爬取该item的spider
         """
        if not item.get('undergraduate_num'):
            # 如果缺失undergraduate_num属性，丢弃该item
            raise DropItem("Missing undergraduate in %s" % item['name'])
        if not item.get('postgraduate_num'):
            # 如果缺失undergraduate_num属性，丢弃该item
            raise DropItem("Missing postgraduate_num in %s" % item['name'])
        # 如果数据完整，返回item对象供之后的pipeline进行处理
        return item


class RedisPipeline(object):

    def __init__(self):
        self.r = redis.Redis()

    def process_item(self, item, spider):
        # 将爬取到的大学名字添加到redis的一个set中
        self.r.sadd(spider.name, item['name'])
        logger.info('redis: add %s to list %s' % (item['name'], spider.name))
        return item


class MysqlPipeline(object):

    def __init__(self):
        self.conn = None
        self.cur = None
    
    def open_spider(self, spider):
        # 初始化mysql连接
        self.conn = pymysql.connect(
            host='localhost', 
            port=3306, 
            user='root', 
            passwd='', 
            db='qianmu', 
            charset='utf8')
        # 初始化游标对象
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        # 将item重组成keys，values的形式，并一一对应
        cols, values = zip(*item.items())
        # 拼装SQL语句
        sql = "INSERT INTO `universities`(%s) VALUES (%s)" % \
              (','.join(cols), ','.join(['%s'] * len(cols)))
        # 执行并commit
        self.cur.execute(sql, values)
        self.conn.commit()
        # 打印出刚才执行的SQL语句
        logger.info(self.cur._last_executed)
        logger.info('mysql: add %s to universities' % item['name'])
        # 返回item以便后续的pipeline处理
        return item

    def close_spider(self, spider):
        """当spider被关闭时，这个方法被调用"""
        self.cur.close()
        self.conn.close()