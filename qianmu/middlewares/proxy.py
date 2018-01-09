#coding:utf-8
import random
import logging
from urllib.request import _parse_proxy
from scrapy.exceptions import NotConfigured


logger = logging.getLogger()

def reform_url(url):
    # 将url解开成不同的部分
    proxy_type, *_, hostport = _parse_proxy(url)
    # 将代理URL重新组合，去掉用户名密码
    return '%s://%s' % (proxy_type, hostport)

class RandomProxyMiddleware(object):

    def __init__(self, settings):
        # 从配置中读取配置到代理池中
        self.proxies = settings.getlist('PROXIES')
        # 从配置中读取最大失败次数配置
        self.max_failed = settings.getint('PROXY_MAX_FAILED', 3)
        # 创建一个字典，用来保存所有代理的失败次数，并将初始值设为0
        self.stats = {}.fromkeys(map(reform_url, self.proxies), 0)

    def random_proxy(self):
        # 从代理池中随机选择一个
        return random.choice(self.proxies)

    @classmethod
    def from_crawler(cls, crawler):
        # 判断配置中是否打开了代理
        if not crawler.settings.getbool('HTTPPROXY_ENABLED'):
            raise NotConfigured
        # 判断是否有PROXIES这项配置
        if not crawler.settings.getlist('PROXIES'):
            raise NotConfigured
        # 创建并返回一个中间件对象
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # 如果request.meta中没有设置proxy，则在proxies中随机设置一个proxy
        if 'proxy' not in request.meta:
            request.meta['proxy'] = self.random_proxy()

    def process_response(self, request, response, spider):
        # 本次请求使用的代理
        cur_proxy = request.meta['proxy']
        # 判断如果本次请求的status是400以上，则将本次使用的代理失败次数+1
        if response.status >= 400:
            self.stats[cur_proxy] += 1
        # 如果失败次数超过了最大失败次数，则将该代理从代理池中删除
        if self.stats[cur_proxy] > self.max_failed:
            for proxy in self.proxies:
                if reform_url(proxy) == cur_proxy:
                    self.proxies.remove(proxy)
                    break
            logger.warn('proxy %s remove from proxies list' % cur_proxy)
        # 返回response对象以便后续的中间件继续执行
        return response


