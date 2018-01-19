# -*- coding: utf-8 -*-
# Originally by: Kelcey Damage, 2012 & Kraig Amador, 2012

import hashlib
import hmac
import base64
import logging

import requests

try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

log = logging.getLogger('cloudstack')


class SignedAPICall(object):
    def __init__(self, api_url, apiKey, secret):
        self.api_url = api_url
        self.apiKey = apiKey
        self.secret = secret

    def request(self, args):
        args['apiKey'] = self.apiKey

        self.params = []
        self._sort_request(args)
        self._create_signature()
        self._build_post_request()

    def _sort_request(self, args):
        keys = sorted(args.keys())

        for key in keys:
            self.params.append(key + '=' + quote_plus(args[key]).replace('+', '%20'))

    def _create_signature(self):
        self.query = '&'.join(self.params)
        digest = hmac.new(
            str.encode(self.secret, encoding='utf-8'),
            msg=str.encode(self.query.lower(), encoding='utf-8'),
            digestmod=hashlib.sha1).digest()

        self.signature = base64.b64encode(digest)

    def _build_post_request(self):
        self.query += '&signature=' + quote_plus(self.signature)
        self.value = self.api_url + '?' + self.query


class CloudStack(SignedAPICall):
    def __getattr__(self, name):
        def handlerFunction(*args, **kwargs):
            if kwargs:
                return self._make_request(name, kwargs)
            return self._make_request(name, args[0])
        return handlerFunction

    def _http_get(self, url):
        response = requests.get(url)
        return response

    def _make_request(self, command, args):
        args['response'] = 'json'
        args['command'] = command
        self.request(args)
        return self._http_get(self.value)
