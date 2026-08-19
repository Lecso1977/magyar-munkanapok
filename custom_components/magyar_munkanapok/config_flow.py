"""Config flow for Magyar munkanapok integration."""
from __future__ import annotations

from typing import Any
import voluptuous as fill_schema

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import CONF_CUSTOM_HOLIDAYS, CONF_CUSTOM_WORKDAYS, DOMAIN, NAME


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
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            # Tisztítjuk a beviteli mezők tartalmát (szóközök, felesleges sorvégjelek eltávolítása)
            cleaned_input = {
                CONF_CUSTOM_WORKDAYS: user_input.get(CONF_CUSTOM_WORKDAYS, "").strip(),
                CONF_CUSTOM_HOLIDAYS: user_input.get(CONF_CUSTOM_HOLIDAYS, "").strip(),
            }
            return self.async_create_entry(title="", data=cleaned_input)

        options = self.config_entry.options

        return self.async_show_form(
            step_id="init",
            data_schema=fill_schema.Schema(
                {
                    fill_schema.Optional(
                        CONF_CUSTOM_WORKDAYS,
                        default=options.get(CONF_CUSTOM_WORKDAYS, ""),
                    ): cv.string,
                    fill_schema.Optional(
                        CONF_CUSTOM_HOLIDAYS,
                        default=options.get(CONF_CUSTOM_HOLIDAYS, ""),
                    ): cv.string,
                }
            ),
        )
