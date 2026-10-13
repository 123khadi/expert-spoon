
from django.db import models
from django.contrib.auth.models import User

class Incident(models.Model):
    INCIDENT_TYPES = [
        ('Flood', 'Flood'),
        ('Fire', 'Fire'),
        ('Accident', 'Accident'),
        ('Landslide', 'Landslide'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('Reported', 'Reported'),
        ('In-Progress', 'In-Progress'),
        ('Resolved', 'Resolved'),
    ]
    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ur', 'Urdu (Pakistan)'),
        ('hi', 'Hindi (India)'),
    ]

    title = models.CharField(max_length=200, default="Flood")
    latitude = models.FloatField()
    longitude = models.FloatField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='Medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Reported')
    description = models.TextField(blank=True, null=True, default="No description")
    ai_sop = models.TextField(blank=True, null=True)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    assigned_to = models.CharField(max_length=100, blank=True, help_text="Officer name")
    created_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.severity}"

    def generate_sop(self):
        sops = {
            'Flood': "1. Rescue 1122 & PDMA ko fori inform karein.\n2. Mutasira ilaqa khali karwayein (Mardan S-10B, Charsadda Road).\n3. Medical camp & de-watering pumps bhejein.\n4. DC Mardan ko hourly update dein.",
            'Fire': "1. Fire Brigade 16 & Rescue 1122 ko call karein.\n2. Area cordon off karein.\n3. WAPDA se bijli cut karwayein.\n4. Qareebi hospital alert karein.",
            'Accident': "1. Rescue 1122 & Traffic Police ko inform karein.\n2. Zakhmi ko DHQ Mardan shift karein.\n3. Road clear karwayein.\n4. FIR ke liye SHO ko inform karein.",
            'Landslide': "1. NHA & C&W Department ko inform karein.\n2. Road block karein aur alternate route dein.\n3. Heavy machinery bhejein.",
        }
        self.ai_sop = sops.get(self.title, "1. Control Room se team bhejein.\n2. Mutalqa mehka ko inform karein.\n3. DC ko report karein.")
        self.save()
