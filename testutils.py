#!/usr/bin/python
# -*- coding: utf-8 -*-

class UrlProxy():
    def __init__(self, response):
        self.openUrls = []
        self.response = response

    def last_url(self):
        return self.openUrls.pop()

    def proxy_url(self, url):
        self.openUrls.append(url)
        return self.response
