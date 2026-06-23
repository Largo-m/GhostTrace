import asyncio
import aiohttp
from typing import List, Dict
from loguru import logger


class ProxyValidator:
    def __init__(self, timeout: int = 8, concurrency: int = 30):
        self.timeout = timeout
        self.concurrency = concurrency
        self.test_urls = [
            "https://httpbin.org/ip",
            "https://api.ipify.org?format=json"
        ]
        self._semaphore = asyncio.Semaphore(concurrency)
        self._session: aiohttp.ClientSession = None

    async def _get_session(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session
    # here you can set how much proxy list would be
    async def validate(self, proxies: List[str], max_valid: int = 20) -> List[Dict[str, str]]:
        if not proxies:
            return []

        logger.info(f"Validating up to {max_valid} proxies from {len(proxies)} total...")

        session = await self._get_session()
        tasks = [self._validate_one(session, proxy) for proxy in proxies]

        valid = []
        for coro in asyncio.as_completed(tasks):
            try:
                result = await coro
                if isinstance(result, dict):
                    valid.append(result)
                    if len(valid) >= max_valid:
                        break
            except Exception:
                pass

        logger.success(f"{len(valid)} valid proxies found")
        return valid

    async def _validate_one(self, session: aiohttp.ClientSession, proxy_url: str) -> Dict:
        async with self._semaphore:
            for test_url in self.test_urls:
                try:
                    async with session.get(
                            test_url,
                            proxy=proxy_url,
                            timeout=aiohttp.ClientTimeout(total=self.timeout)
                    ) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            ip = data.get("origin") or data.get("ip") or str(data)
                            return {"url": proxy_url, "exit_ip": str(ip).strip()}
                except Exception:
                    continue
        raise ValueError(f"Failed: {proxy_url}")

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()