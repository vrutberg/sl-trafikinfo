#!/usr/bin/python
# -*- coding: utf-8 -*-

import json


class SlApi:
    _endpoint_url = None
    _api_key_key = None

    _configuration_object = None

    def __init__(self):
        return

    def _get_api_key(self):
        if self._configuration_object is None:
            f = open("environment.json", "r")
            lines = f.readlines()
            f.close()

            self._configuration_object = json.loads(''.join(lines))

        return self._configuration_object[self._api_key_key]

    def get_base_url(self):
        return self._endpoint_url + "?key=" + self._get_api_key()
