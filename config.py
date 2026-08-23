"""
config.py
Configuration constants for the Django Home Assistant AI Bot.
Replace placeholder values with your actual credentials/settings before deployment.
"""

# ---------------- Email Alert Settings ----------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_bot_email@gmail.com"
SENDER_PASSWORD = "your_app_password"
ALERT_EMAIL = "recipient_email@gmail.com"

# ---------------- Push Notification Settings ----------------
PUSH_SERVICE_API_KEY = "your_push_service_api_key"
PUSH_NOTIFICATION_URL = "https://api.pushservice.com/send"

# ---------------- MQTT Settings ----------------
MQTT_BROKER = "localhost"          # e.g. Mosquitto broker address
MQTT_PORT = 1883
MQTT_TOPIC_COMMANDS = "django/commands"
MQTT_TOPIC_ALERTS = "django/alerts"
MQTT_TOPIC_STATUS = "django/status"
MQTT_USERNAME = "django_bot"
MQTT_PASSWORD = "change_me"

# ---------------- Alert Frequency Control ----------------
ALERT_COOLDOWN_SECONDS = 60  # minimum time between repeated alerts of same type

# ---------------- Sensor Thresholds ----------------
GAS_THRESHOLD_PPM = 300
TEMP_MAX_C = 45
HUMIDITY_MAX_PERCENT = 85
