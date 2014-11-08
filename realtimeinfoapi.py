#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse

from slapi import SlApi
from lookupapi import LookupApi


class RealTimeInfoApi(SlApi):
    def __init__(self):
        SlApi.__init__(self, "http://api.sl.se/api2/realtimedepartures.json", "realtimedeparturesApiKey")

    def query(self, site_id, time_window, destination=None, skip_buses=False, skip_metro=False):
        params = {
            "siteid": site_id,
            "timewindow": time_window
        }

        jsondata = self.make_api_call(params)
        responsedata = jsondata["ResponseData"]

        all = []
        all += responsedata["Buses"] if skip_buses is False else []
        all += responsedata["Metros"] if skip_metro is False else []

        if destination is not None:
            return [item for item in all if item["Destination"] == destination]

        return all

if __name__ == "__main__":

    _transportModeMap = {
        "METRO": "T-bana",
        "BUS": "Buss"
    }

    parser = argparse.ArgumentParser(description="Search for departures from"
                                                 "train stations and bus stops in Stockholm")
    parser.add_argument("searchString", help="the train station or bus stop name to search for")
    parser.add_argument("-w", default=20, type=int, help="time window in minutes (default is 20)")
    parser.add_argument("-m", default=False, action="store_true", help="skip metros in results")
    parser.add_argument("-b", default=False, action="store_true", help="skip buses in results")
    parser.add_argument("-d", help="exact destination")

    args = parser.parse_args()

    lookupApi = LookupApi()
    realTimeApi = RealTimeInfoApi()

    lookupResults = lookupApi.query(args.searchString, 1)

    if len(lookupResults) == 1:
        station = lookupResults[0]
        dest = None

        if args.d is not None:
            dest = args.d

        print "=== {0}".format(station["Name"].encode("utf-8"))
        results = realTimeApi.query(station["SiteId"],
                                    time_window=args.w,
                                    destination=dest,
                                    skip_buses=args.b,
                                    skip_metro=args.m)

        for item in results:
            print "{0} {1} {2}: {3}".format(_transportModeMap[item["TransportMode"]],
                                            item["LineNumber"],
                                            item["Destination"].encode("utf-8"),
                                            item["DisplayTime"])
