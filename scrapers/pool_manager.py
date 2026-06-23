import asyncio
import random
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger

from scrapers.proxy_scrapers import (
    ProxyScrapeScraper,
    ProxyListDownloadScraper,
    OpenProxyListScraper,
    FreeProxyListScraper,
    GeoNodeScraper,
    SpysMeScraper
)
from scrapers.validator import ProxyValidator


class PoolManager:
    def __init__(self, storage_path: str = "config/proxy_list.txt"):
        self.storage_path = Path(storage_path)
        self.scrapers = [
            ProxyScrapeScraper(),
            ProxyListDownloadScraper(),
            OpenProxyListScraper(),
            FreeProxyListScraper(),
            GeoNodeScraper(),
            SpysMeScraper()
        ]
        self.validator = ProxyValidator()
        self._pool: List[Dict[str, str]] = []
        self._last_refresh: Optional[datetime] = None

    async def scrape_all(self) -> List[str]:
        logger.info("Scraping proxies...")
        tasks = [scraper.scrape() for scraper in self.scrapers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        all_proxies = set()
        for result in results:
            if isinstance(result, list):
                all_proxies.update(result)
        logger.success(f"Scraped {len(all_proxies)} unique proxies")
        return list(all_proxies)

    async def refresh_pool(self, min_proxies: int = 10) -> List[Dict[str, str]]:
        raw_proxies = await self.scrape_all()
        if not raw_proxies:
            logger.warning("No proxies scraped")
            self._load_from_disk()
            return self._pool

        random.shuffle(raw_proxies)
        validated = await self.validator.validate(raw_proxies, max_valid=min_proxies)

        if validated:
            self._pool = validated
            self._last_refresh = datetime.now()
            self._save_to_disk()
        else:
            logger.warning("No valid proxies found")
            self._load_from_disk()

        return self._pool

    def get_random(self) -> Optional[Dict[str, str]]:
        if not self._pool:
            return None
        return random.choice(self._pool)

    def get_batch(self, count: int) -> List[Dict[str, str]]:
        if len(self._pool) <= count:
            return self._pool.copy()
        return random.sample(self._pool, count)

    def _save_to_disk(self) -> None:
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.storage_path, 'w') as f:
            for proxy in self._pool:
                f.write(f"{proxy['url']}\n")
        logger.info(f"Saved {len(self._pool)} proxies")

    def _load_from_disk(self) -> None:
        if not self.storage_path.exists():
            return
        self._pool = []
        with open(self.storage_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    self._pool.append({"url": line, "exit_ip": "unknown"})
        logger.info(f"Loaded {len(self._pool)} proxies from disk")

    @property
    def pool_size(self) -> int:
        return len(self._pool)

    @property
    def last_refresh_time(self) -> Optional[datetime]:
        return self._last_refresh