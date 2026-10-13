import re
from.models import Incident

def parse_whatsapp_message(message_text, sender_name="WhatsApp Citizen"):
    """
    Hamara chota AI Agent - message se incident nikalta hai
    """
    message_text = message_text.lower()

    # 1. Type detect karega
    incident_type = "Other"
    if any(w in message_text for w in ["aag", "fire", "jal"]):
        incident_type = "Fire"
    elif any(w in message_text for w in ["flood", "selaab", "paani"]):
        incident_type = "Flood"
    elif any(w in message_text for w in ["accident", "hadsa", "takkar"]):
        incident_type = "Accident"
    elif any(w in message_text for w in ["bijli", "light", "electric"]):
        incident_type = "Electric"

    # 2. Severity detect karega
    severity = "Medium"
    if any(w in message_text for w in ["emergency", "foran", "jaldi", "bahut", "zyada"]):
        severity = "High"
    elif any(w in message_text for w in ["chota", "kam", "thoda"]):
        severity = "Low"

    # 3. Location nikalega
    location = "Chitral/Mardan" # default
    # Simple logic: "in" ke baad wala location
    match = re.search(r"(?:in|at|near)\s+([a-zA-Z\s]+)", message_text)
    if match:
        location = match.group(1).strip().title()

    return {
        "title": f"{incident_type} reported via WhatsApp",
        "description": message_text,
        "location": location,
        "severity": severity,
        "type": incident_type,
        "reporter": sender_name
    }

def create_incident_from_whatsapp(parsed_data):
    incident = Incident.objects.create(
        title=parsed_data["title"],
        description=parsed_data["description"],
        location=parsed_data["location"],
        severity=parsed_data["severity"],
        incident_type=parsed_data["type"],
        reported_by=parsed_data["reporter"],
        status="Active"
    )
    return incident