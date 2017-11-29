# 创建项目目录结构
scrapy startproject qianmu

cd qianmu

# 生成spider文件（注意，当前目录要在项目的根目录下）
# scrapy genspider <spider名字> <start_url>
scrapy genspider university 140.143.192.76:8002


# 使用scrapy配置下载目标页面，下载完成后在浏览器内打开
scrapy view http://140.143.192.76:8002/2018USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D

# 打印出settings文件指定配置的值，如果settings.py内没有指定，则打印出系统默认的值
scrapy settings --get=BOT_NAME

# 执行爬虫程序（参数为spider的名字）
scrapy crawl university

# 使用srapy下载器访问链接，并在控制台内输出页面源码
scrapy fetch http://140.143.192.76:8002/2018USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D

# 列出所有spider的名字
scrapy list

# 进入命令行模式
scrapy shell http://140.143.192.76:8002/2018USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D

# 使用spider的parse方法去处理链接的返回内容
scrapy parse http://140.143.192.76:8002/2018USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D



[s]   scrapy     scrapy模块
[s]   request    request对象，有headers，url等等属性
[s]   response   response对象，有xpath，方法，url、meta属性
[s]   settings   settings.py文件内的内容，以字幕形式保存
[s]   spider     spider对象,比如：UniversitySpider
[s] Useful shortcuts:
[s]   fetch(url[, redirect=True]) 抓取某个链接，并将response，request对象重置为当前爬取的结果
[s]   fetch(req)                  同上，但是以一个request对象作为参数
[s]   shelp()           打印可用的内置方法和变量。
[s]   view(response)    将当前的response的页面在浏览器内打开

