"""Tests for shared entity helpers."""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import MagicMock

from custom_components.estfeed.api import MeteringPoint, Period
from custom_components.estfeed.const import DOMAIN, CommodityType
from custom_components.estfeed.entity import meter_device_info


def _meter(commodity: CommodityType) -> MeteringPoint:
    return MeteringPoint(
        eic="38ZEE-00000001-A",
        commodity_type=commodity,
        periods=[Period(start=datetime(2024, 1, 1, tzinfo=UTC), end=None)],
    )


def test_device_name_uses_entry_title_and_hides_full_eic():
    coordinator = MagicMock(slug="home")
    coordinator.config_entry.title = "Home"
    info = meter_device_info(coordinator, _meter(CommodityType.ELECTRICITY))
    assert info["name"] == "Home electricity meter 001A"
    assert "38ZEE-00000001-A" not in info["name"]
    assert info["serial_number"] == "38ZEE-00000001-A"
    assert info["identifiers"] == {(DOMAIN, "38ZEE-00000001-A")}
    assert info["model"] == "Electricity metering point"


def test_device_name_falls_back_to_slug_for_gas_without_entry():
    coordinator = MagicMock(slug="cabin", config_entry=None)
    info = meter_device_info(coordinator, _meter(CommodityType.NATURAL_GAS))
    assert info["name"] == "cabin gas meter 001A"
    assert info["model"] == "Gas metering point"
