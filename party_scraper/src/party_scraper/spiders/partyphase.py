import scrapy
from party_scraper import items


class EventURLSpider(scrapy.Spider):
    name = "partyphase"
    allowed_domains = ["muenster.partyphase.net"]
    start_urls = [
        'http://muenster.partyphase.net/veranstaltungskalender-muenster/',
    ]

    def parse(self, response):
        # split events
        raw = response.xpath('//div[@class="kalenderbreit"]')

        # get event URLs from overview
        A = raw.xpath('//div[@class="veranstaltungsname"]/a')
        event_urls = A.xpath('@href').getall()

        # crawl events
        for event_url in event_urls:
            yield scrapy.Request(event_url, callback=self._parse_event)

        return events

    def _get_location_address(self, url):
        response = scrapy.Request(url=url)
        add = response.xpath('//div[@class="entry-content"]/text()').getall()
        return f'{add[1].strip()} {add[2].strip()}'

    def _parse_event(self, response):
        event = items.PartyItem()

        event['title'] = response.xpath('//div/div[@class="eme_period"]/text()').get()
        event['start_date'] = response.xpath('//div/div[@class="beginn"]/text()').get()
        event['location_name'] = response.xpath('//div/div[@class="ort"]/a/text()').get()
        event['link'] = response.url
        event['description'] = u' '.join([s.strip() for s in response.xpath('//div/p/text()').getall()])
        # TODO: extract tags from description
        # event['tags'] = ['party']
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
        return event