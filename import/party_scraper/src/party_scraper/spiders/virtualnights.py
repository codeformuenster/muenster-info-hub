import datetime
import json
import os
import re

import scrapy

from party_scraper import items


class VirtualNightsSpider(scrapy.Spider):
    """
    Scrape events for given dates from
    virtualnights.com/muenster/events.
    Scrape dates from SCRAPE_START to SCRAPE_END
    or today and next 6 days if no dates passed
    """

    name = "virtualnights"

    def start_requests(self):
        if ('SCRAPE_START' in os.environ and
            'SCRAPE_END' in os.environ):
            start = datetime.datetime.strptime(
                os.environ['SCRAPE_START'], '%Y-%m-%d')
            end = datetime.datetime.strptime(
                os.environ['SCRAPE_END'], '%Y-%m-%d')

            urls = ['https://www.virtualnights.com/muenster/events/{}'.format(
                d) for d in self._date_list(start, end)]
        else:  # if not start and end provided, scrape today and 6 next days
            start = datetime.datetime.today()
            end = start + datetime.timedelta(days=6)

            urls = ['https://www.virtualnights.com/muenster/events/{}'.format(
                d) for d in self._date_list(start, end)]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def _parse_details(self, response):
        event = response.meta['event']
        description = response.selector.xpath(
            '//div[@class="event-description"]/text()').get()
        description = description.strip()
        # TODO: fix AttributeError: 'NoneType' object has no attribute 'strip'

        event['description'] = re.sub(' +', ' ', description)
        return event


    def _parse_article(self, article_selector, response):
        for span in article_selector.xpath('descendant::span/text()').getall():
            if span == 'Münster':
                event = items.PartyItem()

                city = article_selector.xpath(
                    'p[@itemprop="location"]/a/span[@itemprop="address"]/span[@itemprop="addressLocality"]/text()').get()

                if city != 'Münster':  # cancel if event not in Muenster
                    return None

                event['start_date'] = article_selector.xpath(
                    'header/a/time/@datetime').get()

                event_day = datetime.datetime.strptime(
                    event['start_date'].split('T')[0], '%Y-%m-%d')

                # cancel if event is not at day of interest
                scrape_day = datetime.datetime.strptime(
                    response.request.url.rsplit('/', 1)[1], '%Y-%m-%d')

                if event_day != scrape_day:
                    return None

                event['title'] = article_selector.xpath(
                    'header/a/h2/text()').get()

                event['location_name'] = article_selector.xpath(
                    'p[@itemprop="location"]/a/span[@itemprop="name"]/text()').get()


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

    def _date_list(self, start_date, end_date):
        date_iter = start_date.date()
        dates = []

        while date_iter <= end_date.date():
            dates.append(date_iter.strftime('%Y-%m-%d'))
            date_iter += datetime.timedelta(days=1)
            date_iter = date_iter

        return dates

    def parse(self, response):
        articles = response.selector.xpath('//article')

        for a in articles:
            for span in a.xpath('descendant::span/text()').getall():
                if span == 'Münster':
                    yield self._parse_article(a, response)
