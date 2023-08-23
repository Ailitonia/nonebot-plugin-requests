'''
@Author         :   Ailitonia
@Date           :   2023/08/23 23:57:15
@FileName       :   requests.py
@Description    :   requests 封装
@GitHub         :   https://github.com/Ailitonia
@Software       :   PyCharm
'''

import asyncio
import pathlib
from contextlib import asynccontextmanager
from copy import deepcopy
from typing import Any, AsyncGenerator, Optional, cast
from urllib.parse import urlparse

try:
    import ujson as json
except ImportError:
    import json

from nonebot import get_driver, logger
from nonebot.drivers import Request, Response, WebSocket, ForwardDriver
from nonebot.internal.driver.model import (
    QueryTypes,
    HeaderTypes,
    CookieTypes,
    ContentTypes,
    DataTypes,
    FilesTypes,
)


from .config import plugin_config


class NonebotRequests(object):
    """对 ForwardDriver 二次封装实现的 HttpClient"""

    _default_timeout_time: float = 10.0
    _default_headers: dict[str, str] = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'dnt': '1',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                      '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    def __init__(
            self,
            *,
            timeout: Optional[float] = None,
            headers: HeaderTypes = None,
            cookies: CookieTypes = None,
            tries: int = 3,
            retry_delay: int = 2,
    ):
        self.driver = get_driver()
        if not isinstance(self.driver, ForwardDriver):
            raise RuntimeError(
                f"Current driver {self.driver.type} doesn't support forward "
                "connections! NonebotRequests need a ForwardDriver to work."
            )

        self.timeout = self._default_timeout_time if timeout is None else timeout
        self.headers = self._default_headers if headers is None else headers
        self.cookies = cookies
        self.tries = tries
        self.retry_delay = retry_delay

    @staticmethod
    def parse_content_json(response: Response, **kwargs) -> Any:
        """解析 Response Content 为 Json"""
        return json.loads(response.content, **kwargs) # type: ignore

    @staticmethod
    def parse_content_text(response: Response, encoding: str = 'utf-8') -> str | None:
        """解析 Response Content 为字符串"""
        if isinstance(response.content, bytes):
            return response.content.decode(encoding=encoding)
        else:
            return response.content

    @classmethod
    def parse_url_file_name(cls, url: str) -> str:
        """尝试解析 url 对应的文件名"""
        parsed_url = urlparse(url=url, allow_fragments=True)
        original_file_name = pathlib.Path(parsed_url.path).name
        return original_file_name

    @classmethod
    def get_default_headers(cls) -> dict[str, str]:
        return deepcopy(cls._default_headers)

    async def request(self, setup: Request) -> Response: # type: ignore
        """装饰原 driver.request 方法, 自动重试"""
        self.driver = cast(ForwardDriver, self.driver)

        _tries, _delay = self.tries, self.retry_delay
        while _tries > 0:
            try:
                return await self.driver.request(setup=setup)
            except Exception as e:
                _tries -= 1
                if _tries <= 0:
                    raise e
                
                logger.warning(
                    f'{setup!r} failed with {e!r}, retrying in {_delay!r} seconds'
                )

                await asyncio.sleep(self.retry_delay)


    @asynccontextmanager
    async def websocket(
            self,
            method: str,
            url: str,
            *,
            params: QueryTypes = None,
            headers: HeaderTypes = None,
            cookies: CookieTypes = None,
            content: ContentTypes = None,
            data: DataTypes = None,
            json: Any = None,
            files: FilesTypes = None,
            timeout: Optional[float] = None,
            use_proxy: bool = True
    ) -> AsyncGenerator[WebSocket, None]:
        """建立 websocket 连接"""
        self.driver = cast(ForwardDriver, self.driver)

        setup = Request(
            method=method,
            url=url,
            params=params,
            headers=self.headers if headers is None else headers,
            cookies=self.cookies if cookies is None else cookies,
            content=content,
            data=data,
            json=json,
            files=files,
            timeout=self.timeout if timeout is None else timeout,
            proxy=plugin_config.proxy_url if use_proxy else None
        )

        async with self.driver.websocket(setup=setup) as ws:
            yield ws

    async def get(
            self,
            url: str,
            *,
            params: QueryTypes = None,
            headers: HeaderTypes = None,
            cookies: CookieTypes = None,
            content: ContentTypes = None,
            data: DataTypes = None,
            json: Any = None,
            files: FilesTypes = None,
            timeout: Optional[float] = None,
            use_proxy: bool = True
    ) -> Response:
        setup = Request(
            method='GET',
            url=url,
            params=params,
            headers=self.headers if headers is None else headers,
            cookies=self.cookies if cookies is None else cookies,
            content=content,
            data=data,
            json=json,
            files=files,
            timeout=self.timeout if timeout is None else timeout,
            proxy=plugin_config.proxy_url if use_proxy else None
        )
        return await self.request(setup=setup)

    async def post(
            self,
            url: str,
            *,
            params: QueryTypes = None,
            headers: HeaderTypes = None,
            cookies: CookieTypes = None,
            content: ContentTypes = None,
            data: DataTypes = None,
            json: Any = None,
            files: FilesTypes = None,
            timeout: Optional[float] = None,
            use_proxy: bool = True
    ) -> Response:
        setup = Request(
            method='POST',
            url=url,
            params=params,
            headers=self.headers if headers is None else headers,
            cookies=self.cookies if cookies is None else cookies,
            content=content,
            data=data,
            json=json,
            files=files,
            timeout=self.timeout if timeout is None else timeout,
            proxy=plugin_config.proxy_url if use_proxy else None
        )
        return await self.request(setup=setup)


__all__ = [
    'NonebotRequests',
]
