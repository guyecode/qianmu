#coding: utf-8
import sys
import json
import logging
import redis
from pipelines import MysqlPipeline

r = redis.Redis()
logging.basicConfig()
logger = logging.getLogger('pipelines')
logger.info('begin to process item...')


def get_item(spider):
    key = '%s:items' % spider
    item = r.blpop(key)
    if item:
        return json.loads(item[1])

    
if __name__ == '__main__':
    spider = sys.argv[1]
    db = MysqlPipeline()
    db.open_spider(spider)
    item = get_item(spider)
    while item:
        db.process_item(item, spider)
        item = get_item(spider)
    db.close_spider(spider)
