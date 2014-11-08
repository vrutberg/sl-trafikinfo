#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import urllib
from datetime import datetime
from time import time

from travelplannerapi import TravelPlannerApi


class TripApi(TravelPlannerApi):
    def __init__(self):
        TravelPlannerApi.__init__(self, "http://api.sl.se/api2/TravelplannerV2/trip.json")

    def query(self, origin_id, dest_id, dep_date=None, dep_time=None, num_trips=5):
        params = {
            "originId": origin_id,
            "destId": dest_id,
            "numTrips": num_trips
        }

        if dep_date is not None:
            params['date'] = dep_date

        if dep_time is not None:
            params['time'] = dep_time

        return self.make_api_call(params)

if __name__ == "__main__":

    def ensure_list(possible_list):
        if type(possible_list) is not list:
            return [possible_list]
        else:
            return possible_list

    def print_legs(input):
        legs = ensure_list(input)

        for leg in legs:
            print "{0} {1} -> {2} -> {3} {4}".format(leg['Origin']['name'].encode('utf-8'),
                                                     leg['Origin']['time'],
                                                     leg['type'],
                                                     leg['Destination']['name'].encode('utf-8'),
                                                     leg['Destination']['time'])

    parser = argparse.ArgumentParser(description="Search for trips in Stockholm")
    parser.add_argument("origin", help="trip origin")
    parser.add_argument("destination", help="trip destination")
    parser.add_argument("-n", default=5, type=int, help="maximum number of trips returned")
    parser.add_argument("-w", default=0, type=int, help="search for departures in x minutes")

    args = parser.parse_args()

    dep_date = None
    dep_time = None

    if args.w > 0:
        timestamp = int(time()) + args.w * 60
        dt = datetime.fromtimestamp(timestamp)

        dep_date = dt.strftime("%Y-%m-%d")
        dep_time = dt.strftime("%H:%M")

    api = TripApi()
    response = api.query(args.origin, args.destination, dep_date, dep_time, args.n)

    trips = ensure_list(response['TripList']['Trip'])

    for trip in trips:
        print "=== Trip"
        print_legs(trip['LegList']['Leg'])
