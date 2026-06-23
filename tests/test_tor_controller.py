import pytest
from core.tor_controller import TorController


def test_tor_controller_init():
    controller = TorController(control_port=9051, password="test")
    assert controller.control_port == 9051
    assert controller.password == "test"
    assert controller._authenticated is False


def test_get_circuits_not_authenticated():
    controller = TorController()
    circuits = controller.get_circuits()
    assert circuits == []


def test_is_ready_not_authenticated():
    controller = TorController()
    ready = controller.is_ready()
    assert ready is False