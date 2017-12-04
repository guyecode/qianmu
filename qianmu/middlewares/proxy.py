#coding:utf-8
import random
import logging
from urllib.request import _parse_proxy
from scrapy.exceptions import NotConfigured


logger = logging.getLogger()

def reform_proxy(url):
    proxy_type, user, password, hostport = _parse_proxy(url)
    return '%s://%s' % (proxy_type, hostport)

class RandomProxyMiddleware(object):

    def __init__(self, settings):
        self.proxies = settings.getlist('PROXIES')
        self.max_failed = settings.getint('PROXY_MAX_FAILED', 3)
        self.stats = {}.fromkeys(map(reform_proxy, self.proxies), 0)

    def random_proxy(self):
        return random.choice(self.proxies)

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('HTTPPROXY_ENABLED'):
            raise NotConfigured
        if not crawler.settings.getlist('PROXIES'):
            raise NotConfigured
        return cls(crawler.settings)

    def process_request(self, request, spider):
        if 'proxy' not in request.meta:
            request.meta['proxy'] = self.random_proxy()

    def process_response(self, request, response, spider):
        cur_proxy = request.meta['proxy']
        if response.status >= 400:
            self.stats[cur_proxy] += 1
        if self.stats[cur_proxy] > self.max_failed:
            for proxy in self.proxies:
                if cur_proxy.endswith(proxy.split('@')[-1]):
                    self.proxies.remove(proxy)
                    break
            logger.warn('proxy %s remove from proxies list' % cur_proxy)
        return response


