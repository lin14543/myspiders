# -*- coding: utf-8 -*-
import scrapy, time, urllib, logging, json
from utils import dataUtil, pubUtil
from myspiders.items import MySpidersItem

class BeSpider(scrapy.Spider):
    name = 'be'
    allowed_domains = ["flybe.com"]
    isOK = True
    start_urls = "https://www.flybe.com/api/fares/day/new/"
    carrier = 'BE'
    custom_settings = dict(
        CONCURRENT_REQUESTS=8,
        # 请求等待时间
        DOWNLOAD_TIMEOUT=10,
        # 请求延迟
        DOWNLOAD_DELAY=0.5,
        # LOG_LEVEL='DEBUG',

        # 设置请求头
        DEFAULT_REQUEST_HEADERS={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
            'referer': 'https://www.flybe.com/web-app/index.html'
        }
    )

    def start_requests(self):
        while True:
            result = pubUtil.getUrl('BE', 10)
            if not result:
                logging.info('no task! sleep 10s...')
                time.sleep(10)
                continue
            for data in result:
                (dt, dep, to) = pubUtil.analysisData(data)  # 把获取到的data格式化
                if pubUtil.dateIsInvalid(dt):
                    continue
                temp = {
                    'depart': dep,
                    'arr': to,
                    'departing': dt,
                    'returning': '',
                    'promo-code': '',
                    'adults': 1,
                    'teens': 0,
                    'children': 0,
                    'infants': 0
                }
                try:
                    params = urllib.parse.urlencode(temp)
                except:
                    params = urllib.urlencode(temp)

                url = '%s%s/%s?%s' % (self.start_urls, dep, to, params)
                yield scrapy.Request(url, callback=self.parse, dont_filter=True,
                                     errback=lambda x: self.download_errback(x, url))

    def download_errback(self, x, url):
        self.isOK = False

    def parse(self, response):
        try:
            content = json.loads(response.text)
        except:
            self.isOK = False
            logging.info('change IP....')
            return
        if 'inbound' in content.keys():
            return
        self.isOK = True
        li = content['outbound']
        for i in range(len(li)):
            outbound = li[i]
            item = MySpidersItem()
            if outbound['totalHighestAdultGrossFare'] == 0:  # 该航班机票已售空
                continue
            if 'low' not in outbound.keys():  # 依次查找此时的最低票价
                if 'medium' not in outbound.keys() or outbound['medium']['flights'][0]['isEligible'] is False:
                    low = outbound['high']
                else:
                    low = outbound['medium']
            else:
                low = outbound['low']

            flights = low['flights']
            departTime = outbound['departDate'][:10] + ' ' + outbound['departureTime'] + ':00'
            ti = time.mktime(time.strptime(departTime, '%Y-%m-%d %H:%M:%S'))
            row = {}
            row['depTime'] = ti
            destTime = outbound['arriveDate'][:10] + ' ' + outbound['destinationTime'] + ':00'
            ti = time.mktime(time.strptime(destTime, '%Y-%m-%d %H:%M:%S'))
            row['arrTime'] = ti
            row['depAirport'] = outbound['depart']
            row['arrAirport'] = outbound['dest']
            row['currency'] = outbound['currency']
            row['adultPrice'] = float(low['totalAdultGrossFare'])
            row['adultTax'] = float(low['totalAdultTaxes'])
            row['netFare'] = float(low['totalAdultNetFare'])
            num = outbound['flightCount']
            segments = []
            if num > 1:  # 判断是否有中转
                continue
            else:
                segments.append(self.analysisSegment(flights[0].copy()))
                row['maxSeats'] = flights[0]['seatsAvailable']
                row['cabin'] = flights[0]['fare']['fareClass']
                row['carrier'] = flights[0]['flightNumber'][:2]
                row['flightNumber'] = flights[0]['flightNumber']
                row['isChange'] = 1
            row['segments'] = json.dumps(segments)
            row['getTime'] = time.time()
            item.update(row)
            yield item

    def analysisSegment(self, content):
        content.pop('isAlwaysDisplay')
        content.pop('fare')
        content.pop('tripId')
        content.pop('maxSeats')
        content.pop('ruleCode')
        content['departureTime'] = content['departDate'][:10] + ' ' + content['departureTime'] + ':00'
        content['destinationTime'] = content['arriveDate'][:10] + ' ' + content['destinationTime'] + ':00'
        content['seats'] = content['seatsAvailable']
        content['number'] = content['sectorSequence']
        content['duration'] = ""
        content['depTerminal'] = ""
        content.pop('sectorSequence')
        content.pop('departDate')
        content.pop('arriveDate')
        content.pop('seatsAvailable')
        return content
