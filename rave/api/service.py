from json import JSONDecodeError, dumps
from typing import Union

from requests import get as _get, post as _post, delete as _delete, put as _put, Response

from . import headers
from .exceptions import handle_exception


class Service:
    def __init__(self, proxies: dict = None):
        self.api = "https://api.red.wemesh.ca{}".format
        self.mojo = "https://api.mojoauth.com{}".format
        self.proxies = proxies
        self.deviceId = None
        self.sessionId = None

    @staticmethod
    def __compose(response):
        try:
            body = response.json()
            handle_exception(body) if response.status_code != 200 else ...
        except JSONDecodeError:
            body = {}

        return body

    @staticmethod
    def get_headers(data=None, soboro=False, mojo=False):
        return (
            headers.Headers().mojo if mojo else (
                headers.Headers().soboro if soboro else headers.Headers(data).headers
            )
        )

    def mojo_post(self, path: str, data: dict = None, params: dict = None) -> dict:
        data = dumps(data)
        response = _post(self.mojo(path), data=data, params=params, headers=self.get_headers(mojo=True),
                         proxies=self.proxies)
        return self.__compose(response)

    def mojo_get(self, path: str, params: dict = None) -> dict:
        response = _get(self.mojo(path), params=params, headers=self.get_headers(mojo=True), proxies=self.proxies)
        return self.__compose(response)

    def post(self, path: str, data: dict = None, params: dict = None) -> dict:
        data = dumps(data)
        response = _post(self.api(path), data=data, params=params, headers=self.get_headers(data),
                         proxies=self.proxies)
        return self.__compose(response)

    def get(self, path: str, params: dict = None) -> dict:
        response = _get(self.api(path), params=params, headers=self.get_headers(), proxies=self.proxies)
        return self.__compose(response)

    def delete(self, path: str, params: dict = None) -> dict:
        response = _delete(self.api(path), params=params, headers=self.get_headers(), proxies=self.proxies)
        return self.__compose(response)

    def put(self, path: str, data: Union[dict, str] = None) -> dict:
        response = _put(self.api(path), data=data, headers=self.get_headers(data), proxies=self.proxies)
        return self.__compose(response)

    def getRequest(self, url: str, params=None):
        response = _get(url, params=params, headers=headers.Headers().agent, proxies=self.proxies)
        return response

    def postSoboro(self, url: str, data: Union[dict, str] = None, params: dict = None) -> Response:
        response = _post(url, data=data, params=params, headers=self.get_headers(soboro=True), proxies=self.proxies)
        return response

    def deleteSoboro(self, url: str, params: dict = None) -> Response:
        response = _delete(url, params=params, headers=self.get_headers(soboro=True), proxies=self.proxies)
        return response

    def putSoboro(self, url: str, data: Union[dict, str] = None) -> dict:
        response = _put(url, data=data, headers=self.get_headers(soboro=True), proxies=self.proxies)
        return self.__compose(response)
