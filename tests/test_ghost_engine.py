import pytest
from core.ghost_engine import GhostEngine, GhostConfig


def test_ghost_config_defaults():
    config = GhostConfig()
    assert config.tor_control_port == 9051
    assert config.min_chain_length == 2
    assert config.max_chain_length == 4
    assert config.spoof_fingerprint is True
    assert config.obfuscate_protocol is True


def test_ghost_config_from_yaml_missing_file():
    config = GhostConfig.from_yaml("nonexistent.yaml")
    assert config.tor_control_port == 9051


def test_ghost_engine_init():
    config = GhostConfig()
    engine = GhostEngine(config)
    assert engine.config == config
    assert engine._running is False
    assert engine._requests_sent == 0
    assert engine._identities_rotated == 0


def test_ghost_engine_print_stats():
    config = GhostConfig()
    engine = GhostEngine(config)
    engine._start_time = None
    engine._print_stats()