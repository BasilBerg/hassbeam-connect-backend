"""Configuration flow for HassBeam Connect Backend integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the configuration flow for HassBeam Connect Backend."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial configuration step."""
        # Only allow one instance
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
            
        # Create entry directly without showing form
        return self.async_create_entry(
            title="HassBeam Connect Backend", 
            data={}
        )

    async def async_step_import(self, import_data: dict[str, Any]) -> FlowResult:
        """Handle import from discovery or configuration.yaml."""
        # Only allow one instance
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
            
        # Create entry from auto-discovery
        return self.async_create_entry(
            title="HassBeam Connect Backend", 
            data=import_data or {}
        )
