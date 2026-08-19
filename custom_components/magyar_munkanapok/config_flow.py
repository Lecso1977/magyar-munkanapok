"""Config flow for Magyar munkanapok integration."""
from __future__ import annotations

from datetime import date
from typing import Any
import voluptuous as fill_schema

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import CONF_CUSTOM_HOLIDAYS, CONF_CUSTOM_WORKDAYS, DOMAIN, NAME


def parse_and_sort_dates(raw_text: str) -> list[tuple[date, str]]:
    """Dátumok feldolgozása és időrendbe rendezése."""
    parsed: list[tuple[date, str]] = []
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
            parsed.append((parsed_date, description))
        except ValueError:
            continue

    parsed.sort(key=lambda x: x[0])
    return parsed


class MagyarMunkanapokConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Magyar munkanapok."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=NAME, data={})

        return self.async_show_form(step_id="user")

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return MagyarMunkanapokOptionsFlowHandler(config_entry)


class MagyarMunkanapokOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Magyar munkanapok."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        options = self._config_entry.options

        existing_workdays = parse_and_sort_dates(options.get(CONF_CUSTOM_WORKDAYS, ""))
        existing_holidays = parse_and_sort_dates(options.get(CONF_CUSTOM_HOLIDAYS, ""))

        workdays_options = {
            d.isoformat(): f"{d.isoformat()}{f' ({desc})' if desc else ''}"
            for d, desc in existing_workdays
        }
        holidays_options = {
            d.isoformat(): f"{d.isoformat()}{f' ({desc})' if desc else ''}"
            for d, desc in existing_holidays
        }

        if user_input is not None:
            kept_workdays: list[str] = []
            selected_workdays = user_input.get("keep_workdays") or []
            for d, desc in existing_workdays:
                if d.isoformat() in selected_workdays:
                    kept_workdays.append(f"{d.isoformat()}:{desc}" if desc else d.isoformat())

            kept_holidays: list[str] = []
            selected_holidays = user_input.get("keep_holidays") or []
            for d, desc in existing_holidays:
                if d.isoformat() in selected_holidays:
                    kept_holidays.append(f"{d.isoformat()}:{desc}" if desc else d.isoformat())

            new_workday = user_input.get("new_workday", "").strip()
            if new_workday:
                kept_workdays.append(new_workday)

            new_holiday = user_input.get("new_holiday", "").strip()
            if new_holiday:
                kept_holidays.append(new_holiday)

            cleaned_input = {
                CONF_CUSTOM_WORKDAYS: ", ".join(kept_workdays),
                CONF_CUSTOM_HOLIDAYS: ", ".join(kept_holidays),
            }
            return self.async_create_entry(title="", data=cleaned_input)

        schema_dict: dict[Any, Any] = {}

        if workdays_options:
            schema_dict[
                fill_schema.Optional(
                    "keep_workdays",
                    default=list(workdays_options.keys()),
                )
            ] = cv.multi_select(workdays_options)

        schema_dict[fill_schema.Optional("new_workday", default="")] = cv.string

        if holidays_options:
            schema_dict[
                fill_schema.Optional(
                    "keep_holidays",
                    default=list(holidays_options.keys()),
                )
            ] = cv.multi_select(holidays_options)

        schema_dict[fill_schema.Optional("new_holiday", default="")] = cv.string

        return self.async_show_form(
            step_id="init",
            data_schema=fill_schema.Schema(schema_dict),
        )
