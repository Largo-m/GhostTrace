import asyncio
import time
from typing import Optional

import stem
import stem.control
from stem import Signal
from loguru import logger


class TorController:
    def __init__(self, control_port: int = 9051, password: str = ""):
        self.control_port = control_port
        self.password = password
        self.controller: Optional[stem.control.Controller] = None
        self._authenticated = False

    async def start(self) -> None:
        loop = asyncio.get_running_loop()
        try:
            self.controller = await loop.run_in_executor(None, self._connect_and_auth)
            self._authenticated = True
            logger.info(f"Connected to Tor on port {self.control_port}")
        except Exception as e:
            logger.error(f"Failed to connect to Tor: {e}")
            raise

    def _connect_and_auth(self) -> stem.control.Controller:
        controller = stem.control.Controller.from_port(port=self.control_port)
        try:
            controller.authenticate(password=self.password)
        except Exception:
            controller.authenticate()
        return controller

    async def new_identity(self) -> bool:
        if not self.controller or not self._authenticated:
            return False
        loop = asyncio.get_running_loop()
        try:
            await loop.run_in_executor(None, self.controller.signal, Signal.NEWNYM)
            logger.success("New Tor identity requested")
            await asyncio.sleep(1)
            return True
        except Exception:
            return False

    def get_circuits(self) -> list:
        if not self.controller or not self._authenticated:
            return []
        try:
            return [str(c) for c in self.controller.get_circuits()]
        except Exception:
            return []

    def is_ready(self) -> bool:
        if not self.controller or not self._authenticated:
            return False
        try:
            return self.controller.is_alive()
        except Exception:
            return False

    async def cleanup(self) -> None:
        if self.controller:
            try:
                self.controller.close()
            except Exception:
                pass