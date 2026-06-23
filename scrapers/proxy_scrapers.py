import asyncio
import re
from typing import List
from scrapers.base_scraper import BaseScraper


class ProxyScrapeScraper(BaseScraper):
    async def fetch(self) -> List[str]:
        session = await self._get_session()
        proxies = []

        urls = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all",
        ]

        for url in urls:
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        for line in text.splitlines():
                            line = line.strip()
                            if line and ":" in line:
                                proxies.append(f"http://{line}")
            except Exception:
                continue

        return proxies


class ProxyListDownloadScraper(BaseScraper):
    async def fetch(self) -> List[str]:
        session = await self._get_session()
        proxies = []

        urls = [
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://www.proxy-list.download/api/v1/get?type=https",
            "https://www.proxy-list.download/api/v1/get?type=socks5",
        ]

        for url in urls:
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        for line in text.splitlines():
                            stripped = line.strip()
                            if stripped and ":" in stripped:
                                proxies.append(f"http://{stripped}")
            except Exception:
                continue

        return proxies


class OpenProxyListScraper(BaseScraper):
    async def fetch(self) -> List[str]:
        session = await self._get_session()
        proxies = []

        api_url = "https://api.openproxylist.xyz/http.txt"

        try:
            async with session.get(api_url) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    for line in text.splitlines():
                        stripped = line.strip()
                        if stripped and ":" in stripped:
                            proxies.append(f"http://{stripped}")
        except Exception:
            pass

        return proxies


class FreeProxyListScraper(BaseScraper):
    async def fetch(self) -> List[str]:
        session = await self._get_session()
        proxies = []

        url = "https://free-proxy-list.net/"

        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    pattern = r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td><td>(\d+)</td>'
                    matches = re.findall(pattern, text)
                    for ip, port in matches:
                        proxies.append(f"http://{ip}:{port}")
        except Exception:
            pass

        return proxies


class GeoNodeScraper(BaseScraper):
    async def fetch(self) -> List[str]:
        session = await self._get_session()
        proxies = []

        url = "https://proxylist.geonode.com/api/proxy-list?limit=100&page=1&sort_by=lastChecked&sort_type=desc&protocols=http,socks5"

        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("data", []):
                        ip = item.get("ip")
                        port = item.get("port")
                        protocols = item.get("protocols", [])
                        if ip and port:
                            if "socks5" in protocols:
                                proxies.append(f"socks5://{ip}:{port}")
                            else:
                                proxies.append(f"http://{ip}:{port}")
        except Exception:
            pass

        return proxies


class SpysMeScraper(BaseScraper):
    async def fetch(self) -> List[str]:
        session = await self._get_session()
        proxies = []

        url = "https://spys.me/proxy.txt"

        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)'
                    matches = re.findall(pattern, text)
                    for ip, port in matches:
                        proxies.append(f"http://{ip}:{port}")
        except Exception:
            pass

        return proxies