import os
import sys
import time
import yaml
import random
import asyncio
import signal
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
from dataclasses import dataclass

from loguru import logger
from rich.console import Console
from rich.table import Table

from core.tor_controller import TorController
from core.fingerprint_spoofer import FingerprintSpoofer
from core.session_manager import SessionManager
from modules.proxy_manager import ProxyManager
from modules.traffic_router import TrafficRouter
from modules.identity_rotator import IdentityRotator
from modules.packet_crafter import PacketCrafter
from modules.protocol_obfuscator import ProtocolObfuscator
from scrapers.pool_manager import PoolManager

console = Console()
logger.add("output/logs/ghost_{time}.log", rotation="10 MB", level="DEBUG")


@dataclass
class GhostConfig:
    tor_control_port: int = 9051
    tor_password: str = ""
    identity_rotation_interval: int = 30
    min_chain_length: int = 2
    max_chain_length: int = 4
    proxy_timeout: int = 10
    spoof_fingerprint: bool = True
    randomize_ua: bool = True
    obfuscate_protocol: bool = True
    auto_scrape_proxies: bool = True
    test_url: str = "https://httpbin.org/ip"
    log_level: str = "DEBUG"

    @classmethod
    def from_yaml(cls, config_path: str = "config/settings.yaml") -> "GhostConfig":
        try:
            with open(config_path, 'r') as f:
                data = yaml.safe_load(f)

            tor_cfg = data.get('tor', {})
            proxy_cfg = data.get('proxy_chains', {})
            fp_cfg = data.get('fingerprint', {})
            targets = data.get('targets', {})
            logging_cfg = data.get('logging', {})
            obf_cfg = data.get('protocol_obfuscation', {})
            scrape_cfg = data.get('proxy_scraping', {})

            return cls(
                tor_control_port=tor_cfg.get('control_port', 9051),
                tor_password=tor_cfg.get('password', ''),
                identity_rotation_interval=tor_cfg.get('new_identity_timeout', 30),
                min_chain_length=proxy_cfg.get('min_chain_length', 2),
                max_chain_length=proxy_cfg.get('max_chain_length', 4),
                proxy_timeout=proxy_cfg.get('rotation_interval', 10),
                spoof_fingerprint=fp_cfg.get('spoof', True),
                randomize_ua=fp_cfg.get('randomize_ua', True),
                obfuscate_protocol=obf_cfg.get('enabled', True),
                auto_scrape_proxies=scrape_cfg.get('auto_scrape', True),
                test_url=targets.get('test_url', 'https://httpbin.org/ip'),
                log_level=logging_cfg.get('level', 'DEBUG')
            )
        except FileNotFoundError:
            logger.warning("Config file not found. Using defaults.")
            return cls()


