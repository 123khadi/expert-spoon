from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Incident
import requests
import os
from django.conf import settings
from django.http import JsonResponse

def citizen_report(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            incident = form.save()
            lang = incident.language
            if lang == 'en':
                msg = 'Report submitted in English!'
            elif lang == 'ur':
                msg = 'رپورٹ اردو میں جمع کر دی گئی!'
            elif lang == 'hi':
                msg = 'रिपोर्ट हिंदी में जमा कर दी गई!'
            messages.success(request, msg)
            return redirect('dashboard')
    else:
        form = IncidentForm()
    return render(request, 'citizen_report.html', {'form': form})

def get_whatsapp_config():
    config = {}
    try:
        path = os.path.join(settings.BASE_DIR, 'whatsapp_config.txt')
        with open(path, 'r') as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    config[k.strip()] = v.strip()
    except:
        pass
    return config

def send_whatsapp_message(to_number, body):
    cfg = get_whatsapp_config()
    phone_id = cfg.get('PHONE_NUMBER_ID')
    token = cfg.get('ACCESS_TOKEN')
    num = to_number.replace(" ", "").replace("-", "")
    if num.startswith('0'):
        num = '92' + num[1:]
    url = f"https://graph.facebook.com/v22.0/{phone_id}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp", "to": num, "type": "text", "text": {"body": body}}
    r = requests.post(url, headers=headers, json=data)
    print("WA RESULT:", r.text)
    return r.json()
