#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import urllib

from travelplannerapi import TravelPlannerApi


class TripApi(TravelPlannerApi):
    def __init__(self):
        TravelPlannerApi.__init__(self, "http://api.sl.se/api2/TravelplannerV2/trip.json")

    def query(self, origin_id, dest_id, num_trips=5):
        url = self.get_base_url()
        url = url + "&originId=" + urllib.quote_plus(origin_id)
        url = url + "&destId=" + urllib.quote_plus(dest_id)
        url = url + "&numTrips=" + str(num_trips)

        return self.make_api_call(url)

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

    args = parser.parse_args()

    api = TripApi()
    response = api.query(args.origin, args.destination, args.n)

    trips = ensure_list(response['TripList']['Trip'])

    for trip in trips:
        print "=== Trip"
        print_legs(trip['LegList']['Leg'])
