import requests
import os
import time
from abc import abstractclassmethod

class RequestError(RuntimeError):
    def __init__(self, message, code, url, response_headers: dict = None):
        self.message = message
        self.code = code
        self.url = url
        self.response_headers = response_headers

class RequestClient:

    def __init__(self):
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com"
        }
        self._sleepTime = 10
        self._requestTime = 0.6
        self._language = "ko_KR"
    
    def set_api_key(self, key:str):
        self._headers["X-Riot-Token"] = key

    def _get(self, url, verify=None):
        r = requests.get(url, headers=self._headers, verify=verify)
        time.sleep(self._requestTime)
        return r

    def get_status(self, url, verify=None):
        r = self._get(url, verify=verify)

        return r.status_code

    def get(self, url, verify=None):
        r = self._get(url, verify=verify)
        
        r_headers = r.headers

        if r.status_code == 429:
            time.sleep(self._sleepTime)
            return self.get(url, verify)
        elif r.status_code >= 400:
            raise RequestError(r.reason, url, r.status_code, r_headers)
        
        content_type = r_headers.get("Content-Type", "application/octet-stream").upper()

        if "APPLICATION/JSON" in content_type:
            body = r.json()
        elif "IMAGE/" in content_type:
            body = r.content
        else:
            body = r.content.decode("utf-8")
        
        return body, r_headers

class APIObject:

    def __init__(self, client:RequestClient):
        self._client = client
        self._queue = 450
    
    def _set_api_key(self, key:str):
        self._client.set_api_key(key)

    @property
    @abstractclassmethod
    def _dto_types(cls):
        pass