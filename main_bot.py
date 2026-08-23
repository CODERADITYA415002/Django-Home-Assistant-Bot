"""
main_bot.py
Main entry point for the Django Home Assistant AI Bot (Phase-I software
prototype).

Orchestrates:
  - Sensor polling & hazard evaluation (sensor_simulation.py)
  - Natural language command interpretation (nlp_engine.py)
  - MQTT-based communication with the mobile app (mqtt_communication.py)
  - Email / push notification alerting

Includes the alert-dispatch functions (send_email_alert, send_push_notification,
send_alert) as originally implemented and shown in the project presentation.
"""

import smtplib
import time
from email.mime.text import MIMEText

import requests

import config
import nlp_engine
import sensor_simulation
from mqtt_communication import DjangoMQTTClient

# Tracks last alert time per sensor_type to avoid notification spam
_last_alert_time = {}


# ---------------------------------------------------------------------------
# Alerting functions
# ---------------------------------------------------------------------------
def send_email_alert(sensor_type):
    """Send an email alert for a triggered sensor/hazard type."""
    message = MIMEText(
        f"Django Home Assistant Bot Alert: {sensor_type} threshold exceeded!"
    )
    message["Subject"] = f"Django Alert: {sensor_type}"
    message["From"] = config.SENDER_EMAIL
    message["To"] = config.ALERT_EMAIL

    try:
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.starttls()  # Enable secure connection
            server.login(config.SENDER_EMAIL, config.SENDER_PASSWORD)
            server.sendmail(config.SENDER_EMAIL, config.ALERT_EMAIL, message.as_string())
            print(f"[EMAIL] {sensor_type} alert sent successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to send email alert for {sensor_type}: {e}")


def send_push_notification(sensor_type):
    """
    Sends a push notification via an external service for a given sensor type.
    """
    try:
        data = {
            "api_key": config.PUSH_SERVICE_API_KEY,
            "sensor_type": sensor_type,
            "message": f"Alert: {sensor_type} threshold exceeded!",
        }
        response = requests.post(config.PUSH_NOTIFICATION_URL, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(f"[PUSH] {sensor_type} push notification sent successfully.")
    except requests.RequestException as e:
        print(f"[ERROR] Failed to send push notification for {sensor_type}: {e}")


def send_alert(sensor_type):
    """
    Sends alerts via email and push notification for a given sensor type.
    Checks alert frequency to avoid spam.
    """
    now = time.time()
    last_time = _last_alert_time.get(sensor_type, 0)

    if now - last_time < config.ALERT_COOLDOWN_SECONDS:
        print(f"[SKIP] {sensor_type} alert suppressed (cooldown active).")
        return

    send_email_alert(sensor_type)
    send_push_notification(sensor_type)
    _last_alert_time[sensor_type] = now


# ---------------------------------------------------------------------------
# Command handling (bridges MQTT <-> NLP engine)
# ---------------------------------------------------------------------------
def handle_incoming_command(payload):
    """Callback invoked when a command arrives from the mobile app via MQTT."""
    text = payload.get("command", "")
    if not text:
        return

    intent_result = nlp_engine.interpret_command(text)
    response_text = nlp_engine.generate_response(intent_result)
    print(f"[AI] Command: '{text}' -> Intent: {intent_result['intent']} "
          f"-> Response: {response_text}")

    mqtt_client.publish_status({
        "type": "command_response",
        "command": text,
        "response": response_text,
    })


# ---------------------------------------------------------------------------
# Main monitoring loop
# ---------------------------------------------------------------------------
def run_monitoring_loop(poll_interval_seconds=5, iterations=None):
    """
    Continuously poll simulated sensors, evaluate hazards, and dispatch
    alerts + MQTT status updates. If `iterations` is None, runs forever.
    """
    count = 0
    while iterations is None or count < iterations:
        readings = sensor_simulation.poll_all_sensors()
        hazards = sensor_simulation.evaluate_hazards(readings)

        mqtt_client.publish_status({"type": "sensor_readings", **readings})

        for hazard in hazards:
            mqtt_client.publish_alert(hazard, f"{hazard} detected!")
            send_alert(hazard)

        time.sleep(poll_interval_seconds)
        count += 1


if __name__ == "__main__":
    mqtt_client = DjangoMQTTClient(on_command_callback=handle_incoming_command)
    mqtt_client.connect()

    try:
        run_monitoring_loop(poll_interval_seconds=5)
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Stopping Django bot...")
    finally:
        mqtt_client.disconnect()
