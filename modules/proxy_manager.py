import asyncio
import random
from typing import List, Dict, Optional

import aiohttp
from loguru import logger
from scrapers.pool_manager import PoolManager


class ProxyManager:
    def __init__(self, min_chain: int = 2, max_chain: int = 4, timeout: int = 10):
        self.min_chain = min_chain
        self.max_chain = max_chain
        self.timeout = timeout
        self.available_proxies: List[Dict[str, str]] = []
        self._pool_manager = PoolManager()

    async def load_proxies(self, filepath: str = "config/proxy_list.txt", auto_scrape: bool = True) -> None:
        if auto_scrape:
            logger.info("Auto-scraping proxies from internet...")
            self.available_proxies = await self._pool_manager.refresh_pool()
            if self.available_proxies:
                logger.success(f"Pool refreshed with {len(self.available_proxies)} proxies")
                return

        try:
            with open(filepath, 'r') as f:
                raw = [line.strip() for line in f if line.strip() and not line.startswith('#')]

            if raw:
                self.available_proxies = [{"url": p, "exit_ip": "unknown"} for p in raw]
                logger.success(f"Loaded {len(self.available_proxies)} proxies from file")
            elif auto_scrape:
                self.available_proxies = await self._pool_manager.refresh_pool()
        except FileNotFoundError:
            logger.warning(f"No proxy file found at {filepath}")
            if auto_scrape:
                self.available_proxies = await self._pool_manager.refresh_pool()

    def build_chain(self) -> List[Dict[str, str]]:
        if len(self.available_proxies) < self.min_chain:
            logger.warning(f"Only {len(self.available_proxies)} proxies available, need {self.min_chain}")
            return self.available_proxies.copy()

        chain_len = random.randint(self.min_chain, min(self.max_chain, len(self.available_proxies)))
        return random.sample(self.available_proxies, chain_len)

    @property
    def proxy_count(self) -> int:
        return len(self.available_proxies)