# === whatsapp_config.txt se config padhna ===
def get_whatsapp_config():
    config = {}
    try:
        # settings.BASE_DIR / whatsapp_config.txt
        config_path = os.path.join(settings.BASE_DIR, 'whatsapp_config.txt')
        with open(config_path, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        print("whatsapp_config.txt nahi mili!")
    return config

def send_whatsapp_message(to_number, message_body):
    wa_config = get_whatsapp_config()

    phone_id = wa_config.get('1365976849934714')
    token = wa_config.get('ACCESS_TOKEN')

    if not phone_id or not token:
        return {"error": "Config missing - whatsapp_config.txt check karo"}

    url = f"https://graph.facebook.com/v22.0/{1365976849934714}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def generate_ai_sop(incident):
    title = incident.title.lower()
    if "flood" in title or "selab" in title:
        return f"""🚨 FLOOD SOP - {incident.title}
1. Foran Rescue 1122 aur TMA ko call karein.
2. Location: {incident.latitude}, {incident.longitude} par team bhejein.
3. Logon ko mehfooz maqam par muntaqil karein.
4. DC Office Mardan ko update dein.
Severity: {incident.severity} | Status: {incident.status}"""
    elif "fire" in title or "aag" in title:
        return f"""🔥 FIRE SOP - {incident.title}
1. Fire Brigade 16 ko foran ittila dein.
2. Aas paas ki dukanon ko khali karwayen.
3. Bijli ka connection kaat dein.
4. Police aur Rescue ko mauqe par bhejein.
Severity: {incident.severity}"""
    elif "accident" in title:
        return f"""🚑 ACCIDENT SOP - {incident.title}
1. Rescue 1122 aur Traffic Police ko bhejein.
2. Zakhmiyon ko DHQ Mardan shift karein.
3. Road ko clear karwayen.
4. FIR ke liye report darj karein."""
    else:
        return f"""📋 GENERAL SOP - {incident.title}
1. Mutalqa department ko assign karein: {incident.assigned_to if hasattr(incident, 'assigned_to') else 'Rescue/Police'}
2. Mauqe ka jaiza lein: {incident.description}
3. DC Control Room ko 30 min me update dein.
4. WhatsApp alert ke zariye team ko location bhejein.
Severity: {incident.severity}"""


@login_required
def control_dashboard(request):
    incidents = Incident.objects.all().order_by('-created_at')
    return render(request, 'dashboard.html', {'incidents': incidents})


@login_required
def incident_detail(request, id):
    incident = get_object_or_404(Incident, id=id)
    return render(request, 'incident_detail.html', {'incident': incident})
    # === WHATSAPP ALERT - START ===
    try:
        from .views import send_whatsapp_message
    except:
        pass

    try:
        # Yahan apna verified WhatsApp number likho - jisko Meta pe add kiya tha
        my_number = "923325710034"  # <-- APNA NUMBER LIKHO, jaise 923001234567

        wa_msg = f"RapidSOP Mardan Alert 🚨\nNew {sev} - {title}\nLocation: {lat},{lon}\nDesc: {desc}\nID: {inc.id}"
        send_whatsapp_message(my_number, wa_msg)
        print("WhatsApp bheja gaya!")
    except Exception as e:
        print("WhatsApp Error:", e)
    # === WHATSAPP ALERT - END ===
    # PRO VERSION - Puri Dunia ke liye
def send_global_whatsapp(to, message):
    # Ye kisi bhi 0333 number pe bhejega
    print(f"🚀 REAL WHATSAPP TO {to}: {message}")
    return send_whatsapp_message(to, message)

@login_required
def update_incident(request, id):
    incident = get_object_or_404(Incident, id=id)
    if request.method == "POST":
        incident.status = request.POST.get('status')
        incident.severity = request.POST.get('severity')
        if hasattr(incident, 'assigned_to'):
            incident.assigned_to = request.POST.get('assigned_to')

        incident.ai_sop = generate_ai_sop(incident)
        incident.save()
        return redirect(f'/incidents/{incident.id}/')

    return render(request, 'update_incident.html', {'incident': incident})

def citizen_report(request):
    if request.method == "POST":
        title = request.POST.get('title') or "Emergency in Mardan"
        desc = request.POST.get('description') or request.POST.get('details') or "Citizen reported emergency, need help"
        lat = request.POST.get('latitude') or 34.2012
        lon = request.POST.get('longitude') or 72.0525
        sev = request.POST.get('severity') or 'Medium'

        inc = Incident.objects.create(
            title=title,
            description=desc,
            latitude=lat,
            longitude=lon,
            severity=sev,
            status="Pending"
        )

        # AI SOP
        try:
            inc.ai_sop = generate_ai_sop(inc)
            inc.save()
        except:
            pass

        # WhatsApp - yahi se msg jayega
        try:
            from .whatsapp import send_incident_alert
            send_incident_alert(inc)
        except Exception as e:
            print("WhatsApp error:", e)

        return redirect('/dashboard/')

    return render(request, 'citizen_report.html')

def account_settings(request):
    return render(request, 'account_settings.html')


def profile_redirect(request):
    return redirect('/dashboard/')


def update_incident_status(request, incident_id):
    incident = get_object_or_404(Incident, id=incident_id)
    if request.method == "POST":
        new_status = request.POST.get('status')
        if new_status in dict(Incident.STATUS_CHOICES).keys():
            incident.status = new_status
            incident.ai_sop = generate_ai_sop(incident)
            incident.save()
            return redirect('/incident/dashboard/')
    return redirect('/dashboard/')


# === RapidSOP Mardan - WhatsApp Real API ===
WHATSAPP_CONFIG = {
    "PHONE_NUMBER_ID": "1365976849934714",  # Aapka ID - screenshot se
    "ACCESS_TOKEN": "EAAaD9pkdAm4BSs7oNmZCu025tG90WQGDLwxCr2gpS9bzNQXP0q5wvfiNC7XxjOz55qGX4VBK4jrP2jJy1ZB4CFAfrCguXJj7iPsiZAVv74JNlQCH2pj5NGwD2r8EZBlk0PckZBbpnR92B0jwqPTrdvf17poOZAL94cLI6khOTvdIEA5VIF9znsImPLodlebfiZAuH8rNOlrL2jXLDISSnBEvUZBC0Hvi0cE530Cfv6gsUW5i7gAKqmRJE4CjXi1BHw4Uyukg8wiZBlrnzCz94OnpX", # Jo green wala lamba token hai, pura paste karo
}

def send_whatsapp_message(to_number, message_body):
    url = f"https://graph.facebook.com/v22.0/{WHATSAPP_CONFIG['923325710034']}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_CONFIG['ACCESS_TOKEN']}",
        "Content-Type": "application/json"
    }

    # 0333... ko 92333... me convert
    clean_number = to_number.strip().replace(" ", "").replace("-", "")
    if clean_number.startswith('0'):
        clean_number = '92' + clean_number[1:]
    if not clean_number.startswith('+'):
        clean_number = clean_number  # 92 se hi rehne do

    payload = {
        "messaging_product": "whatsapp",
        "to": clean_number,
        "type": "text",
        "text": {"body": message_body}
    }

    r = requests.post(url, headers=headers, json=payload)
    print("WHATSAPP API RESULT:", r.text)
    return r.json()
