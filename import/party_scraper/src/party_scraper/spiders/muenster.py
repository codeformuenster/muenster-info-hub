# -*- coding: utf-8 -*-
""" Copyright (C) 2019 Christian Römer
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    Contact: https://github.com/thunfischtoast or christian.roemer[ät]posteo.de
"""

import scrapy
import urllib.request
import urllib.parse
import json
import logging
import os
import sys
import datetime
import pytz

from party_scraper import items


from_src_date = lambda str: datetime.datetime.strptime(str, '%Y-%m-%d')
to_date_str = lambda date: datetime.datetime.strftime(date, '%d.%m.%Y')
date_trans = lambda str: to_date_str(from_src_date(str))

class MuensterSpider(scrapy.Spider):
    name = "muenster"
    allowed_domains = ["muenster.de"]
    start_url = (
        "https://www.muenster.de/veranstaltungskalender/scripts/frontend/suche.php"
    )
    if "ELASTICSEARCH_URL_PREFIX" in os.environ:
        elasticsearch_url_param = os.environ["ELASTICSEARCH_URL_PREFIX"]
    if ('SCRAPE_START' in os.environ and 'SCRAPE_END' in os.environ):
        start = date_trans(os.environ['SCRAPE_START'])
        end = date_trans(os.environ['SCRAPE_END'])
    else:
        req_start_date = None
        req_end_date = None


    def start_requests(self):
        self.req_start_date = getattr(self, "start", None)
        self.req_end_date = getattr(self, "end", None)
        self.req_window = getattr(self, "window", None)
        self.mapquest_api_key = getattr(self, "mapquest_key", None)

        if self.req_window is not None and self.req_end_date is not None:
            self.log("Provice either a window or a end date, but not both")
            raise ValueError("Provie either a window or a end date, but not both")

        if self.mapquest_api_key is None and "MAPQUEST_KEY" in os.environ:
            self.mapquest_api_key = os.environ["MAPQUEST_KEY"]

        if self.req_start_date is None:
            start = datetime.datetime.now(pytz.timezone("Europe/Berlin")) + datetime.timedelta(days=1)
            self.req_start_date = start.strftime("%d.%m.%Y")
            end = datetime.datetime.now(pytz.timezone("Europe/Berlin")) + datetime.timedelta(days=8)
            self.req_end_date = end.strftime("%d.%m.%Y")

        if self.req_window is not None:
            try:
                self.req_window = int(self.req_window)
            except:
                self.log("Provide a integer as window")
                raise ValueError("Provide a integer as window")

            if self.req_window < 0:
                self.log("Provide a positive integer as window")
                raise ValueError("Provice a positive integer as window")

            if self.req_start_date == "today":
                start = datetime.datetime.now(pytz.timezone("Europe/Berlin"))
            else:
                start = datetime.datetime.strptime(self.req_start_date, "%d.%m.%Y")
            end = start + datetime.timedelta(days=self.req_window)
            self.req_start_date = start.strftime("%d.%m.%Y")
            self.req_end_date = end.strftime("%d.%m.%Y")

        elif self.req_start_date is not "today" and self.req_end_date is None:
            self.log('End date not given, using "today" as start date.')
            self.req_start_date = "today"

        if hasattr(self, "elasticsearch_url_param") == False:
            self.elasticsearch_url_param = None

        self.elasticsearch_url = getattr(
            self, "elasticsearch_url_prefix", self.elasticsearch_url_param
        )

        # TODO: validate start/end dates

        yield scrapy.Request(self.start_url, self.parse)

    def parse(self, response):
        """Submit the search form searching for events that start today."""

        datum_von = ""
        datum_bis = ""
        zeitraum = ""

        if self.req_start_date is None or self.req_start_date is "today":
            zeitraum = "heute"
        else:
            datum_von = self.req_start_date
            datum_bis = self.req_end_date
            zeitraum = "zeitraum"

        self.log("------------ START PARAMETERS -------------- ")
        self.log("START: " + datum_von)
        self.log("END: " + datum_bis)
        self.log("ES: " + str(self.elasticsearch_url))
        self.log("------------  ")

        return scrapy.FormRequest.from_response(
            response,
            formname="submit",
            formdata={
                "datum_bis": datum_bis,
                "datum_von": datum_von,
                "submit": "Suchen",
                "suchstring": "",
                "volltextsuche-verknuepfung": "und",
                "zeitraum": zeitraum,
                "zielgruppe": "alle",
            },
            callback=self.after_post,
        )

    def after_post(self, response):
        """Response here is the overview page over all events. We collect the links to the individual detail pages."""

        detail_links = response.xpath("//a[text() = 'Details']/@href").extract()
        for href in detail_links:
            categories = response.xpath(
                "//a[@href = '"
                + href
                + "']/ancestor::div[@class = 'eintrag ']/preceding-sibling::div[@class = 'kategorie']/text()"
            ).extract()
            category = categories[-1]
            # select the last of all preceding categories
            if category is not None:
                category = category.strip(" \t\n\r")
            yield response.follow(
                href, callback=self.extract_event, meta={"category": category}
            )


    def extract_event(self, response):
        """Callback function for the detail pages. We find the indivudal data points and try to bring the date/time in proper form, then
        summarize it into a Event-object and return it."""

        # extract the interesting data points
        title = self.getText(response, "titel")
        subtitle = self.getText(response, "untertitel")
        raw_datetime = self.getText(response, "datum-uhrzeit")
        description = self.getText(response, "detailbeschreibung")
        location = self.getText(response, "location")
        location_adresse = self.getText(response, "location-adresse")
        link = (
            response.xpath("//div[@class='detail-link']/a/@href")
            .extract_first()
        )
        if link is not None:
            link = link.strip(" \t\n\r")
        else:
            link = None
        pos = (
            response.xpath("//input[@name='pos']/@value")
            .extract_first()
            .strip(" \t\n\r")
        )

        times = self.produce_dates(raw_datetime)
        start_date = times[0]
        end_date = times[1]

        lat = ""
        lng = ""

        # if a mapquest api key was provided we use it for geocoding
        if self.mapquest_api_key is not None:
            latLng = self.fetchMapquestCoordinates(location_adresse)
            if latLng is not None:
                lat = latLng[0]
                lng = latLng[1]
        else: 
            self.log("No mapquest_api_key! Skip location mapping.")

        event = items.PartyItem(
            title=title,
            subtitle=subtitle,
            start_date=start_date,
            end_date=end_date,
            description=description,
            link=link,
            category=response.meta["category"],
            location_name=location,
            location_address=location_adresse,
            geo=dict(lat=lat, lon=lng),
            #location_lng=lng,
            #pos=pos,
            source='muenster.de'
        )

        if (
            self.elasticsearch_url is not None
            and isinstance(lat, float)
            and isinstance(lng, float)
        ):
            print(
                "Check before ES: "
                + str(self.elasticsearch_url)
                + "places/event_"
                + event["pos"]
                + " at pos lat:"
                + str(lat)
                + "; lng:"
                + str(lng)
            )
            self.log("Putting into ES")
            self.put_into_es(event)

        return event


    def getText(self, response, clazz):
        """Find the first div with the class clazz and extract the text, stripping whitespaces and such."""

        return (
            response.xpath("//div[@class='" + clazz + "']/text()")
            .extract_first()
            .strip(" \t\n\r")
        )

    def produce_dates(self, raw_datetime):
        """ Try to produce a clean start and end date (if it exists)."""

        # dates are usually of format "Donnerstag, 26.7.2018, 21.30 - 23.30 Uhr"
        # if there is only a start time it's just "Donnerstag, 26.7.2018, 21.30 Uhr"
        # sometimes the time is missing entirely, then it's just "Donnerstag, 26.7.2018,"
        # we'll ignore the leading day of the week

        datetime_parts = raw_datetime.split(",")  # split at commas
        date = datetime_parts[1].strip(" \t\n\r")  # drop whitespaces and such
        start_time = ""
        end_time = ""
        if len(datetime_parts) > 2:  # if there is a time given
            time = datetime_parts[2].replace("Uhr", "")  # drop unnessary string
            time_splits = time.split("-")  # split start and end time
            start_time = time_splits[0].strip(" \t\n\r")

            if len(time_splits) > 1:
                end_time = time_splits[1].strip(" \t\n\r")

        start_date = ""
        end_date = ""

        # sometimes, if the event contains two start/end times, the time looks like
        # 14.00 u. 16.00
        # in that case, use the first one for now. In future it would be better
        # to retain all times
        if " u. " in start_time:
            start_time = start_time.split(" u. ")[0]
        if " u. " in end_time:
            end_time = end_time.split(" u. ")[0]

        # produce proper ISO conform datetime strings
        if start_time is "":
            start_date = datetime.datetime.strptime(date, "%d.%m.%Y")  # case: no time
        else:
            start_date = datetime.datetime.strptime(
                date + " " + start_time, "%d.%m.%Y %H.%M"
            ).isoformat()

        if end_time is not "":
            end_date = datetime.datetime.strptime(
                date + " " + end_time, "%d.%m.%Y %H.%M"
            ).isoformat()

        return (start_date, end_date)

    def fetchMapquestCoordinates(self, location_adresse):
        """Try calling the geocoding api from mapquest. It it fails return None
            Documentation: https://developer.mapquest.com/documentation/open/geocoding-api/address/get/"""

        self.log("Attempt geocoding: " + location_adresse)

        contents_json = None
        try:
            parsed_location_adresse = urllib.parse.quote(location_adresse)
            mapquest_url = (
                "http://open.mapquestapi.com/geocoding/v1/address?key="
                + self.mapquest_api_key
                + "&location="
                + parsed_location_adresse
                + ",M%C3%BCnster,Germany"
            )
            logging.debug("Attempting to fetch " + mapquest_url)
            resource = urllib.request.urlopen(mapquest_url)
            contents = resource.read().decode(resource.headers.get_content_charset())
            contents_json = json.loads(contents)

        except Exception as e:
            logging.warning("Location geocoding failed with exception: " + str(e))
            return None

        status_code = contents_json["info"]["statuscode"]
        if status_code != 0:  # some kind of error happened
            logging.warning("Location geocoding failed with code " + status_code)
            return None

        latLng = contents_json["results"][0]["locations"][0]["latLng"]
        lat = latLng["lat"]
        lng = latLng["lng"]

        self.log("LOCATION: " + str(lat) + ", " + str(lng))
        if lat > 52.3 or lat < 51.8 or lng > 8 or lng < 7.3:
            self.log("NOT MUENSTER! Setting location to ZERO")
            return None  # not in Muenster

        return (lat, lng)

    def put_into_es(self, event):
        """Push the given event into Elasticsearch"""
        from elasticsearch import Elasticsearch

        esurl, index_prefix = os.environ["ELASTICSEARCH_URL_PREFIX"].rsplit(
            "/", maxsplit=1
        )

        if hasattr(self, "es") == False:
            self.es = Elasticsearch(esurl)


        content = {
            "address": {
                "geo": {"lat": event["location_lat"], "lon": event["location_lng"]},
                "geometry": {
                    "type": "Point",
                    "coordinates": [event["location_lng"], event["location_lat"]],
                },
                "street": event["location_addresse"],
            },
            "date_start": event["start_date"],
            "type": "event",
            "name": event["title"],
            "id": event["pos"],
            "properties": {
                "ID": event["pos"],
                "name": event["title"],
                "subtitle": event["subtitle"],
                "description": event["description"],
                "link": event["link"],
                "location": event["location"],
                "street": event["location_addresse"],
            },
        }

        if "end_date" in event and len(event["end_date"]) > 0:
            content["date_end"] = event["end_date"]

        res = self.es.index(
            index=(index_prefix + "places"),
            doc_type="_doc",
            body=content,
            id="event_" + event["pos"],
        )
        self.log(res)
