import datetime
import json
import re

import scrapy

from party_scraper import items

DATE_TODAY = str(datetime.date.today())


class VirtualNightsSpider(scrapy.Spider):
    name = "virtualnights"

    def start_requests(self):
        urls = [
            'https://www.virtualnights.com/muenster/events/{}'.format(
                DATE_TODAY),
            # 'https://www.virtualnights.com/muenster/events/2019-09-27',
            # 'https://www.virtualnights.com/muenster/events/2019-09-28',
            # 'https://www.virtualnights.com/muenster/events/2019-09-29',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def _parse_details(self, response):
        event = response.meta['event']
        description = response.selector.xpath(
            '//div[@class="event-description"]/text()').get()
        description = description.strip()
        event['description'] = re.sub(' +', ' ', description)
        return event


    def _parse_article(self, article_selector):
        for span in article_selector.xpath('descendant::span/text()').getall():
            if span == 'Münster':
                event = items.PartyItem()

                event['start_date'] = article_selector.xpath(
                    'header/a/time/@datetime').get()

                event['title'] = article_selector.xpath(
                    'header/a/h2/text()').get()

                event['location_name'] = article_selector.xpath(
                    'p[@itemprop="location"]/a/span[@itemprop="name"]/text()').get()

                city = article_selector.xpath(
                    'p[@itemprop="location"]/a/span[@itemprop="address"]/span[@itemprop="addressLocality"]/text()').get()

                address = article_selector.xpath(
                    'p[@itemprop="location"]/a/span[@itemprop="address"]/span[@itemprop="streetAddress"]/text()').get()

                city_zip = article_selector.xpath(
                    'p[@itemprop="location"]/a/span[@itemprop="address"]/meta[@itemprop="postalCode"]/@content').get()

                event['location_address'] = '{}, {} {}'.format(address, city_zip, city)

                event['link'] = 'https://www.virtualnights.com{}'.format(
                    article_selector.xpath('header/a/@href').get())

                geo_lon = article_selector.xpath(
                    'p[@itemprop="location"]/span[@itemtype="http://schema.org/GeoCoordinates"]/meta[@itemprop="longitude"]/@content').get()
                geo_lat = article_selector.xpath(
                    'p[@itemprop="location"]/span[@itemtype="http://schema.org/GeoCoordinates"]/meta[@itemprop="latitude"]/@content').get()

                event['geo'] = {'lat': geo_lat, 'lon': geo_lon}
                event['category'] = 'Party'
                event['source'] = 'virtualnights.com'

                img = (article_selector.xpath('div/span/img/@src').get()
                    if article_selector.xpath('div/span/img/@src').get()
                    else article_selector.xpath('div/span/img/@data-src').get())

                event['images'] = [{'image_url': img}]

                request = scrapy.Request(
                    url=event['link'], callback=self._parse_details,
                    meta={'event': event})

                return request

    def parse(self, response):
        articles = response.selector.xpath('//article')

        for a in articles:
            for span in a.xpath('descendant::span/text()').getall():
                if span == 'Münster':
                    yield self._parse_article(a)