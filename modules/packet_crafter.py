import random
import struct
from typing import Optional
from scapy.all import IP, TCP, UDP, ICMP, Raw, send
from scapy.all import sr1
from loguru import logger


class PacketCrafter:
    def __init__(self, interface: Optional[str] = None):
        self.interface = interface
        self._ttl_pool = [64, 128, 255]
        self._window_pool = [64240, 65535, 29200, 8192]

    def craft_syn_packet(self, dst_ip: str, dst_port: int, src_ip: Optional[str] = None, src_port: Optional[int] = None) -> IP:
        src_ip = src_ip or self._random_ip()
        src_port = src_port or random.randint(49152, 65535)
        seq = random.randint(0, 4294967295)
        ttl = random.choice(self._ttl_pool)
        window = random.choice(self._window_pool)
        ip = IP(src=src_ip, dst=dst_ip, ttl=ttl)
        tcp = TCP(
            sport=src_port,
            dport=dst_port,
            flags="S",
            seq=seq,
            window=window,
            options=[("MSS", 1460), ("NOP", None), ("WScale", 7), ("NOP", None), ("NOP", None), ("SAckOK", b"")]
        )
        return ip / tcp

    def craft_icmp_probe(self, dst_ip: str, src_ip: Optional[str] = None) -> IP:
        src_ip = src_ip or self._random_ip()
        ttl = random.choice(self._ttl_pool)
        payload = self._random_payload(32)
        ip = IP(src=src_ip, dst=dst_ip, ttl=ttl)
        icmp = ICMP(type=8, code=0) / Raw(load=payload)
        return ip / icmp

    def craft_stealth_scan(self, dst_ip: str, dst_port: int) -> IP:
        src_port = random.randint(1024, 49151)
        seq = random.randint(0, 4294967295)
        ip_id = random.randint(0, 65535)
        ttl = 64
        window = 1024
        ip = IP(dst=dst_ip, id=ip_id, ttl=ttl)
        tcp = TCP(
            sport=src_port,
            dport=dst_port,
            flags="F",
            seq=seq,
            window=window
        )
        return ip / tcp

    def craft_null_packet(self, dst_ip: str, dst_port: int) -> IP:
        src_port = random.randint(1024, 49151)
        seq = random.randint(0, 4294967295)
        ip = IP(dst=dst_ip)
        tcp = TCP(sport=src_port, dport=dst_port, seq=seq, flags="")
        return ip / tcp

    def send_packet(self, packet, timeout: int = 3) -> Optional[IP]:
        try:
            response = sr1(packet, timeout=timeout, verbose=0)
            return response
        except Exception as e:
            logger.error(f"Packet send failed: {e}")
            return None

    def send_bulk(self, packets: list, timeout: int = 3) -> list:
        results = []
        for packet in packets:
            try:
                send(packet, verbose=0)
                results.append({"packet": packet.summary(), "status": "sent"})
            except Exception as e:
                results.append({"packet": packet.summary(), "status": "failed", "error": str(e)})
        return results

    def _random_ip(self) -> str:
        return f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

    def _random_payload(self, size: int) -> bytes:
        return bytes(random.randint(0, 255) for _ in range(size))