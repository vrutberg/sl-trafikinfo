#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import urllib2
import urllib

class SlApi:
    _configuration_object = None

    def __init__(self, endpoint_url, api_key_key):
        self._endpoint_url = endpoint_url
        self._api_key_key = api_key_key

    def _get_api_key(self):
        try:
            if self._configuration_object is None:
                f = open("environment.json", "r")
                lines = f.readlines()
                f.close()
                self._configuration_object = json.loads(''.join(lines))

            return self._configuration_object[self._api_key_key]
        except IOError:
            print "Could not open 'environment.json' for reading"
            raise
        except ValueError:
            print "Could not parse 'environment.json', perhaps it contains invalid JSON?"
            raise
        except KeyError as e:
            print "Could not find key '" + e.message + "' in 'environment.json'"
            raise

    def get_base_url(self):
        return self._endpoint_url + "?key=" + self._get_api_key()

    def make_api_call(self, query_params=None):
        url = self.get_base_url()

        if query_params is not None:
            url += "&" + urllib.urlencode(query_params)

        response = urllib2.urlopen(url).read()
        return json.loads(response, "utf-8")