def send_whatsapp_alert(to_number, incident_text):
    try:
        import requests
    except ImportError:
        return {"error": "requests package is not installed"}

    url = f"https://graph.facebook.com/v19.0/{1365976849934714}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": f"🚨 RapidSOP ALERT: {incident_text}\nLocation: Mardan District"}
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    return response.json()
def get_whatsapp_config():
    config = {}
    try:
        path = os.path.join(settings.BASE_DIR, 'whatsapp_config.txt')
        with open(path, 'r') as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    config[k.strip()] = v.strip()
    except:
        pass
    return config

def send_whatsapp_message(to_number, body):
    cfg = get_whatsapp_config()
    phone_id = cfg.get('PHONE_NUMBER_ID')
    token = cfg.get('ACCESS_TOKEN')
    if not phone_id or not token:
        print("WhatsApp config missing")
        return None

    # 0333 -> 92333
    num = to_number.replace(" ", "").replace("-", "")
    if num.startswith('0'):
        num = '92' + num[1:]

    url = f"https://graph.facebook.com/v22.0/{phone_id}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": num,
        "type": "text",
        "text": {"body": body}
    }
    r = requests.post(url, headers=headers, json=data)
    print("WA RESULT:", r.text)
    return r.json()
def student_admission_view(request):
    if request.method == 'POST':
        student_name = request.POST.get('name')
        student_phone = request.POST.get('phone')
        phone = request.POST.get("phone")
def test_whatsapp(request):
    from django.http import HttpResponse
    try:
        from .adapter import send_whatsapp_message
        result = send_whatsapp_message("923325710034", "Test from RapidSOP - WhatsApp working!")
        return HttpResponse(f"WhatsApp Result: {result}")
    except Exception as e:
        return HttpResponse(f"Error: {e}")

def profile_redirect(request):
    from django.shortcuts import redirect
    return redirect('/dashboard/')

def account_settings(request):
    from django.shortcuts import render
    return render(request, 'account_settings.html')
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json

try:
    from .agent import parse_whatsapp_message, create_incident_from_whatsapp
except ImportError:
    try:
        from incidents.agent import parse_whatsapp_message, create_incident_from_whatsapp
    except ImportError:
        parse_whatsapp_message = None
        create_incident_from_whatsapp = None

try:
    from .adapter import send_whatsapp_message
except ImportError:
    try:
        from incidents.adapter import send_whatsapp_message
    except ImportError:
        def send_whatsapp_message(*args, **kwargs):
            return {"error": "WhatsApp adapter not found"}

VERIFY_TOKEN = "rapidsop123" # ye aapka secret password hai

@csrf_exempt
def whatsapp_webhook(request):
    # Meta verification ke liye
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        return HttpResponse("Verification failed", status=403)

    # Jab Citizen WhatsApp karega
    if request.method == "POST":
        if parse_whatsapp_message is None or create_incident_from_whatsapp is None:
            return JsonResponse({"status": "error", "message": "WhatsApp agent is not available"}, status=500)

        data = json.loads(request.body)
        try:
            entry = data['entry'][0]['changes'][0]['value']
            if 'messages' in entry:
                msg = entry['messages'][0]
                text = msg['text']['body']
                sender = msg['from']

                print(f"WhatsApp Agent ko mila: {text} from {sender}")

                # Agent kaam karega
                parsed = parse_whatsapp_message(text, sender)
                incident = create_incident_from_whatsapp(parsed)

                # Wapas citizen ko reply
                reply = f"✅ RapidSOP: Aapki report mil gayi!\nType: {parsed['type']}\nLocation: {parsed['location']}\nID: #{incident.id}\nTeam jald pohonchegi."
                send_whatsapp_message(sender, reply)

                return JsonResponse({"status": "incident created", "id": incident.id})
        except Exception as e:
            print(f"Agent Error: {e}")

        return JsonResponse({"status": "ok"})

