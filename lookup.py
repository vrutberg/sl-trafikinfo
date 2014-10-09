#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import json
import argparse

from slapi import SlApi


class Lookup(SlApi):

    _endpoint_url = "http://api.sl.se/api2/typeahead.json"
    _api_key_key = "typeaheadApiKey"

    def _transform_response_data_item(self, item):
        return {
            "text": item["Name"],
            "id": item["SiteId"]
        }

    def query(self, search_string, max_results):
        url = self.get_base_url()
        url = url + "&searchstring=" + str(search_string)
        url = url + "&maxresults=" + str(max_results)

        response = urllib2.urlopen(url).read()
        jsondata = json.loads(response, "utf-8")

        return map(self._transform_response_data_item,
                   jsondata["ResponseData"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for train stations and "
                                                 "bus stops in Stockholm")
    parser.add_argument("searchString", help="the train station or bus stop name to search for")
    parser.add_argument("-n", default=10, type=int, help="limit the search results to this number")

    args = parser.parse_args()

    api = Lookup()

    results = api.query(args.searchString, args.n)

    for item in results:
        print "{0}: {1}".format(item["text"].encode("utf-8"), item["id"])
