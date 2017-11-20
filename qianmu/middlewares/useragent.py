# -*- coding: utf-8 -*-
import faker

class RandomUserAgentMiddleware(object):
    """该中间件负责给每个请求随机分配user agent"""

    def __init__(self, settings):
        self.faker = faker.Faker()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.faker.user_agent()