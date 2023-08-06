from abc import ABC, abstractmethod

__all__ = [
    'APIMethod'
]

import base64
import random
import string

import ecdsa
import hashlib

import re
import json
import requests

from enum import Enum, StrEnum
from datetime import datetime

from pydantic import BaseModel

from requests import Response
from aiohttp import (
    ClientSession,
    ClientResponse
)
from typing import Union, Optional

from mbnk.exceptions import *

from mbnk.types import *

from mbnk.responses import *

from pydantic import dataclasses


class BaseAPIMethod(ABC):
    _api_token = None
    _headers = {}

    def __init__(
            self,
            base_url: str,
            api_token: Optional[str] = None
    ):
        self._base_url: str = base_url

        if api_token is not None:
            self._api_token: str = api_token
            self._headers["X-Token"] = self._api_token

    @staticmethod
    def _time_header():
        def outer(func):
            def inner(self):
                self.__headers["X-Time"]: str = str(int(datetime.now().timestamp()))

            return inner

        return outer

    @staticmethod
    def _key_id_header():
        def outer(func):
            def inner(self):
                self.__headers["X-Key-Id"]: str = self.__key_id

            return inner

        return outer

    @abstractmethod
    def _request(self):
        pass


class APIMethod(BaseAPIMethod):

    def __init__(
            self,
            base_url: str,
            api_token: Optional[str] = None,
    ):
        super().__init__(
            base_url=base_url,
            api_token=api_token
        )

    @staticmethod
    def __is_exception(response: Union[Response, ClientResponse]) -> bool:
        if isinstance(response, Response):
            status_code = response.status_code
        elif isinstance(response, ClientResponse):
            status_code = response.status
        else:
            return True

        if status_code != 200:
            return True

        return False

    def __sync_request(
            self,
            method: str,
            path: str,
            data: str = None,
            params: str = None
    ):
        response = requests.request(
            method=method,
            url=f"{self.__base_url}/{path}",
            headers=self.__headers,
            params=params,
            data=json.dumps(data) if data is not None else None
        )
        response_data = response.json()

        if self.__is_exception(response):
            raise MonobankAPIException

        if isinstance(response_data, list):
            return {"list": response_data}

        return response.json()

    async def __async_request(
            self,
            method: str,
            path: str,
            data: str = None,
            params: str = None
    ):
        async with ClientSession() as session:
            request = getattr(session, method)
            async with request(
                    url=f"{self.__base_url}/{path}",
                    headers=self.__headers,
                    data=json.dumps(data) if data is not None else None,
                    params=params
            ) as response:
                response_data = await response.json()
                response_data = self.__load_response(response_data)

                if self.__is_exception(response):
                    raise MonobankAPIException

                return response_data

    @staticmethod
    def __generate_request_id():
        request_id = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(18, 24)))
        return request_id

    @staticmethod
    def _request_id_header():
        def outer(func):
            def inner(self):
                self.__headers["X-Request-Id"]: str = self.__generate_request_id()

            return inner

        return outer

    @staticmethod
    def __create_signature(self):
        url = "https://api.monobank.ua"
        data = (self.__headers["X-Time"] + url).encode('utf-8')

        private_key = ecdsa.SigningKey.from_pem(self.__privkey, hashfunc=hashlib.sha256)

        sign = private_key.sign(data, hashfunc=hashlib.sha256)
        sign_base64 = base64.b64encode(sign)

        return sign_base64

    @staticmethod
    def _sign_header():
        def outer(func):
            def inner(self):
                self.__headers["X-Sign"]: str = self.__create_signature(self)
            return inner

        return outer

    @staticmethod
    async def _async_request(
            method: str,
            path: str
    ):
        async def outer(func):
            async def inner(*args, **kwargs):
                self = args[0]
                args = args[1:]

                func_args = {
                    "method": method,
                    "path": path,
                    ("params" if request_method == "get" else "data"): self.__build_data(**kwargs)
                }

                async with ClientSession() as session:
                    async with session.request(
                            method=method,
                            url=f"{self.__base_url}/{path}",
                            headers=self.__headers,
                            data=json.dumps(data) if data is not None else None,
                            params=params
                    ) as response:
                        response_data = await response.json()
                        response_data = self.__load_response(response_data)

                        if self.__is_exception(response):
                            raise MonobankAPIException

                        if isinstance(response, MonobankAPIException) or isinstance(response, MonobankAPIException):
                            return response

                        return func(self, *args, **kwargs, response_data=response)

            return inner

        return outer

    @staticmethod
    def _request(
            method: str,
            path: str
    ):
        def outer(func):
            def inner(*args, **kwargs):
                self = args[0]
                args = args[1:]

                func_args = {
                    "method": method,
                    "path": path,
                    ("params" if request_method == "get" else "data"): self.__build_data(**kwargs)
                }

                response = requests.request(
                    method=method,
                    url=f"{self.__base_url}/{path}",
                    headers=self.__headers,
                    params=params,
                    data=json.dumps(data) if data is not None else None
                )

                response_data = response.json()

                if self.__is_exception(response):
                    raise MonobankAPIException

                if isinstance(response_data, list):
                    response_data = {"list": response_data}

                return func(self, *args, **kwargs, response_data=response_data)

            return inner

        return outer
