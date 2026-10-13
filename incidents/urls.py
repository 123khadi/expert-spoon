from django.urls import path
from . import views

urlpatterns = [
    path('', views.citizen_report, name='report'),
	path('report/', views.citizen_report, name='report_page'),
	path('dashboard/', views.control_dashboard, name='dashboard'),
	path('incident/<int:incident_id>/', views.incident_detail, name='incident_detail'),
	path('account/', views.account_settings, name='account_settings'),
	path('accounts/profile/', views.profile_redirect, name='profile_redirect'),
    path('incident/<int:incident_id>/update_status/', views.update_incident_status, name='update_incident_status'),
    path('incident/<int:incident_id>/update/', views.update_incident, name='update_incident'),
    path('report/', views.citizen_report, name='citizen_report'),
    path('test-wa/', views.test_whatsapp, name='test_whatsapp'),
	
]
