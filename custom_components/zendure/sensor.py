"""Platform for Zendure sensor integration."""
from __future__ import annotations
import logging
import json
from typing import Any

from homeassistant.components.mqtt import async_publish_to_mqtt
from homeassistant.components.mqtt.subscription import async_subscribe_topics
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import (
    PERCENTAGE,
    POWER_WATT,
)

from .const import (
    DOMAIN,
    MQTT_BROKER,
    MQTT_PORT,
    MQTT_USERNAME,
    MQTT_PASSWORD,
    MQTT_TOPIC_PREFIX,
    SENSOR_BATTERY_LEVEL,
    SENSOR_CHARGING_STATUS,
    SENSOR_OUTPUT_POWER,
    SENSOR_INPUT_POWER,
)

_LOGGER = logging.getLogger(__name__)

SENSOR_DESCRIPTIONS = [
    SensorEntityDescription(
        key=SENSOR_BATTERY_LEVEL,
        name="Battery Level",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=SENSOR_CHARGING_STATUS,
        name="Charging Status",
        icon="mdi:battery-charging",
    ),
    SensorEntityDescription(
        key=SENSOR_OUTPUT_POWER,
        name="Output Power",
        native_unit_of_measurement=POWER_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=SENSOR_INPUT_POWER,
        name="Input Power",
        native_unit_of_measurement=POWER_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
]

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Zendure sensors."""
    device_id = entry.data['device_id']
    mqtt_topic = f"{MQTT_TOPIC_PREFIX}/{device_id}/status"
    
    sensors = [ZendureSensor(hass, entry, description, mqtt_topic) for description in SENSOR_DESCRIPTIONS]
    async_add_entities(sensors, True)

class ZendureSensor(SensorEntity):
    """Representation of a Zendure Sensor."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, description: SensorEntityDescription, mqtt_topic: str) -> None:
        """Initialize the sensor."""
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_name = f"{entry.data['name']} {description.name}"
        self._attr_native_value = None
        self._entry = entry
        self._hass = hass
        self._mqtt_topic = mqtt_topic
        self._mqtt_subscription = None

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT topic when entity is added to hass."""
        @callback
        def message_received(msg: Any) -> None:
            """Handle new MQTT messages."""
            try:
                import pdb; pdb.set_trace()  # 添加断点
                data = json.loads(msg.payload)
                if self.entity_description.key == SENSOR_BATTERY_LEVEL:
                    self._attr_native_value = data.get('battery_level')
                elif self.entity_description.key == SENSOR_CHARGING_STATUS:
                    self._attr_native_value = data.get('charging_status')
                elif self.entity_description.key == SENSOR_OUTPUT_POWER:
                    self._attr_native_value = data.get('output_power')
                elif self.entity_description.key == SENSOR_INPUT_POWER:
                    self._attr_native_value = data.get('input_power')
                self.async_write_ha_state()
            except Exception as err:
                _LOGGER.error("Error processing MQTT message: %s", err)

        self._mqtt_subscription = await async_subscribe_topics(
            self._hass,
            self._mqtt_subscription,
            {
                "state_topic": {
                    "topic": self._mqtt_topic,
                    "msg_callback": message_received,
                    "qos": 1,
                }
            },
        )

    async def async_will_remove_from_hass(self) -> None:
        """Unsubscribe from MQTT topic when entity is removed from hass."""
        if self._mqtt_subscription:
            await async_unsubscribe_topics(self._hass, self._mqtt_subscription)

    async def async_update(self) -> None:
        """No polling needed for MQTT."""
        pass