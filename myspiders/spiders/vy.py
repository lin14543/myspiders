# -*- coding: utf-8 -*-
import scrapy, logging, time, json
from datetime import datetime
from myspiders import settings
from utils import dataUtil, pubUtil
from utils.spe_util import vyUtil
from jsonpath import jsonpath
from myspiders.items import MySpidersItem


class VySpider(scrapy.Spider):
    name = 'vy'
    allowed_domains = ['vueling.com']
    start_url = 'https://apimobile.vueling.com/Vueling.Mobile.AvailabilityService.WebAPI/api/AvailabilityController/DoAirPriceSB'
    carrier = 'VY'
    isOK = True
    cookie = ''
    cookies = [
        'sto-id-47873-%3FFE-PRO%3Fmaqueta-waf-mobile-443=ADBEKIMALLAB; ak_bmsc=971CA00C1B3C0EE405820C1BD70EC3ABDF77F85D1E2F0000C556075B7D87485C~plp0RWi2rN+sNIkga3IY591kobvkfBH2JJPnGS12ucAudZZGhb7lneTvmBzgeizzjeyVzDvIR9aMqVYO+wzQrIQcDfLCHQ8ZDgnHRt+Gxc9kvcEYJTz6f+Cn8PP5ZTaXDO7qQA6FRPjLh76uKAOLrNgkPMQ1D1MaIa+iDwLo8jHxAAXS0U8RAWe1w3bY6X4NIoO1RlSuRFLoZqdkjc5UZiP8QapVS3SyLqAMPJeL3yB1w=',
        'sto-id-47873-%3FFE-PRO%3Fmaqueta-waf-mobile-443=ACBEKIMALLAB; ak_bmsc=D46CD922B8008E17B75EB4DFC6479A06B8325774A616000086310E5BA08FC12E~plInDegCfE0SBXDYY1yL7wkXEU6qCOtq4dxVXG9rAW+Wuk8Gmb0pejgeni0HRTOin10bIi3o7H7hXLDyq0a9IBlxy6u3afgH6r+ftXxb8G1zVUV1lVGDiN08LnpjDUW37f1hwyXlKm5k5asitnh+n2dNyU/LZOigR/q9WbDOdNBzIyTTSNOArwvagkZVIcXX+N1hU6j+lC2pOnjA4FDOAlUaTykukAxIURCH9LFyWcg+I=',
        'sto-id-47873-%3FFE-PRO%3Fmaqueta-waf-mobile-443=ACBEKIMALLAB; ak_bmsc=523E87D358BC4F53525FC0D12416D9CEB8325774A6160000B4F80D5BDA868302~plN2M/xIrHbeMymLfw2YU5nk0gkLLblR6RLUDOAK5b1hPsOxIPJ8RgGHNHLuWqvai/RcvJoO0GlVVOn2I47aAwMFPkp1uqoP6uIdO5ROcxD+LLHklcpJrsYDw7ie02ynE4k46zbniLp7Sohb+In8zpTA4pPnkCUY68e4JNV88llQsMEgvTtwIueFoEffuH7mHTuAwjlD0pVv4+LL1LTI39SaYqX80XJsk2C7H2d0QmKBA='
    ]
    InstallationID = [
        '9AC6A648-98AE-4875-8451-DA948F84D777',
        'DBB3A54A-8132-4B1B-A28A-B360335B4820',
        '3BAE1C15-5389-44C6-955C-D04B3BABEF03'
    ]

    custom_settings = dict(
        DEFAULT_REQUEST_HEADERS={
            'Host': 'apimobile.vueling.com',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Accept-Language': 'en-us',
            'User-Agent': 'Vueling/881 CFNetwork/811.5.4 Darwin/16.7.0',
            # 'Cookie': ''
        },
        DEFAULT_DATA={
            "DiscountType": 0,
            "AppVersion": "892",
            "DeviceModel": "iPhone 6P",
            "CurrencyCode": "EUR",
            "TimeZone": 8,
            "Language": "EN",
            "Xid": "",
            # "InstallationID": "",
            "Paxs": [{
                "Paxtype": "ADT",
                "Quantity": 3
            }, {
                "Paxtype": "CHD",
                "Quantity": 0
            }, {
                "Paxtype": "INF",
                "Quantity": 0
            }],
            # 'AirportDateTimeList': [ # 如果要单独抓取某个航线，可修改以下内容并去掉注释即可
            #     {
            #         'MarketDateDeparture': '2018-04-23T00:00:00',
            #         'DepartureStation': 'BCN',
            #         'ArrivalStation': 'FCO',
            #     }
            # ],
            "OsVersion": "10.3.3",
            "Currency": "EUR",
            "DeviceType": "IOS",
        },

        DOWNLOAD_TIMEOUT=20,

        CLOSESPIDER_TIMEOUT=60 * 60 * 2,
        COOKIES_ENABLED=True,
        CONCURRENT_REQUESTS=4,

        # ITEM_PIPELINES={ # 往测试库添加数据
        #     'lmd_spiders.pipelines.LmdSpidersPipelineTest': 300,
        # },
    )

    def start_requests(self):
        while True:
            result = pubUtil.getUrl(self.carrier, 1)
            if not result:
                logging.info('get task error')
                time.sleep(10)
                continue

            hour = datetime.now().hour + 2
            self.cookie = self.cookies[hour % len(self.cookies)]
            installid = self.InstallationID[hour % len(self.InstallationID)]

            for data in result:
                (dt_st, dep, to, days) = vyUtil.analysisData(data)  # 把获取到的data格式化
                for i in range(int(days)):
                    dt = vyUtil.get_real_date(dt_st, i)
                    dt = dt + 'T00:00:00'
                    data_list = {
                        'InstallationID': installid,
                        'AirportDateTimeList': [
                            {
                                'MarketDateDeparture': dt,
                                'DepartureStation': dep,
                                'ArrivalStation': to,
                            }
                        ]
                    }

                    data_list.update(self.custom_settings.get('DEFAULT_DATA'))
                    yield scrapy.Request(method='POST',
                                         url=self.start_url,
                                         headers={'Cookie': self.cookie},
                                         body=json.dumps(data_list),
                                         meta={'data_list': data_list},
                                         callback=self.parse,
                                         dont_filter=True,
                                         errback=lambda x: self.download_errback(x, data_list))

    def download_errback(self, x, data):
        logging.info('error download:' + 'pls change ip')
        self.isOK = False
        yield scrapy.Request(method='POST',
                             url=self.start_url,
                             headers={'Cookie': self.cookie},
                             body=json.dumps(data),
                             callback=self.parse,
                             meta={'data_list': data},
                             dont_filter=True,
                             errback=lambda x: self.download_errback(x, data))

    def parse(self, response):
        response_dict = None
        try:
            response_dict = json.loads(response.body)
            journeys = jsonpath(response_dict, '$..Journeys')[0]
        except:
            if response.body.lower().find('<title>access denied</title>') != -1:
                logging.info('access denied!!!')
                self.isOK = False
            else:
                logging.info(response.body)
                return
            data_list = response.meta['data_list']
            yield scrapy.Request(method='POST',
                                 url=self.start_url,
                                 headers={'Cookie': self.cookie},
                                 body=json.dumps(data_list),
                                 meta={'data_list': data_list},
                                 callback=self.parse,
                                 dont_filter=True,
                                 errback=lambda x: self.download_errback(x, data_list))
            return
        self.isOK = True
        for journey in journeys:
            segments = journey.get('Segments')
            if len(segments) > 1:
                continue

            dep = journey.get('DepartureStation')
            arr = journey.get('ArrivalStation')
            dep_time = vyUtil.date_to_stamp(journey.get("STD"))
            arr_time = vyUtil.date_to_stamp(journey.get("STA"))

            fares = journey.get('JourneyFare')
            col_flag = len(fares)
            index_flag = -1
            for i in range(len(fares)):  # 找出最低价且有票的舱位
                fare = fares[i]
                if fare.get('IsFareAvailable') and fare.get('ColumnId') < col_flag:
                    seats = fare.get('AvailableCount')
                    if not seats or seats >= 3:
                        col_flag = fare.get('ColumnId')
                        index_flag = i
            if index_flag == -1:
                continue
            fare = fares[index_flag]
            seats = 9 if not seats else seats
            currency = fare.get('CurrencyCode')
            cabin = fare.get('ProductClass')
            price = fare.get('Amount')

            seg = segments[0]
            carrier = seg.get('CarrierCode')
            flightNumber = carrier + seg.get('FlightNumber')

            segment = {}
            segment['flightNumber'] = flightNumber
            segment['aircraftType'] = ""
            segment['number'] = 1
            segment['dep'] = seg.get("DepartureStation")
            segment['dest'] = seg.get("ArrivalStation")
            segment['airline'] = seg.get("OperatedBy")
            segment['duration'] = vyUtil.format_duration(seg.get("Duration"))
            segment['departureTime'] = seg.get('STD').replace('T', ' ')
            segment['destinationTime'] = seg.get('STA').replace('T', ' ')
            segment['seats'] = seats
            segment['depTerminal'] = ''

            item = MySpidersItem()
            item['maxSeats'] = seats
            item['flightNumber'] = flightNumber
            item['depTime'] = dep_time
            item['arrTime'] = arr_time
            item['depAirport'] = dep
            item['arrAirport'] = arr
            item['currency'] = currency
            item['cabin'] = cabin
            item['adultTax'] = 0
            item['carrier'] = carrier
            item['segments'] = json.dumps([segment])
            item['isChange'] = 1
            item['getTime'] = time.time()
            item['adultPrice'] = price
            item['netFare'] = price
            yield item
