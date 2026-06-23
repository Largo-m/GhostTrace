import random
from pathlib import Path
from typing import Optional
from fake_useragent import UserAgent


class FingerprintSpoofer:
    def __init__(self, ua_file: Optional[str] = None):
        self.ua_file = ua_file
        self.current_ua = ""
        self.current_headers = {}
        self._fallback_ua = UserAgent()
        self._custom_uas = []
        self._load_useragents()

    def _load_useragents(self):
        if self.ua_file and Path(self.ua_file).exists():
            with open(self.ua_file, 'r') as f:
                self._custom_uas = [line.strip() for line in f if line.strip()]

    def randomize(self) -> dict:
        accept_languages = [
            "en-US,en;q=0.9",
            "en-GB,en;q=0.8",
            "fr-FR,fr;q=0.9,en;q=0.7",
            "de-DE,de;q=0.9,en;q=0.7",
        ]
        accept_encodings = ["gzip, deflate, br", "gzip, deflate", "br, gzip, deflate"]

        if self._custom_uas:
            ua = random.choice(self._custom_uas)
        else:
            ua = self._fallback_ua.random

        self.current_ua = ua
        self.current_headers = {
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": random.choice(accept_languages),
            "Accept-Encoding": random.choice(accept_encodings),
            "DNT": str(random.choice([0, 1])),
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
        }
        return self.current_headers

    def get_headers(self) -> dict:
        if not self.current_headers:
            self.randomize()
        return self.current_headers.copy()

    def get_ua(self) -> str:
        if not self.current_ua:
            self.randomize()
        return self.current_ua