import random
import zlib
import base64
from typing import Optional, Dict, Any
from loguru import logger


class ProtocolObfuscator:
    def __init__(self):
        self._obfuscation_methods = ["base64_pad", "gzip_wrap", "xor_mask", "chunk_split", "noise_inject"]
        self._current_method = None
        self._noise_pool = [
            b"X-Forwarded-For: 127.0.0.1\r\n",
            b"X-Real-IP: 10.0.0.1\r\n",
            b"Cache-Control: no-cache\r\n",
            b"Pragma: no-cache\r\n",
            b"Via: 1.1 proxy\r\n",
        ]

    def obfuscate(self, data: bytes, method: Optional[str] = None) -> bytes:
        method = method or random.choice(self._obfuscation_methods)
        self._current_method = method

        if method == "base64_pad":
            return self._obf_base64_pad(data)
        elif method == "gzip_wrap":
            return self._obf_gzip_wrap(data)
        elif method == "xor_mask":
            return self._obf_xor_mask(data)
        elif method == "chunk_split":
            return self._obf_chunk_split(data)
        elif method == "noise_inject":
            return self._obf_noise_inject(data)
        return data

    def deobfuscate(self, data: bytes, method: Optional[str] = None) -> bytes:
        method = method or self._current_method

        if method == "base64_pad":
            return self._deobf_base64_pad(data)
        elif method == "gzip_wrap":
            return self._deobf_gzip_wrap(data)
        elif method == "xor_mask":
            return self._deobf_xor_mask(data)
        elif method == "chunk_split":
            return self._deobf_chunk_split(data)
        elif method == "noise_inject":
            return self._deobf_noise_inject(data)
        return data

    def _obf_base64_pad(self, data: bytes) -> bytes:
        encoded = base64.b64encode(data)
        padding = random.randint(1, 10)
        return encoded + b"=" * padding

    def _deobf_base64_pad(self, data: bytes) -> bytes:
        cleaned = data.rstrip(b"=")
        return base64.b64decode(cleaned)

    def _obf_gzip_wrap(self, data: bytes) -> bytes:
        compressed = zlib.compress(data, level=9)
        header = b"\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff"
        return header + compressed[2:-4]

    def _deobf_gzip_wrap(self, data: bytes) -> bytes:
        stripped = data[10:]
        return zlib.decompress(stripped, -15)

    def _obf_xor_mask(self, data: bytes) -> bytes:
        key = random.randint(1, 255)
        masked = bytes([b ^ key for b in data])
        return bytes([key]) + masked

    def _deobf_xor_mask(self, data: bytes) -> bytes:
        key = data[0]
        return bytes([b ^ key for b in data[1:]])

    def _obf_chunk_split(self, data: bytes) -> bytes:
        chunk_size = random.randint(8, 32)
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        separator = b"\r\n" if random.choice([True, False]) else b"\n"
        return separator.join(chunks)

    def _deobf_chunk_split(self, data: bytes) -> bytes:
        data = data.replace(b"\r\n", b"").replace(b"\n", b"")
        return data

    def _obf_noise_inject(self, data: bytes) -> bytes:
        result = bytearray()
        mid = len(data) // 2
        result.extend(data[:mid])
        noise = random.choice(self._noise_pool)
        result.extend(noise)
        result.extend(data[mid:])
        result.extend(random.choice(self._noise_pool))
        return bytes(result)

    def _deobf_noise_inject(self, data: bytes) -> bytes:
        for noise in self._noise_pool:
            data = data.replace(noise, b"")
        return data

    def obfuscate_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        obfuscated = {}
        normal_headers = {
            "Host", "User-Agent", "Accept", "Accept-Language",
            "Accept-Encoding", "Connection", "Content-Type", "Content-Length"
        }
        fake_headers = {
            "X-Requested-With": "XMLHttpRequest",
            "X-Forwarded-Proto": "https",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Referer": "https://www.google.com/search?q=" + str(random.randint(10000, 99999)),
            "Origin": "https://" + self._random_domain(),
        }

        for key, value in headers.items():
            if key in normal_headers:
                obfuscated[key] = value
            else:
                obfuscated[f"X-{key}"] = value

        injection_count = random.randint(1, 3)
        for _ in range(injection_count):
            fake_key, fake_val = random.choice(list(fake_headers.items()))
            obfuscated[fake_key] = fake_val

        return obfuscated

    def _random_domain(self) -> str:
        tlds = [".com", ".org", ".net", ".io", ".co"]
        names = ["cdn", "static", "assets", "media", "img", "api", "cdn2", "secure"]
        return random.choice(names) + random.choice(tlds)

    def get_method(self) -> str:
        return self._current_method or "none"