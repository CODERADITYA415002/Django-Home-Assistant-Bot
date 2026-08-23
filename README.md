# Django — AI-Controlled Home Assistant Bot

**Team 4 | DY Patil College of Engineering, Akurdi, Pune**
Robotics & Automation Engineering Department | Academic Year 2024–25

Guide: Mr. Nilesh Mahajan

Team: Aditya Chavan, Shivam Amrutkar, Soham Bansode, Sahil Birle, Vishwajeet Hadake

---

## Overview

Django is a Wall-E-inspired, AI-controlled home assistant robot built as a
proof-of-concept that combines smart home automation, environmental
monitoring, safety alerting, and interactive AI-driven assistance into a
single modular robotic platform.

Phase-I of the project focuses on the software architecture: natural
language command interpretation, simulated environmental sensing (gas,
temperature, humidity, seismic activity), MQTT-based communication with a
mobile app, and reinforcement-learning-driven adaptive behavior. Hardware
mobility is powered by an Arduino Uno, DC geared motors, and an L298N motor
driver, with Bluetooth v5.0 used for short-range appliance control and an
ESP32-CAM planned for machine vision.

## Key Features

- **Smart Home Control** — Turn lights, fans, AC, TV, and other appliances
  on/off via Bluetooth/Wi-Fi from a mobile app.
- **Environmental Monitoring** — Live temperature, humidity, and gas
  concentration readings with hazard alerting.
- **Natural Language Commands** — Transformer-based NLP interprets
  context-sensitive queries like *"Is there smoke in the kitchen?"*
- **MQTT Communication** — Lightweight, low-latency messaging between the
  bot and the companion mobile app.
- **Reinforcement Learning** — Adaptive response tuning based on
  reward/penalty feedback from simulated hazard events.
- **Modular 3D-Printed Chassis** — PLA+ body (20×20×22 cm) designed for easy
  upgrades and component swaps.
- **Planned**: disaster alert system, elderly fall detection, parental
  controls, and educational modules for children.

## Project Structure

```
django-home-assistant-bot/
├── main_bot.py              # Entry point — orchestrates sensors, NLP, MQTT, and alerts
├── sensor_simulation.py      # Simulated gas/temperature/humidity/motion/seismic sensors
├── nlp_engine.py             # Natural language command interpretation & response generation
├── mqtt_communication.py     # MQTT client for bot <-> mobile app communication
├── config.py                 # Configuration constants (SMTP, API keys, MQTT, thresholds)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Hardware Components

| Component | Specification |
|---|---|
| Arduino UNO | ATmega328P, 14 Digital I/O Pins |
| Motor Driver | L298N Dual H-Bridge, 2A per channel |
| DC Geared Motor | 12V, 100–150 RPM, 37mm diameter |
| ESP32-CAM | 2MP camera, Wi-Fi, MicroSD |
| Bluetooth Module | HC-05, v2.0, 10m range |
| Gas Sensor | MQ-series, analog output |
| Temp/Humidity Sensor | 0–50°C / 20–90% RH |
| Chassis | 3D-printed PLA, 20x20x22 cm |
| Power Supply | 12V Li-Po, 2200mAh |

## Setup & Installation

1. Clone the repository (see Git instructions below).
2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Update `config.py` with your actual SMTP credentials, push notification
   API key, and MQTT broker details.
5. Start an MQTT broker locally (e.g. [Mosquitto](https://mosquitto.org/)) if
   testing communication end-to-end.
6. Run the bot:
   ```bash
   python main_bot.py
   ```

## Usage

- The bot polls simulated sensors every few seconds and publishes readings
  and alerts over MQTT.
- Send natural language commands (e.g. via an MQTT test client or the
  companion mobile app) to the `django/commands` topic in the form:
  ```json
  {"command": "Is there smoke in the kitchen?"}
  ```
- Responses and status updates are published to `django/status`, and
  hazard alerts to `django/alerts`.

## Future Roadmap

- Physical embodiment with autonomous navigation
- Real sensor calibration and hardware integration
- TLS-encrypted MQTT communication
- Multilingual NLP support
- Integration with Google Home / Amazon Alexa ecosystems
- Disaster alert system (earthquake, flood, fire, gas leak)
- Elderly fall detection and emergency alerting
- Educational modules for children via machine vision

## References

See the full project report for detailed literature review and citations,
including works by Colombo et al. (2023), Zhang & Li (2022), Brown et al.
(2020), Chen & Martinez (2021), and Patel & Williams (2021).

## License

Academic project — DY Patil College of Engineering, Akurdi. For educational
use; contact the team for reuse permissions.
