# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


def convert_int(s):
    if isinstance(s, int):
        return s
    if not s:
        return 0
    return int(s.strip().replace(',', ''))


class UniversityItem(scrapy.Item):

    name = scrapy.Field()
    rank = scrapy.Field(serializer=convert_int)
    country = scrapy.Field()
    state = scrapy.Field()
    city = scrapy.Field()
    undergraduate_num = scrapy.Field()
    postgraduate_num = scrapy.Field()
    website = scrapy.Field()


if __name__ == '__main__':
    u = UniversityItem(name='哈佛大学', rank=1)
    u['country'] = '美国'
    u['state'] = '马萨诸塞州'
    print(u)
    print(u['name'])

    # 将会打印出['country', 'state', 'name']，不包含未设置值的字段
    print(u.keys())
    # 打印出所有定义过的字段名称
    print(u.fields.keys())
    # 打印出所有的fields及其序列化函数
    print(u.fields)
    # 判断某个item对象是否包含指定字段
    print('undergraduate_num' in u.fields)
    # 判断某个字段是否设置了值
    print('name' in u)
    print('undergraduate_num' in u)

    # 复制另外一个Item对象的值
    u2 = UniversityItem(u)
    u2['undergraduate_num'] = 2345
    print(u2)
    print(u)

    # 将Item对象转换为字典对象
    u_dict = dict(u)
    print(type(u_dict))
    # 从一个字典对象中创建item对象
    u3 = UniversityItem(u_dict)
    print(u3)

    # 如果设置一个未定义的字段，则会抛出KeyError异常
    u4 = UniversityItem({'unknow': 123})
