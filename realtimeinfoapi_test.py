#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from realtimeinfoapi import RealTimeInfoApi
from testutils import UrlProxy
import slapi


class DummyRead():
    def __init__(self):
        pass

    def read(self):
        return u'{"StatusCode":0,"Message":null,"ExecutionTime":307,"ResponseData":{"LatestUpdate":"2014-10-09T18:36:00","DataAge":22,"Metros":[{"StopAreaName":"Telefonplan","GroupOfLine":"Tunnelbanans röda linje","DisplayTime":"Nu","SafeDestinationName":"Mörby centrum","GroupOfLineId":2,"DepartureGroupId":1,"PlatformMessage":null,"TransportMode":"METRO","LineNumber":"14","Destination":"Mörby centrum","JourneyDirection":1,"SiteId":9263},{"StopAreaName":"Telefonplan","GroupOfLine":"Tunnelbanans röda linje","DisplayTime":"4 min","SafeDestinationName":"Mörby centrum","GroupOfLineId":2,"DepartureGroupId":1,"PlatformMessage":null,"TransportMode":"METRO","LineNumber":"14","Destination":"Mörby centrum","JourneyDirection":1,"SiteId":9263},{"StopAreaName":"Telefonplan","GroupOfLine":"Tunnelbanans röda linje","DisplayTime":"12 min","SafeDestinationName":"Mörby centrum","GroupOfLineId":2,"DepartureGroupId":1,"PlatformMessage":null,"TransportMode":"METRO","LineNumber":"14","Destination":"Mörby centrum","JourneyDirection":1,"SiteId":9263},{"StopAreaName":"Telefonplan","GroupOfLine":"Tunnelbanans röda linje","DisplayTime":"8 min","SafeDestinationName":"Fruängen","GroupOfLineId":2,"DepartureGroupId":2,"PlatformMessage":null,"TransportMode":"METRO","LineNumber":"14","Destination":"Fruängen","JourneyDirection":2,"SiteId":9263},{"StopAreaName":"Telefonplan","GroupOfLine":"Tunnelbanans röda linje","DisplayTime":"18 min","SafeDestinationName":"Fruängen","GroupOfLineId":2,"DepartureGroupId":2,"PlatformMessage":null,"TransportMode":"METRO","LineNumber":"14","Destination":"Fruängen","JourneyDirection":2,"SiteId":9263},{"StopAreaName":"Telefonplan","GroupOfLine":"Tunnelbanans röda linje","DisplayTime":"27 min","SafeDestinationName":"Fruängen","GroupOfLineId":2,"DepartureGroupId":2,"PlatformMessage":null,"TransportMode":"METRO","LineNumber":"14","Destination":"Fruängen","JourneyDirection":2,"SiteId":9263}],"Buses":[],"Trains":[],"Trams":[],"Ships":[],"StopPointDeviations":[]}}'


def dummy_get_api_key(api):
    return "{0}:{1}".format(api._api_key_key, "secret-api-key")


class RealTimeInfoApiTestCase(unittest.TestCase):
    urlProxy = UrlProxy(DummyRead())

    def setUp(self):
        self.originalUrlOpen = slapi.urllib2.urlopen
        self.originalGetApiKey = slapi.SlApi._get_api_key

        slapi.SlApi._get_api_key = dummy_get_api_key
        slapi.urllib2.urlopen = self.urlProxy.proxy_url

    def tearDown(self):
        slapi.urllib2.urlopen = self.originalUrlOpen
        slapi.SlApi._get_api_key = self.originalGetApiKey

    def test_api_looks_like_expected(self):
        self.assertIsNotNone(RealTimeInfoApi)

        api = RealTimeInfoApi()
        self.assertIsNotNone(api.query)

    def test_query_data_is_ok(self):
        api = RealTimeInfoApi()

        data = api.query(2602, 10)
        self.assertIsNotNone(data)

        actual_url = self.urlProxy.last_url()

        self.assertTrue("?key={0}:{1}".format(api._api_key_key, "secret-api-key") in actual_url)
        self.assertTrue("siteid=2602" in actual_url)
        self.assertTrue("timewindow=10" in actual_url)

        self.assertEqual(len(data), 6)


if __name__ == '__main__':
    unittest.main()
