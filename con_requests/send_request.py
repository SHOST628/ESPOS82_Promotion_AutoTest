from util.mylogger import logger
import requests
import json


class Requester:
    def __init__(self, test_cls, api_url, api_key):
        self.cls = test_cls
        self.api_url = api_url
        self.api_key = api_key

    def _header(self, api_key):
        headers = {
            'ApiKey': api_key
        }
        return headers

    def get(self):
        pass

    def post(self, request):
        if self.api_key == '' or self.api_key is None:
            self.cls.skipTest('缺少ApiKey,请在config.ini 下【Api】的 ApiKey 配置')
        elif self.api_url == '' or self.api_url is None:
            self.cls.skipTest('缺少API 请求路径,请在config.ini 下【Api】的 url 配置')
        headers = self._header(self.api_key)
        headers.update({'content-type': 'application/json'})
        res = requests.post(self.api_url, data=request, headers=headers)
        return res
