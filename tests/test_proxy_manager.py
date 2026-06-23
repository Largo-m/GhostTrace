import pytest
import tempfile
import os
from modules.proxy_manager import ProxyManager


def test_proxy_manager_init():
    pm = ProxyManager(min_chain=2, max_chain=4, timeout=10)
    assert pm.min_chain == 2
    assert pm.max_chain == 4
    assert pm.timeout == 10
    assert pm.available_proxies == []


def test_proxy_count():
    pm = ProxyManager()
    assert pm.proxy_count == 0


def test_build_chain_empty():
    pm = ProxyManager(min_chain=1, max_chain=2)
    chain = pm.build_chain()
    assert len(chain) == 0