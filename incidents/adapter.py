from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_app(self, request, provider, client_id=None):
        try:
            return super().get_app(request, provider, client_id)
        except SocialApp.MultipleObjectsReturned:
            return SocialApp.objects.filter(provider=provider).first()
        except SocialApp.DoesNotExist:
            return SocialApp.objects.filter(provider=provider).first()
import requests

TOKEN = "EAAaD9pkdAm4BSiDIJG4t7bZCRQRIwq9YEyavXEQGU2ZAcx5XZCmopUUZBsM7DgXCfg8aN9ckZAbIRzdE3W6o2R6R10tXXbwxNiwyHF63sayUTa0RSLOoflq8lCKBdYDjsQHhyeRI49B3T4X1qV5OL4ZA7o11g2fVuSOr37l2DkN3A3UocEokYDdIhZCadQh9c9xlLUiybyrBcSZA1rAmF8HMjdybDuZC925ENezJGYRaeF0uI3aViCcdMVpgE8gseUKtcs2Q9RwGsgbVKlkIbB6ZAAkAZDZD"  # Step 1 wala temporary token
PHONE_ID = "1365976849934714"  # Meta dashboard se milega
#WhatsApp_Business_account ID = 1859457492075624

def send_incident_alert(incident):
    url = f"https://graph.facebook.com/v22.0/{PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": "923325710034",  # aapka number
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {"code": "en_US"}
        }
    }
    r = requests.post(url, headers=headers, json=data)
    print("WHATSAPP RESULT:", r.text)
    return r.text