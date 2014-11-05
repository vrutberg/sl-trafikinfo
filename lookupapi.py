#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse

from slapi import SlApi


class LookupApi(SlApi):
    def __init__(self):
        SlApi.__init__(self, "http://api.sl.se/api2/typeahead.json", "typeaheadApiKey")

    def query(self, search_string, max_results):
        url = self.get_base_url()
        url = url + "&searchstring=" + str(search_string)
        url = url + "&maxresults=" + str(max_results)

        jsondata = self.make_api_call(url)

        return jsondata["ResponseData"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for train stations and "
                                                 "bus stops in Stockholm")
    parser.add_argument("searchString", help="the train station or bus stop name to search for")
    parser.add_argument("-n", default=10, type=int, help="limit the search results to this number")

    args = parser.parse_args()

    api = LookupApi()

    results = api.query(args.searchString, args.n)

    for item in results:
        print "{0}: {1}".format(item["Name"].encode("utf-8"), item["SiteId"])
