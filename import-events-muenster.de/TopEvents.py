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


class TopEventsSpider(scrapy.Spider):
    name = "TopEventsSpider"
    allowed_domains = ["www.muenster.de"]
    start_urls = [
        "https://www.muenster.de/veranstaltungskalender/scripts/frontend/top-veranstaltungen.php",
        "https://www.muenster.de/veranstaltungskalender/scripts/frontend/mm2/top-veranstaltungen.php?guestID=101"
    ]
    if "ELASTICSEARCH_URL_PREFIX" in os.environ:
        elasticsearch_url_param = os.environ["ELASTICSEARCH_URL_PREFIX"]
    req_start_date = None
    req_end_date = None

    def parse(self, response):

        self.mapquest_api_key = getattr(self, "mapquest_key", None)
        if self.mapquest_api_key is None and "MAPQUEST_KEY" in os.environ:
            self.mapquest_api_key = os.environ["MAPQUEST_KEY"]

        if hasattr(self, "elasticsearch_url_param") == False:
            self.elasticsearch_url_param = None
        self.elasticsearch_url = getattr(
            self, "elasticsearch_url_prefix", self.elasticsearch_url_param
        )

        detail_links = response.xpath("//a[text() = 'Details']/@href").extract()

        for href in detail_links:
            category = "top"
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
            title
        )
        image_url = (
            response.xpath("//div[@class='tv-grafik']/img/@src")
            .extract_first()
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

        event = Event(
            title=title,
            subtitle=subtitle,
            start_date=start_date,
            end_date=end_date,
            location=location,
            location_addresse=location_adresse,
            location_lat=lat,
            location_lng=lng,
            description=description,
            link=link,
            category=response.meta["category"],
            pos=pos,
            image_url=image_url
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

        # dates are sometimes of format "Donnerstag, 26.7.2018, 21.30 - 23.30 Uhr"
        # and sometimes "26.7.2018 - 22.12.2019"
        # if there is only a start time it's just "Donnerstag, 26.7.2018, 21.30 Uhr"
        # sometimes the time is missing entirely, then it's just "Donnerstag, 26.7.2018,"
        # we'll ignore the leading day of the week

        self.log("----> datetime " + raw_datetime)
        raw_datetime = raw_datetime.replace("--","-")
        datetime_parts = raw_datetime.split(",")  # split at commas

        if len(datetime_parts) > 1:
            date = datetime_parts[1]
        else:
            date = raw_datetime

        date = date.strip(" \t\n\r")  # drop whitespaces and such
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

            if date.count("-"):
                date_splits = date.split("-")
                date=date_splits[0].strip(" \t\n\r")
                end_date = datetime.datetime.strptime(date_splits[1].strip(" \t\n\r"), "%d.%m.%Y")
            start_date = datetime.datetime.strptime(date, "%d.%m.%Y")  # case: no time
        else:
            start_date = datetime.datetime.strptime(
                date + " " + start_time, "%d.%m.%Y %H.%M"
            ).isoformat()

        if end_time is not "":
            end_date = datetime.datetime.strptime(
                date + " " + end_time, "%d.%m.%Y %H.%M"
            ).isoformat()

        self.log("---> got dates " + str(start_date) + " - " + str(end_date))
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
            "id": event["pos"],
            "title": event["title"],
            "subtitle": event["subtitle"],
            "start_date": str(event["start_date"]).replace(" ","T")+"Z",
            "description": event["description"],
            "link": event["link"],
            "category": "top",
            "location_name": event["location"],
            "location_address": event["location_addresse"],
            "source": "www.muenster.de",
            "geo": {
                "lat": event["location_lat"], 
                "lon": event["location_lng"],
            },
            "is_top_event": True,
            "images": [
                { "image_url":event["image_url"] }
            ]
        }

        if "end_date" in event and event["end_date"]:
            content["end_date"] = str(event["end_date"]).replace(" ","T")+"Z"

        res = self.es.index(
            index=(index_prefix + "events"),
            doc_type="_doc",
            body=content,
            id="event_" + event["pos"],
        )
        self.log(res)



class Event(scrapy.Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    location = scrapy.Field()
    location_addresse = scrapy.Field()
    location_lat = scrapy.Field()
    location_lng = scrapy.Field()
    description = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()
    pos = scrapy.Field()
    image_url = scrapy.Field()
