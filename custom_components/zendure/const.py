"""Constants for the Zendure integration."""

DOMAIN = "zendure"
NAME = "Zendure"

# API相关常量
API_BASE_URL = "https://app.zendure.tech"
API_TIMEOUT = 30

# MQTT相关常量
MQTT_BROKER = "mqtt.zendure.tech"
MQTT_PORT = 1883
MQTT_USERNAME = "zendure"
MQTT_PASSWORD = "zendure"
MQTT_TOPIC_PREFIX = "zendure/device"

# 设备状态相关常量
DEVICE_ONLINE = "online"
DEVICE_OFFLINE = "offline"

# 传感器类型
SENSOR_BATTERY_LEVEL = "battery_level"
SENSOR_CHARGING_STATUS = "charging_status"
SENSOR_OUTPUT_POWER = "output_power"
SENSOR_INPUT_POWER = "input_power"