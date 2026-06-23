import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def run_web():
    import uvicorn
    from web.app import app
    print("Starting Web Dashboard on http://127.0.0.1:5000")
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")


def main():
    if "--demo" in sys.argv:
        import asyncio
        from core.ghost_engine import GhostEngine, GhostConfig
        config = GhostConfig.from_yaml("config/settings.yaml")
        ghost = GhostEngine(config)
        try:
            asyncio.run(ghost.single_request_demo(config.test_url))
        except Exception as e:
            print(f"[!] Tor not running: {e}")
            print("[!] Make sure Tor Browser is open and connected")

    elif "--scrape" in sys.argv:
        import asyncio
        from scrapers.pool_manager import PoolManager
        print("Scraping fresh proxies...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def run():
            pool = PoolManager()
            try:
                proxies = await pool.refresh_pool(min_proxies=5)
                return proxies
            finally:
                for s in pool.scrapers:
                    await s.close()
                await pool.validator.close()

        proxies = loop.run_until_complete(run())
        loop.close()
        print(f"\nGot {len(proxies)} valid proxies")
        for p in proxies[:10]:
            print(f"  {p['url']} -> {p['exit_ip']}")

    elif "--scan" in sys.argv:
        try:
            idx = sys.argv.index("--scan")
            target = sys.argv[idx + 1]
            print(f"[!] Scan requires Tor running. Target: {target}")
            print("[!] Open Tor Browser first, then try again")
        except (ValueError, IndexError):
            print("Usage: python ghost.py --scan <target_ip>")

    elif "--duration" in sys.argv:
        print("[!] Stealth loop requires Tor running")
        print("[!] Open Tor Browser first, then try again")

    elif "--web" in sys.argv:
        run_web()

    else:
        print("GhostTrace - Stealth Proxy Chain Analyzer")
        print("  --demo       Show real vs ghost IP")
        print("  --scrape     Scrape fresh proxies")
        print("  --scan <IP>  Stealth scan target")
        print("  --duration N Run stealth loop")
        print("  --web        Launch web dashboard")


if __name__ == "__main__":
    main()