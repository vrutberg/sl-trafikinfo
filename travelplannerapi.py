#!/usr/bin/python
# -*- coding: utf-8 -*-

from slapi import SlApi


class TravelPlannerApi(SlApi):
    def __init__(self, endpoint_url):
        SlApi.__init__(self, endpoint_url, "travelplannerApiKey")

#
# class JourneyDetailApi(TravelPlannerApi):
#     def __init__(self):
#         TravelPlannerApi.__init__(self, "http://api.sl.se/api2/TravelplannerV2/journeydetail.json")
#
