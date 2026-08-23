"""
nlp_engine.py
AI Processing Unit for the Django Home Assistant AI Bot.

Interprets natural language commands from the mobile application and maps
them to executable bot actions (e.g. "Is there smoke in the kitchen?",
"Start patrolling the hall.", "Send me a safety report.").

Phase-I uses simple rule/keyword-based intent matching as a lightweight
stand-in for the transformer-based LLM described in the project report.
Swap `interpret_command` internals for an actual LLM call if available.
"""

import re

# Intent keyword map: intent_name -> list of trigger phrases/keywords
INTENT_KEYWORDS = {
    "check_smoke": ["smoke", "fire", "burning"],
    "check_gas": ["gas", "leak"],
    "start_patrol": ["patrol", "start patrolling", "go to"],
    "stop_patrol": ["stop patrolling", "stop patrol", "halt"],
    "status_report": ["status report", "safety report", "how are things"],
    "control_appliance": ["turn on", "turn off", "switch on", "switch off"],
    "greeting": ["hello", "hi django", "hey django"],
}


def interpret_command(text):
    """
    Given a raw natural language command string, return a dict describing
    the detected intent and any extracted entities (e.g. room name,
    appliance name).
    """
    normalized = text.lower().strip()

    detected_intent = "unknown"
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            detected_intent = intent
            break

    entities = _extract_entities(normalized)

    return {
        "raw_text": text,
        "intent": detected_intent,
        "entities": entities,
    }


def _extract_entities(text):
    """Extract simple entities like room names or appliance names."""
    rooms = ["kitchen", "hall", "bedroom", "living room", "bathroom"]
    appliances = ["light", "fan", "ac", "television", "tv", "washing machine",
                  "refrigerator"]

    found_room = next((r for r in rooms if r in text), None)
    found_appliance = next((a for a in appliances if a in text), None)

    action = None
    if re.search(r"\bturn on\b|\bswitch on\b", text):
        action = "on"
    elif re.search(r"\bturn off\b|\bswitch off\b", text):
        action = "off"

    return {
        "room": found_room,
        "appliance": found_appliance,
        "action": action,
    }


def generate_response(intent_result, hazard_status=None):
    """Generate a natural-language style response for a given intent."""
    intent = intent_result["intent"]

    if intent == "check_smoke":
        return "No smoke detected currently." if not hazard_status else \
            "Warning: smoke levels are elevated!"
    if intent == "check_gas":
        return "Gas levels are within safe limits." if not hazard_status else \
            "Alert: gas leak detected, please check immediately!"
    if intent == "start_patrol":
        room = intent_result["entities"].get("room") or "the house"
        return f"Starting patrol towards {room}."
    if intent == "stop_patrol":
        return "Patrol stopped. Returning to standby mode."
    if intent == "status_report":
        return "All systems nominal. No hazards detected in the last cycle."
    if intent == "control_appliance":
        appliance = intent_result["entities"].get("appliance") or "the device"
        action = intent_result["entities"].get("action") or "toggled"
        return f"{appliance.capitalize()} has been {action}."
    if intent == "greeting":
        return "Hello! I'm Django, your home assistant. How can I help?"

    return "Sorry, I didn't understand that command. Could you rephrase it?"


if __name__ == "__main__":
    test_commands = [
        "Is there smoke in the kitchen?",
        "Start patrolling the hall.",
        "Send me a safety report.",
        "Turn off the fan in the bedroom",
    ]
    for cmd in test_commands:
        result = interpret_command(cmd)
        print(result, "->", generate_response(result))
