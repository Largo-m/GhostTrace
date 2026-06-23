import asyncio
from typing import Callable, Optional
from loguru import logger


class IdentityRotator:
    def __init__(self, tor, interval: int = 30, callback: Optional[Callable] = None):
        self.tor = tor
        self.interval = interval
        self.callback = callback
        self._task: Optional[asyncio.Task] = None
        self._running = False

    async def start_rotation(self) -> None:
        self._running = True
        self._task = asyncio.create_task(self._rotation_loop())
        logger.info(f"Identity rotation started, interval: {self.interval}s")

    async def _rotation_loop(self) -> None:
        while self._running:
            try:
                await asyncio.sleep(self.interval)
                success = await self.tor.new_identity()
                if success and self.callback:
                    await self.callback()
            except asyncio.CancelledError:
                logger.info("Rotation loop cancelled")
                break
            except Exception as e:
                logger.error(f"Rotation error: {e}")
                await asyncio.sleep(5)

    async def stop_rotation(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            logger.info("Identity rotation stopped")

    async def rotate_now(self) -> bool:
        result = await self.tor.new_identity()
        if result and self.callback:
            await self.callback()
        return result

    @property
    def is_rotating(self) -> bool:
        return self._running