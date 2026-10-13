import requests
from django.conf import settings
import logging

def send_whatsapp_alert(to_phone, incident):
    """
    Modified Integrated Alert - Mardan RapidSOP
    """
    try:
        # Number ko Pakistan format me convert karo
        if to_phone.startswith('0'):
            to_phone = '92' + to_phone[1:]

        token = settings.WHATSAPP_TOKEN
        phone_id = settings.WHATSAPP_PHONE_ID

        if not token or token.startswith("EAA") == False:
            print("Token sahi nahi hai!")
            return False

        url = f"https://graph.facebook.com/v21.0/{phone_id}/messages"

        headers = {
            "Authorization": f"Bearer {token}", # <-- Yahan YOUR_API_KEY ki jagah token ayega
            "Content-Type": "application/json"
        }

        # Dashboard wale SOP ko message me bhejenge
        message_body = f"""🚨 *RapidSOP - DC Mardan*
*Incident:* {incident.title}
*Location:* {incident.latitude}, {incident.longitude}
*Severity:* {incident.severity}
*Status:* {incident.status}

*SOP:*
{incident.sop_text if hasattr(incident, 'sop_text') else 'Team ko foran assign karen'}

📍 https://maps.google.com/?q={incident.latitude},{incident.longitude}
"""

        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "text",
            "text": {"body": message_body}
        }

        response = requests.post(url, json=payload, headers=headers, timeout=5)
        print(f"WhatsApp Response: {response.status_code} - {response.text}")
        return response.status_code == 200

    except Exception as e:
        print(f"WhatsApp Error: {e}")
        return False