import threading
from django.conf import settings
import requests

WHATSAPP_URL = getattr(settings, "WHATSAPP_URL", None)


def send_whatsapp_message(phone, message):
    if not WHATSAPP_URL:
        return

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message},
    }

    try:
        # timeout 5 seconds; do not block the request flow
        requests.post(WHATSAPP_URL, json=payload, timeout=5)
    except requests.RequestException:
        # If network is slow or unavailable, keep the report flow intact
        pass


def send_whatsapp_in_background(phone, message):
    threading.Thread(
        target=send_whatsapp_message,
        args=(phone, message),
        daemon=True,
    ).start()
import threading
import requests
from django.conf import settings
from django.shortcuts import redirect, render
from .forms import IncidentForm

def send_whatsapp_message(phone, message):
    try:
        # 5 second se zyada wait nahi karega
        url = f"https://graph.facebook.com/v19.0/{settings.WHATSAPP_PHONE_ID}/messages"
        headers = {"Authorization": f"Bearer {settings.WHATSAPP_TOKEN}"}
        data = {"messaging_product": "whatsapp", "to": phone, "type": "text", "text": {"body": message}}
        requests.post(url, json=data, headers=headers, timeout=5)
    except:
        pass

def submit_incident(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save()
            # Yahan se speed ayegi
            phone_number = form.cleaned_data.get('phone') or '03325710034'
            threading.Thread(target=send_whatsapp_message, args=[phone_number, "New Citizen Report Received!"], daemon=True).start()
            return redirect('success')
    else:
        form = IncidentForm()
    return render(request, 'update_incident.html', {'form': form})
def submit_incident(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # WhatsApp abhi band, baad me lagayenge
            return redirect('success')
    else:
        form = IncidentForm()
    return render(request, 'update_incident.html', {'form': form})
import threading
import requests
from django.conf import settings

def send_whatsapp_alert(phone, title):
    try:
        url = f"https://graph.facebook.com/v21.0/{getattr(settings, 'WHATSAPP_PHONE_ID', '')}/messages"
        headers = {"Authorization": f"Bearer {getattr(settings, 'WHATSAPP_TOKEN', '')}", "Content-Type": "application/json"}
        data = {"messaging_product": "whatsapp", "to": phone, "type": "text", "text": {"body": f"RapidSOP Alert: {title}"}}
        requests.post(url, json=data, headers=headers, timeout=3)
    except:
        pass

def citizen_report_submit(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST, request.FILES)
        if form.is_valid():
            incident = form.save()
            # Yahan se speed ayegi - background me jayega, user wait nahi karega
            phone = getattr(incident, 'phone', '923325710034') # apna control room number
            threading.Thread(target=send_whatsapp_alert, args=[phone, incident.title], daemon=True).start()

            return redirect('dashboard')
    else:
        form = IncidentForm()
    return render(request, 'citizen_report.html', {'form': form})

def update_incident_status(request, id):
    if request.method == 'POST':
        incident = Incident.objects.get(id=id)
        new_status = request.POST.get('status')
        incident.status = new_status
        incident.save()
        # Status update pe bhi alert
        threading.Thread(target=send_whatsapp_alert, args=["923325710034", f"Status {new_status}: {incident.title}"], daemon=True).start()
        return redirect('dashboard')


def send_alert_view(request, incident_id):
    incident = Incident.objects.get(id=incident_id)
    # Background me bhejo taake Dashboard slow na ho
    threading.Thread(
        target=send_whatsapp_alert,
        args=[settings.WHATSAPP_CONTROL_ROOM, incident],
        daemon=True
    ).start()
    return redirect('dashboard')

from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import IncidentForm

def citizen_report(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report submitted successfully!')  # Success message
            return redirect('dashboard')
    else:
        form = IncidentForm()
    return render(request, 'citizen_report.html', {'form': form})
