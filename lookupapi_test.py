#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from lookupapi import LookupApi
from testutils import UrlProxy
import slapi


class DummyRead():
    def __init__(self):
        pass

    def read(self):
        return u'{"StatusCode":0,"Message":null,"ExecutionTime":5,"ResponseData":[{"Name":"TES",' \
               u'"SiteId":"1137","Type":"Station","X":"18081172","Y":"59348509"},{"Name":' \
               u'"Tessinparken (Stockholm)","SiteId":"1131","Type":"Station","X":"18093379","Y"' \
               u':"59345192"},{"Name":"Solskiftesvägen (Österåker)","SiteId":"2605","Type":"Station"' \
               u',"X":"18303718","Y":"59504967"},{"Name":"Nantes vägskäl (Österåker)","SiteId":"2847"' \
               u',"Type":"Station","X":"18289218","Y":"59441521"},{"Name":"Nöttesta (Södertälje)",' \
               u'"SiteId":"7726","Type":"Station","X":"17415782","Y":"59286816"},{"Name":"Sittesta (Nynäshamn)",' \
               u'"SiteId":"8630","Type":"Station","X":"17919681","Y":"58976976"},{"Name":"Östermalmstorg (Stockholm)",' \
               u'"SiteId":"9206","Type":"Station","X":"18080048","Y":"59336365"},{"Name":' \
               u'"Tegnérgatan (Västm.g/Upplandsg) (Stockholm)","SiteId":"1046","Type":"Station","X":' \
               u'"18052101","Y":"59338064"},{"Name":"ÖST","SiteId":"9600","Type":"Station","X":"1807170' \
               u'6","Y":"59345543"},{"Name":"Tunagård (Österåker)","SiteId":"9661","Type":"Station","X' \
               u'":"18307287","Y":"59469630"}]}'


def dummy_get_api_key(api):
    return "{0}:{1}".format(api._api_key_key, "secret-api-key")


class LookupApiTestCase(unittest.TestCase):
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
        self.assertIsNotNone(LookupApi)

        api = LookupApi()
        self.assertIsNotNone(api.query)

    def test_query_data_is_ok(self):
        api = LookupApi()

        data = api.query("telefonplan", 100)
        self.assertIsNotNone(data)

        expected_url = "{0}?key={1}:{2}&searchstring={3}&maxresults={4}".format(api._endpoint_url,
                                                                                api._api_key_key,
                                                                                'secret-api-key',
                                                                                "telefonplan",
                                                                                100)

        actual_url = self.urlProxy.last_url()

        self.assertEquals(actual_url, expected_url)

        self.assertEqual(len(data), 10)


if __name__ == '__main__':
    unittest.main()