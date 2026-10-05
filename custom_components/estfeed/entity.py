"""Shared entity helpers for the Estfeed integration."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo

from .api import MeteringPoint
from .const import DOMAIN, CommodityType
from .coordinator import EstfeedCoordinator
from .statistics import eic_suffix


def meter_device_info(coordinator: EstfeedCoordinator, meter: MeteringPoint) -> DeviceInfo:
    """Device for one metering point, e.g. "Home electricity meter 089N".

    The full EIC lives in ``serial_number`` instead of the name so it does not
    end up in entity IDs, dashboards and screenshots.
    """
    entry = coordinator.config_entry
    title = entry.title if entry is not None else coordinator.slug
    commodity = "electricity" if meter.commodity_type == CommodityType.ELECTRICITY else "gas"
    return DeviceInfo(
        identifiers={(DOMAIN, meter.eic)},
        name=f"{title} {commodity} meter {eic_suffix(meter.eic).upper()}",
        manufacturer="Elering Estfeed",
        model=f"{commodity.capitalize()} metering point",
        serial_number=meter.eic,
    )
