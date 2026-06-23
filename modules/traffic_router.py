import asyncio
from typing import Dict, Any, Optional

import aiohttp
from loguru import logger


class TrafficRouter:
    def __init__(self, tor_controller=None, proxy_manager=None, spoofer=None):
        self.tor = tor_controller
        self.proxy_mgr = proxy_manager
        self.spoofer = spoofer
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            connector = aiohttp.TCPConnector(ssl=False)
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)
        return self.session

    async def route_request(
        self,
        method: str = "GET",
        url: str = "",
        headers: Optional[Dict] = None,
        spoof_headers: bool = True
    ) -> Any:
        chain = self.proxy_mgr.build_chain() if self.proxy_mgr else []

        if spoof_headers and self.spoofer:
            req_headers = self.spoofer.get_headers()
        else:
            req_headers = {}

        if headers:
            req_headers.update(headers)

        if not chain:
            return await self._direct_request(method, url, req_headers)

        if len(chain) == 1:
            return await self._single_proxy_request(method, url, req_headers, chain[0])

        return await self._chained_request(method, url, req_headers, chain)

    async def _direct_request(self, method: str, url: str, headers: Dict) -> Any:
        session = await self._get_session()
        async with session.request(method, url, headers=headers) as resp:
            return await self._wrap_response(resp)

    async def _single_proxy_request(
        self, method: str, url: str, headers: Dict, proxy: Dict
    ) -> Any:
        proxy_url = proxy.get("url", "")
        session = await self._get_session()
        async with session.request(method, url, headers=headers, proxy=proxy_url) as resp:
            return await self._wrap_response(resp)

    async def _chained_request(
        self, method: str, url: str, headers: Dict, chain: list
    ) -> Any:
        for i, proxy in enumerate(chain):
            if i == len(chain) - 1:
                return await self._single_proxy_request(method, url, headers, proxy)
            proxy_url = proxy.get("url", "")
            session = await self._get_session()
            async with session.request(
                method, url, headers=headers, proxy=proxy_url
            ) as resp:
                pass
        return None

    async def _wrap_response(self, resp: aiohttp.ClientResponse) -> Any:
        class Response:
            def __init__(self, status, headers_dict, text):
                self.status_code = status
                self.headers = headers_dict
                self._text = text

            def json(self):
                import json
                return json.loads(self._text)

        text = await resp.text()
        return Response(resp.status, dict(resp.headers), text)

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()