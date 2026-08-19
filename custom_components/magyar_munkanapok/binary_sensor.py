"""Binary sensor platform for Magyar munkanapok integration."""
from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_CUSTOM_HOLIDAYS, CONF_CUSTOM_WORKDAYS, DOMAIN
from .hu_holidays import HungarianHolidays


def parse_custom_dates(raw_text: str) -> dict[date, str]:
    """Segédfüggvény az egyedi dátumok feldolgozásához."""
    parsed: dict[date, str] = {}
    if not raw_text:
        return parsed

    cleaned = raw_text.replace("\n", ",").split(",")
    for item in cleaned:
        item = item.strip()
        if not item:
            continue

        description = ""
        if ":" in item:
            date_part, description = item.split(":", 1)
            date_part = date_part.strip()
            description = description.strip()
        else:
            date_part = item

        try:
            parsed_date = date.fromisoformat(date_part)
            parsed[parsed_date] = description
        except ValueError:
            continue

    return parsed


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Magyar munkanapok binary sensor."""
    async_add_entities([MagyarMunkanapokSensor(entry)], True)


class MagyarMunkanapokSensor(BinarySensorEntity):
    """Representation of the Magyar munkanapok binary sensor."""

    _attr_has_entity_name = True
    _attr_name = "Magyar munkanapok"
    _attr_icon = "mdi:calendar-check"
    _attr_device_class = BinarySensorDeviceClass.RUNNING

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_binary_sensor"
        self._holidays = HungarianHolidays()

    @property
    def is_on(self) -> bool:
        """Return true if today is a workday."""
        today = date.today()
        options = self._entry.options

        custom_workdays = parse_custom_dates(options.get(CONF_CUSTOM_WORKDAYS, ""))
        custom_holidays = parse_custom_dates(options.get(CONF_CUSTOM_HOLIDAYS, ""))

        if today in custom_workdays:
            return True
        if today in custom_holidays:
            return False

        return self._holidays.is_workday(today)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return device state attributes."""
        today = date.today()
        options = self._entry.options

        custom_workdays = parse_custom_dates(options.get(CONF_CUSTOM_WORKDAYS, ""))
        custom_holidays = parse_custom_dates(options.get(CONF_CUSTOM_HOLIDAYS, ""))

        is_workday = self.is_on
        day_type = "Munkanap" if is_workday else "Munkaszuneti nap"

        # Következő munkanap megkeresése
        next_workday = today + timedelta(days=1)
        while True:
            if next_workday in custom_workdays:
                break
            if next_workday not in custom_holidays and self._holidays.is_workday(next_workday):
                break
            next_workday += timedelta(days=1)

        # Következő munkaszüneti nap megkeresése
        next_holiday = today + timedelta(days=1)
        next_holiday_desc = ""
        while True:
            if next_holiday in custom_holidays:
                next_holiday_desc = custom_holidays[next_holiday] or "Egyedi munkaszüneti nap"
                break
            if next_holiday not in custom_workdays and not self._holidays.is_workday(next_holiday):
                next_holiday_desc = self._holidays.get_holiday_name(next_holiday) or "Hétvége / Ünnepnap"
                break
            next_holiday += timedelta(days=1)

        return {
            "nap_tipusa": day_type,
            "munkanap": is_workday,
            "hetvege": today.weekday() in (5, 6),
            "kovetkezo_munkanap": next_workday.isoformat(),
            "kovetkezo_munkaszuneti_nap": next_holiday.isoformat(),
            "kovetkezo_munkaszuneti_nap_leirasa": next_holiday_desc,
        }
