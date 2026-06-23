import asyncio
import aiohttp
from abc import ABC, abstractmethod
from typing import List, Optional, Set
from loguru import logger


class BaseScraper(ABC):
    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None
        self._proxies: Set[str] = set()

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            timeout_config = aiohttp.ClientTimeout(total=self.timeout)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
            }
            self.session = aiohttp.ClientSession(
                timeout=timeout_config,
                headers=headers
            )
        return self.session

    @abstractmethod
    async def fetch(self) -> List[str]:
        pass

    def _clean_proxy(self, raw: str) -> Optional[str]:
        raw = raw.strip()
        if not raw or ":" not in raw:
            return None
        if raw.count(".") < 1:
            return None
        if any(c.isalpha() and c not in "httpssocks45://" for c in raw.replace("://", "").replace(".", "").replace(":", "")):
            return None
        if not raw.startswith(("http://", "https://", "socks4://", "socks5://")):
            raw = f"http://{raw}"
        return raw

    async def scrape(self) -> List[str]:
        logger.info(f"Scraping from {self.__class__.__name__}...")
        try:
            raw_proxies = await self.fetch()
            cleaned = []
            for proxy in raw_proxies:
                cleaned_proxy = self._clean_proxy(proxy)
                if cleaned_proxy and cleaned_proxy not in self._proxies:
                    self._proxies.add(cleaned_proxy)
                    cleaned.append(cleaned_proxy)
            logger.success(f"{self.__class__.__name__}: {len(cleaned)} new proxies found")
            return cleaned
        except Exception as e:
            logger.error(f"{self.__class__.__name__} failed: {e}")
            return []

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()