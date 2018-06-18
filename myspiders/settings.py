# -*- coding: utf-8 -*-

# Scrapy settings for myspiders project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'myspiders'

SPIDER_MODULES = ['myspiders.spiders']
NEWSPIDER_MODULE = 'myspiders.spiders'

DOWNLOADER_MIDDLEWARES = {
   'myspiders.middlewares.ProxyMiddleware': 543,
   # 'myspiders.middlewares.StatisticsItem': 400,
}

ITEM_PIPELINES = {
   'myspiders.pipelines.MyspidersPipeline': 300,
}

CARRIER_SITE = {
    'VY': 'http://www.vueling.com/es',
    'BE': 'https://www.flybe.com/',
}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'myspiders (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

#日志处理
LOG_LEVEL = 'INFO'
GET_URL_TIMEOUT = 60

# GET_TASK_URL = 'http://dx.redis.jiaoan100.com/buddha/gettask?'

GET_TASK_URL = 'http://127.0.0.1:5000/gettask?'

# LOG_URL = 'http://dx.jiaoan100.com/br/log?'
# GET_CITYPORTS_URL = 'http://dx.spider.jiaoan100.com/br/portcity?'

GET_PROXY_URL = 'http://dx.proxy.jiaoan100.com/proxy/getproxy?'

GET_CMD_URL = 'http://127.0.0.1:5000/getcmd?'
HEARTBEAT_URL = 'http://127.0.0.1:5000/heartbeat?'

MONITOR_DURATION = 5 * 60

DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_USER = 'root'
DB_PWD = 'lin'
DB_NAME = 'tickets'

# email util settings

SENDER = [
    '1697160859@qq.com',
    '765171067@qq.com',
    '815704044@qq.com',
]

HOST_RECEIVERS = ['lincc@lamudatech.com']

SPIDER_RECEIVERS = [
    'lincc@lamudatech.com',
    'xjb@lamudatech.com',
    'flymrc@qq.com',
 ]

HOST_SERVER = 'smtp.qq.com'

PWD = [ # qq邮箱第三方授权码
    'hhxbmixpdlpgchec',
    'mfeywdjmgvgobefi',
    'tdwssamzjgfpbcdj',
]


