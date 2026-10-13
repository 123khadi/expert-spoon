
from django.contrib import admin
from django.urls import include, path
from incidents import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('incidents.urls')),
    path('', views.citizen_report, name='report'),
    path('dashboard/', views.control_dashboard, name='dashboard'),
    path('account/', views.account_settings, name='account_settings'),
    path('incident/<int:incident_id>/', views.incident_detail, name='incident_detail'),
    path('accounts/', include('allauth.urls')),
    path('account/', include('allauth.urls')),  # Include allauth URLs for account management
    path('settings/', views.account_settings, name='account_settings'),
    path('incident/<int:incident_id>/update_status/', views.update_incident_status, name='update_incident_status'),
    path('accounts/profile/', views.control_dashboard, name='profile_redirect'),  # Redirect to dashboard after login
    path('whatsapp/webhook/', views.whatsapp_webhook, name='whatsapp_webhook'),
    path('whatsapp/webhook/', views.whatsapp_webhook, name='whatsapp_webhook'),


]