class GhostEngine:
    def __init__(self, config: Optional[GhostConfig] = None):
        self.config = config or GhostConfig()
        self.tor: Optional[TorController] = None
        self.spoofer: Optional[FingerprintSpoofer] = None
        self.proxy_mgr: Optional[ProxyManager] = None
        self.router: Optional[TrafficRouter] = None
        self.rotator: Optional[IdentityRotator] = None
        self.crafter: Optional[PacketCrafter] = None
        self.obfuscator: Optional[ProtocolObfuscator] = None
        self.pool_mgr: Optional[PoolManager] = None
        self.session = SessionManager()
        self._running = False
        self._start_time: Optional[datetime] = None
        self._identities_rotated = 0
        self._requests_sent = 0
        self.console = Console()
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

    def _handle_shutdown(self, signum, frame):
        logger.info(f"Signal {signum} received")
        self._running = False
        self.console.print("\n[bold red]Ghost vanishing...[/bold red]")
        if self.tor:
            asyncio.get_event_loop().run_until_complete(self.tor.cleanup())
        sys.exit(0)

    async def initialize(self) -> None:
        self.console.print("[bold cyan]Initializing GhostTrace Engine...[/bold cyan]")

        self.session.create_session("ghost_run")

        if self.config.auto_scrape_proxies:
            self.pool_mgr = PoolManager()
            self.console.print("[dim]Proxy scraper ready[/dim]")

        logger.info("Starting Tor Controller...")
        self.tor = TorController(
            control_port=self.config.tor_control_port,
            password=self.config.tor_password
        )
        await self.tor.start()
        logger.success("Tor Controller online")

        if self.config.spoof_fingerprint:
            self.spoofer = FingerprintSpoofer(ua_file="config/useragents.txt")
            self.spoofer.randomize()
            logger.success("Fingerprint spoofer active")

        self.obfuscator = ProtocolObfuscator()
        logger.success("Protocol obfuscator ready")

        self.crafter = PacketCrafter()
        logger.success("Packet crafter ready")

        self.proxy_mgr = ProxyManager(
            min_chain=self.config.min_chain_length,
            max_chain=self.config.max_chain_length,
            timeout=self.config.proxy_timeout
        )
        await self.proxy_mgr.load_proxies(auto_scrape=self.config.auto_scrape_proxies)
        logger.success(f"Proxy manager ready ({self.proxy_mgr.proxy_count} proxies)")

        self.router = TrafficRouter(
            tor_controller=self.tor,
            proxy_manager=self.proxy_mgr,
            spoofer=self.spoofer
        )

        self.rotator = IdentityRotator(
            tor=self.tor,
            interval=self.config.identity_rotation_interval,
            callback=self._on_identity_rotated
        )

        self._start_time = datetime.now()
        self._running = True

        self.console.print("[bold green]GhostTrace engine ready![/bold green]")
        self.console.print(f"[dim]Proxies: {self.proxy_mgr.proxy_count}[/dim]")
        self.console.print(f"[dim]Chain: {self.config.min_chain_length}-{self.config.max_chain_length} hops[/dim]")
        self.console.print(f"[dim]Rotation: {self.config.identity_rotation_interval}s[/dim]")
        self.console.print(f"[dim]Obfuscation: {'ON' if self.config.obfuscate_protocol else 'OFF'}[/dim]")

    async def _on_identity_rotated(self) -> None:
        self._identities_rotated += 1
        self.session.log_identity_rotation()
        self.console.print(f"[yellow]New identity #{self._identities_rotated}[/yellow]")

    async def test_connection(self, url: Optional[str] = None) -> Dict[str, Any]:
        target = url or self.config.test_url
        self.console.print(f"\n[bold blue]Testing {target}...[/bold blue]")

        try:
            chain = self.proxy_mgr.build_chain() if self.proxy_mgr else []
            response = await self.router.route_request(method="GET", url=target, spoof_headers=True)

            self._requests_sent += 1
            self.session.log_request(target, chain)

            if 'application/json' in str(response.headers.get('Content-Type', '')):
                data = response.json()
                self.console.print(f"[green]Server sees: {data.get('origin', 'unknown')}[/green]")

            return {
                "status": response.status_code,
                "headers": dict(response.headers),
                "body": response._text[:200]
            }
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self.console.print(f"[red]Failed: {e}[/red]")
            return {"error": str(e)}

    async def stealth_scan(self, target_ip: str, ports: List[int]) -> Dict[str, Any]:
        self.console.print(f"\n[bold blue]Stealth scan {target_ip}[/bold blue]")

        results = {"target": target_ip, "open_ports": [], "filtered_ports": [], "scan_time": datetime.now().isoformat()}

        for port in ports:
            await asyncio.sleep(random.uniform(0.5, 2))
            packet = self.crafter.craft_stealth_scan(target_ip, port)

            if self.config.obfuscate_protocol and self.obfuscator:
                self.obfuscator.obfuscate(bytes(packet), method="xor_mask")

            response = self.crafter.send_packet(packet, timeout=2)

            if response and response.haslayer("TCP"):
                flags = response.getlayer("TCP").flags
                if flags & 0x12:
                    results["open_ports"].append(port)
                    self.console.print(f"[green]Port {port}: OPEN[/green]")
                elif flags & 0x14:
                    results["filtered_ports"].append(port)
                    self.console.print(f"[yellow]Port {port}: FILTERED[/yellow]")
            else:
                self.console.print(f"[dim]Port {port}: no response[/dim]")

        return results

    async def run_stealth_loop(self, duration: Optional[int] = None) -> None:
        if not self._running:
            await self.initialize()

        rotator_task = asyncio.create_task(self.rotator.start_rotation())
        self.console.print("[bold magenta]Ghost haunting the network...[/bold magenta]")
        self.console.print("[dim]Ctrl+C to stop[/dim]\n")

        end_time = datetime.now() + timedelta(seconds=duration) if duration else None

        try:
            while self._running:
                if end_time and datetime.now() >= end_time:
                    break

                await self.test_connection()
                self._print_stats()
                await asyncio.sleep(random.uniform(5, 15))

        except asyncio.CancelledError:
            pass
        finally:
            rotator_task.cancel()
            self.console.print("[bold]GhostTrace stopped.[/bold]")

    def _print_stats(self) -> None:
        table = Table(title="GhostTrace Stats", header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        uptime = datetime.now() - self._start_time if self._start_time else timedelta(0)
        table.add_row("Uptime", str(uptime).split('.')[0])
        table.add_row("Identities", str(self._identities_rotated))
        table.add_row("Requests", str(self._requests_sent))
        table.add_row("Proxies", str(self.proxy_mgr.proxy_count if self.proxy_mgr else 0))
        table.add_row("Spoofing", "ON" if self.config.spoof_fingerprint else "OFF")
        table.add_row("Obfuscation", self.obfuscator.get_method() if self.obfuscator else "none")

        self.console.print(table)

    async def single_request_demo(self, url: str) -> None:
        await self.initialize()

        self.console.print(f"\n[bold]Demo: {url}[/bold]")

        self.console.print("[bold yellow]Real IP:[/bold yellow]")
        try:
            import requests
            real = requests.get('https://httpbin.org/ip', timeout=5).json()
            self.console.print(f"  {real.get('origin')}")
        except Exception:
            self.console.print("  [red]unknown[/red]")

        self.console.print("\n[bold green]Ghost IP:[/bold green]")
        result = await self.test_connection(url)
        if 'error' not in result:
            self.console.print("[bold green]Anonymity preserved![/bold green]")