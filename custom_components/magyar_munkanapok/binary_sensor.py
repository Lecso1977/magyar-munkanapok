"""Binary sensor platform for Magyar munkanapok integration."""
from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_CUSTOM_HOLIDAYS,
    CONF_CUSTOM_WORKDAYS,
    DOMAIN,
    FIX_HOLIDAYS,
    NAME,
    OFFICIAL_SHIFTED_HOLIDAYS,
    OFFICIAL_SHIFTED_WORKDAYS,
)


def get_easter_sunday(year: int) -> date:
    """Calculates Easter Sunday date using Anonymous Gregorian algorithm."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def get_movable_holidays(year: int) -> dict[date, str]:
    """Returns all Easter-based movable holidays for a given year."""
    easter = get_easter_sunday(year)
    good_friday = easter - timedelta(days=2)
    easter_monday = easter + timedelta(days=1)
    whit_monday = easter + timedelta(days=50)

    return {
        good_friday: "Nagypéntek",
        easter_monday: "Húsvéthétfő",
        whit_monday: "Pünkösdhétfő",
    }


def parse_custom_dates(raw_text: str) -> dict[date, str]:
    """Parses raw text input into a dictionary of date -> description."""
    parsed: dict[date, str] = {}
    if not raw_text:
        return parsed

    # Elválasztójelek kezelése (új sor vagy vessző)
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
    _attr_name = None
    _attr_icon = "mdi:calendar-check"

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self._entry = entry
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}"
        self._is_on: bool = False
        self._reason: str = ""

    @property
    def is_on(self) -> bool:
        """Return True if today is a workday."""
        return self._is_on

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra attributes for the sensor."""
        return {
            "ok": self._reason,
            "munkanap": self._is_on,
        }

    async def async_update(self) -> None:
        """Update the sensor state based on today's date."""
        today = date.today()
        today_str = today.isoformat()
        current_year = today.year

        # Beállításokból az egyedi napok beolvasása
        options = self._entry.options
        custom_workdays = parse_custom_dates(options.get(CONF_CUSTOM_WORKDAYS, ""))
        custom_holidays = parse_custom_dates(options.get(CONF_CUSTOM_HOLIDAYS, ""))

        # --- PRIORITÁSI LÁNCSZÁMÍTÁS ---

        # 1. Egyedi felülbírálás (Felhasználó által megadott)
        if today in custom_workdays:
            desc = custom_workdays[today]
            self._is_on = True
            self._reason = f"Egyedi munkanap{f' ({desc})' if desc else ''}"
            return

        if today in custom_holidays:
            desc = custom_holidays[today]
            self._is_on = False
            self._reason = f"Egyedi munkaszüneti nap{f' ({desc})' if desc else ''}"
            return

        # 2. Évente változó hivatalos áthelyezett napok
        if today_str in OFFICIAL_SHIFTED_WORKDAYS:
            self._is_on = True
            self._reason = OFFICIAL_SHIFTED_WORKDAYS[today_str]
            return

        if today_str in OFFICIAL_SHIFTED_HOLIDAYS:
            self._is_on = False
            self._reason = OFFICIAL_SHIFTED_HOLIDAYS[today_str]
            return

        # 3. Fix állami ünnepek
        month_day = (today.month, today.day)
        if month_day in FIX_HOLIDAYS:
            self._is_on = False
            self._reason = FIX_HOLIDAYS[month_day]
            return

        # 4. Vándorló ünnepnapok (Húsvét alapú)
        movable_holidays = get_movable_holidays(current_year)
        if today in movable_holidays:
            self._is_on = False
            self._reason = movable_holidays[today]
            return

        # 5. Hétvégi / Hétköznapi alapszabály
        if today.weekday() >= 5:  # Szombat (5) vagy Vasárnap (6)
            self._is_on = False
            self._reason = "Hétvége"
        else:
            self._is_on = True
            self._reason = "Munkanap"
