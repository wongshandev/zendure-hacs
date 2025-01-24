"""Config flow for Zendure integration."""
from __future__ import annotations

from typing import Any

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol

from .const import DOMAIN

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Zendure Integration."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input["name"],
                data={
                    "name": user_input["name"],
                    "device_id": user_input["device_id"],
                    "mqtt_host": user_input["mqtt_host"],
                    "mqtt_port": user_input["mqtt_port"],
                    "mqtt_username": user_input["mqtt_username"],
                    "mqtt_password": user_input["mqtt_password"]
                }
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name"): str,
                vol.Required("device_id"): str,
                vol.Required("mqtt_host"): str,
                vol.Required("mqtt_port", default=1883): int,
                vol.Required("mqtt_username"): str,
                vol.Required("mqtt_password"): str
            }),
            errors=errors
        )