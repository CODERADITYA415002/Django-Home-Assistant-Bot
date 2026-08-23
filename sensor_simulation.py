"""
sensor_simulation.py
Virtual sensor simulation layer for the Django Home Assistant AI Bot (Phase-I).

Since Phase-I hardware sensors were not yet physically integrated for all
scenarios, this module generates simulated real-time sensor data streams
(smoke/gas, temperature, humidity, PIR motion, and seismic/accelerometer
vibration) that feed into the alert and AI decision-making pipeline.
"""

import random
import time

import config


def read_gas_sensor():
    """Simulate an MQ-series gas sensor reading in ppm."""
    return round(random.uniform(50, 400), 2)


def read_temperature():
    """Simulate a DHT11/DHT22 style temperature reading in Celsius."""
    return round(random.uniform(20, 50), 1)


def read_humidity():
    """Simulate a DHT11/DHT22 style humidity reading in % RH."""
    return round(random.uniform(20, 90), 1)


def read_pir_motion():
    """Simulate a PIR motion sensor. Returns True if motion detected."""
    return random.random() < 0.1  # 10% chance of motion per poll


def read_seismic_vibration():
    """Simulate an accelerometer-based seismic/abrupt-motion reading (g-force)."""
    return round(random.uniform(0.0, 2.0), 2)


def poll_all_sensors():
    """Poll every simulated sensor once and return a dict of readings."""
    return {
        "gas_ppm": read_gas_sensor(),
        "temperature_c": read_temperature(),
        "humidity_pct": read_humidity(),
        "motion_detected": read_pir_motion(),
        "seismic_g": read_seismic_vibration(),
        "timestamp": time.time(),
    }


def evaluate_hazards(readings):
    """
    Compare sensor readings against configured thresholds and return
    a list of hazard types that were triggered.
    """
    hazards = []

    if readings["gas_ppm"] > config.GAS_THRESHOLD_PPM:
        hazards.append("gas_leak")

    if readings["temperature_c"] > config.TEMP_MAX_C:
        hazards.append("fire_risk")

    if readings["humidity_pct"] > config.HUMIDITY_MAX_PERCENT:
        hazards.append("flooding_risk")

    if readings["seismic_g"] > 1.2:
        hazards.append("seismic_event")

    return hazards


if __name__ == "__main__":
    # Simple standalone test loop
    for _ in range(5):
        data = poll_all_sensors()
        print("Sensor readings:", data)
        print("Hazards detected:", evaluate_hazards(data))
        time.sleep(1)
