import scrapy
import os
from party_scraper import items
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim


MONTH = {
    'Januar': 'January',
    'Februar': 'February',
    'März': 'March',
    'April': 'April',
    'Mai': 'May',
    'Juni': 'June',
    'Juli': 'July',
    'August': 'August',
    'September': 'September',
    'Oktober': 'October',
    'November': 'November',
    'Dezember': 'December'
}

def clean_date(str, inf='%Y-%m-%d', outf='%Y-%m-%d'):
    date = datetime.strptime(str, inf)
    news = datetime.strftime(date, outf)
    return news


class PartyPhaseSpider(scrapy.Spider):
    name = "partyphase"
    allowed_domains = ["muenster.partyphase.net"]
    geolocator = Nominatim(user_agent='muenster-info-hub')

    def start_requests(self):
        if ('SCRAPE_START' in os.environ and 'SCRAPE_END' in os.environ):
            start = clean_date(os.environ['SCRAPE_START'])
            end = clean_date(os.environ['SCRAPE_END'])
        else:
            start = datetime.strftime(datetime.today(), '%Y-%m-%d')
            end = datetime.strftime(datetime.today() + timedelta(days=6), '%Y-%m-%d')
        start_urls = [
            f'http://muenster.partyphase.net/veranstaltungskalender-muenster/?eme_scope_filter={start}--{end}&eme_submit_button=Submit&eme_eventAction=filter',
        ]

        self.log("------------ START PARAMETERS -------------- ")
        self.log(f"START: {start}")
        self.log(f"END: {end}")
        self.log("------------  ")

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        # split events
        raw = response.xpath('//div[@class="kalenderbreit"]')

        # get event URLs from overview
        A = raw.xpath('//div[@class="veranstaltungsname"]/a')
        event_urls = A.xpath('@href').getall()

        # crawl events
        for event_url in event_urls:
            yield scrapy.Request(
                event_url,
                callback=self._parse_event)

    def _get_location_address(self, url):
        response = scrapy.Request(url=url)
        add = response.xpath('//div[@class="entry-content"]/text()').getall()
        return f'{add[1].strip()} {add[2].strip()}'

    def _parse_event(self, response):
        event = items.PartyItem()

        event['title'] = response.xpath('//div/div[@class="eme_period"]/text()').get()

        wday, date, time = response.xpath('//div/div[@class="beginn"]/text()').get().split(' | ')
        mday, month, year = date.split(' ')
        start_date = f'{mday} {MONTH[month]} {year} {time}'
        start_date = datetime.strptime(start_date, '%d. %B %Y %H:%M Uhr').isoformat()
        event['start_date'] = f'{start_date}+02:00'

        event['location_name'] = response.xpath('//div/div[@class="ort"]/a/text()').get()
        event['link'] = response.url
        event['description'] = u' '.join([s.strip() for s in response.xpath('//div/p/text()').getall()])
        if any(tag in event['title'].lower() for tag in ['live', 'party', 'fest']):
            event['category'] = 'Party'
        event['source'] = 'muenster.partyphase.net'

        location_url = response.xpath('//div/div[@class="ort"]/a/@href').get()

        try:
            request = scrapy.Request(url=location_url, callback=self._parse_location, meta={'event': event})
        except ValueError:
            return

        return request

    def _parse_location(self, response):
        add = u' '.join(map(str.strip, response.xpath('//div[@class="entry-content"]/text()').getall())).strip()
        event = response.meta['event']
        event['location_address'] = add
        loc = self.geolocator.geocode(add)
        event['geo'] = dict(lat=loc.latitude, lon=loc.longitude)
        return event